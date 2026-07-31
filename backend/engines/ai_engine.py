import json
import re

from openai import OpenAI

from backend.config import settings
from backend.schemas.audit import AuditReport
from backend.schemas.ai import AIAnalysisResponse, Recommendation
from backend.engines.prompts import build_ai_prompt


def run_ai_reasoning_service(report: AuditReport) -> AIAnalysisResponse:
    """
    Executes AI reasoning using Featherless AI.

    IMPORTANT:
    - The raw CSV is NEVER sent.
    - Only the AuditReport JSON is sent.
    - Falls back to deterministic reasoning if API fails.
    """

    prompt = build_ai_prompt(report)

    if settings.FEATHERLESS_API_KEY.strip():

        try:

            client = OpenAI(
                api_key=settings.FEATHERLESS_API_KEY.strip(),
                base_url=settings.FEATHERLESS_BASE_URL
            )

            response = client.chat.completions.create(
                model=settings.FEATHERLESS_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content":
                        (
                            "You are an expert AI Data Quality Engineer. "
                            "Always return ONLY valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
            )

            response_text = response.choices[0].message.content.strip()

            # Remove markdown wrappers if model returns ```json
            clean_json = re.sub(
                r"^```(?:json)?",
                "",
                response_text,
                flags=re.MULTILINE,
            )

            clean_json = re.sub(
                r"```$",
                "",
                clean_json,
                flags=re.MULTILINE,
            ).strip()

            parsed = json.loads(clean_json)

            return AIAnalysisResponse(**parsed)

        except Exception as e:

            print(
                f"[Featherless Exception] {e}"
            )

            print(
                "Falling back to deterministic reasoning..."
            )

    return _generate_fallback_ai_response(report)


def _generate_fallback_ai_response(
    report: AuditReport,
) -> AIAnalysisResponse:

    score = report.readiness_score.overall_score

    issues = report.issues

    dataset_id = report.dataset_id

    health_summary = (
        f"Dataset '{report.filename}' has a "
        f"Readiness Score of "
        f"{score}/100 "
        f"(Grade {report.readiness_score.grade}). "
        f"{len(issues)} quality issue(s) "
        f"were detected."
    )

    explanation = (
        f"The dataset contains "
        f"{report.summary.total_rows} rows and "
        f"{report.summary.total_columns} columns. "
        f"Missing values account for "
        f"{report.summary.total_missing_pct}% "
        f"of all cells. "
        f"Duplicate rows account for "
        f"{report.summary.total_duplicate_pct}% "
        f"of the dataset. "
        f"A total of "
        f"{report.summary.total_outliers} "
        f"IQR outliers were detected."
    )

    recommendations = []

    code = [
        "import pandas as pd",
        "import numpy as np",
        "",
        f"df = pd.read_csv('{report.filename}')",
        "df_clean = df.copy()",
        "",
    ]

    rec = 1

    # -----------------------------------------------------
    # Duplicate Rows
    # -----------------------------------------------------

    if report.summary.total_duplicate_rows > 0:

        recommendations.append(
            Recommendation(
                id=f"rec_{rec}",
                category="duplicate_rows",
                title="Remove duplicate rows",
                impact="Prevents duplicate learning samples.",
                suggested_action="Use df.drop_duplicates().",
                priority="high",
            )
        )

        code.extend(
            [
                "# Remove duplicates",
                "df_clean.drop_duplicates(inplace=True)",
                "",
            ]
        )

        rec += 1

    # -----------------------------------------------------
    # Missing Values
    # -----------------------------------------------------

    if report.summary.total_missing_cells > 0:

        recommendations.append(
            Recommendation(
                id=f"rec_{rec}",
                category="missing_values",
                title="Handle missing values",
                impact="Improves ML model quality.",
                suggested_action="Median for numeric, mode for categorical.",
                priority="high",
            )
        )

        code.extend(
            [
                "# Fill missing values",
                "for col in df_clean.columns:",
                "    if df_clean[col].dtype in ['int64','float64']:",
                "        df_clean[col] = df_clean[col].fillna(df_clean[col].median())",
                "    else:",
                "        mode = df_clean[col].mode()",
                "        if len(mode):",
                "            df_clean[col] = df_clean[col].fillna(mode[0])",
                "",
            ]
        )

        rec += 1

    # -----------------------------------------------------
    # Outliers
    # -----------------------------------------------------

    if report.summary.total_outliers > 0:

        recommendations.append(
            Recommendation(
                id=f"rec_{rec}",
                category="outliers",
                title="Cap outliers using IQR",
                impact="Reduces effect of extreme values.",
                suggested_action="Apply IQR Winsorization.",
                priority="medium",
            )
        )

        code.extend(
            [
                "# IQR Outlier Capping",
                "num_cols = df_clean.select_dtypes(include=[np.number]).columns",
                "",
                "for col in num_cols:",
                "    q1 = df_clean[col].quantile(0.25)",
                "    q3 = df_clean[col].quantile(0.75)",
                "    iqr = q3 - q1",
                "    lower = q1 - 1.5 * iqr",
                "    upper = q3 + 1.5 * iqr",
                "    df_clean[col] = np.clip(df_clean[col], lower, upper)",
                "",
            ]
        )

        rec += 1

    code.extend(
        [
            "# Save cleaned dataset",
            f"df_clean.to_csv('cleaned_{report.filename}', index=False)",
            "",
            "print('Cleaning completed successfully.')",
        ]
    )

    return AIAnalysisResponse(
        dataset_id=dataset_id,
        health_summary=health_summary,
        explanation=explanation,
        recommendations=recommendations,
        python_code="\n".join(code),
    )
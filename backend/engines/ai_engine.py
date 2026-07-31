import json
import re

from openai import OpenAI

from backend.config import settings
from backend.schemas.audit import AuditReport
from backend.schemas.ai import (
    AIAnalysisResponse,
    Decision,
)
from backend.engines.prompts import build_ai_prompt


def run_ai_reasoning_service(
    report: AuditReport,
) -> AIAnalysisResponse:
    """
    Executes AI reasoning using Featherless AI.

    The raw CSV is NEVER sent.

    Only the structured audit report is
    provided to the LLM.
    """

    prompt = build_ai_prompt(report)

    if settings.FEATHERLESS_API_KEY.strip():

        try:

            client = OpenAI(
                api_key=settings.FEATHERLESS_API_KEY.strip(),
                base_url=settings.FEATHERLESS_BASE_URL,
            )

            response = client.chat.completions.create(
                model=settings.FEATHERLESS_MODEL,
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content":
                        (
                            "You are an expert AI "
                            "Data Quality Decision Engine. "
                            "Always return ONLY valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            response_text = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

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
                "Falling back to deterministic AI..."
            )

    return _generate_fallback_ai_response(report)


def _generate_fallback_ai_response(
    report: AuditReport,
) -> AIAnalysisResponse:

    dataset_id = report.dataset_id

    score = report.readiness_score.overall_score

    grade = report.readiness_score.grade

    issues = report.issues

    summary = report.summary

    health_summary = (
        f"Dataset '{report.filename}' "
        f"received an AI Readiness Score "
        f"of {score}/100 "
        f"(Grade {grade}). "
        f"The audit detected "
        f"{len(issues)} quality issue(s)."
    )

    explanation = (
        f"The dataset contains "
        f"{summary.total_rows} rows and "
        f"{summary.total_columns} columns. "
        f"The audit identified "
        f"{summary.total_missing_cells} missing values, "
        f"{summary.total_duplicate_rows} duplicate rows, "
        f"and "
        f"{summary.total_outliers} statistical outliers."
    )

    decisions = []

    code = [

        "import pandas as pd",

        "import numpy as np",

        "",

        f"df = pd.read_csv('{report.filename}')",

        "",

        "df_clean = df.copy()",

        "",

    ]
        # =====================================================
    # DUPLICATE ROWS
    # =====================================================

    if summary.total_duplicate_rows > 0:

        decisions.append(

            Decision(

                decision="Remove Duplicate Rows",

                target="Entire Dataset",

                confidence=99,

                reason=(
                    f"{summary.total_duplicate_rows} duplicate "
                    "rows were detected."
                ),

                expected_impact=(
                    "Removes redundant records and improves "
                    "dataset consistency."
                ),

                auto_fix=True,

            )

        )

        code.extend(
            [

                "# --------------------------------",

                "# Remove duplicate rows",

                "# --------------------------------",

                "df_clean.drop_duplicates(inplace=True)",

                "",

            ]
        )

    # =====================================================
    # MISSING VALUES
    # =====================================================

    if summary.total_missing_cells > 0:

        decisions.append(

            Decision(

                decision="Fill Missing Values",

                target="Columns containing null values",

                confidence=97,

                reason=(
                    f"{summary.total_missing_cells} missing "
                    "values were detected."
                ),

                expected_impact=(
                    "Improves completeness and prevents loss "
                    "of training information."
                ),

                auto_fix=True,

            )

        )

        code.extend(
            [

                "# --------------------------------",

                "# Fill Missing Values",

                "# --------------------------------",

                "for col in df_clean.columns:",

                "    if df_clean[col].isnull().sum() == 0:",

                "        continue",

                "",

                "    if pd.api.types.is_numeric_dtype(df_clean[col]):",

                "        df_clean[col] = df_clean[col].fillna(",

                "            df_clean[col].median()",

                "        )",

                "",

                "    else:",

                "        mode = df_clean[col].mode()",

                "",

                "        if len(mode):",

                "            df_clean[col] = df_clean[col].fillna(",

                "                mode.iloc[0]",

                "            )",

                "",

            ]
        )
            # =====================================================
    # OUTLIERS
    # =====================================================

    if summary.total_outliers > 0:

        decisions.append(

            Decision(

                decision="Cap Outliers",

                target="Numeric Columns",

                confidence=95,

                reason=(
                    f"{summary.total_outliers} statistical "
                    "outliers were detected using the "
                    "IQR method."
                ),

                expected_impact=(
                    "Reduces the influence of extreme values "
                    "while preserving most observations."
                ),

                auto_fix=True,

            )

        )

        code.extend(
            [

                "# --------------------------------",

                "# Cap Outliers using IQR",

                "# --------------------------------",

                "numeric_columns = df_clean.select_dtypes(",

                "    include=[np.number]",

                ").columns",

                "",

                "for col in numeric_columns:",

                "    q1 = df_clean[col].quantile(0.25)",

                "    q3 = df_clean[col].quantile(0.75)",

                "    iqr = q3 - q1",

                "",

                "    if iqr == 0:",

                "        continue",

                "",

                "    lower = q1 - 1.5 * iqr",

                "    upper = q3 + 1.5 * iqr",

                "",

                "    df_clean[col] = np.clip(",

                "        df_clean[col],",

                "        lower,",

                "        upper",

                "    )",

                "",

            ]
        )

    # =====================================================
    # DATA TYPE CORRECTION
    # =====================================================

    decisions.append(

        Decision(

            decision="Correct Data Types",

            target="Automatically Detectable Columns",

            confidence=90,

            reason=(
                "Ensure numeric and datetime columns use "
                "appropriate data types whenever possible."
            ),

            expected_impact=(
                "Improves downstream analytics and model "
                "training."
            ),

            auto_fix=True,

        )

    )

    code.extend(
        [

            "# --------------------------------",

            "# Attempt datatype correction",

            "# --------------------------------",

            "for col in df_clean.columns:",

            "    if df_clean[col].dtype == object:",

            "        try:",

            "            df_clean[col] = pd.to_numeric(",

            "                df_clean[col]",

            "            )",

            "        except Exception:",

            "            pass",

            "",

        ]
    )

    # =====================================================
    # CONSTANT COLUMNS
    # =====================================================

    decisions.append(

        Decision(

            decision="Review Constant Columns",

            target="Columns with a single unique value",

            confidence=88,

            reason=(
                "Constant features contribute little or no "
                "predictive value."
            ),

            expected_impact=(
                "Removing constant columns can simplify "
                "the dataset."
            ),

            auto_fix=False,

        )

    )
        # =====================================================
    # SAVE CLEANED DATASET
    # =====================================================

    code.extend(
        [

            "# --------------------------------",

            "# Save cleaned dataset",

            "# --------------------------------",

            "output_file = 'cleaned_dataset.csv'",

            "",

            "df_clean.to_csv(",

            "    output_file,",

            "    index=False",

            ")",

            "",

            "print(",

            "    f'Cleaned dataset saved to: {output_file}'",

            ")",

            "",

        ]
    )

    # =====================================================
    # FALLBACK DECISION
    # =====================================================

    if len(decisions) == 0:

        decisions.append(

            Decision(

                decision="No Action Required",

                target="Dataset",

                confidence=100,

                reason=(
                    "The audit did not identify any major "
                    "data quality issues."
                ),

                expected_impact=(
                    "Dataset is already suitable for "
                    "analysis and machine learning."
                ),

                auto_fix=False,

            )

        )

    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return AIAnalysisResponse(

        dataset_id=dataset_id,

        health_summary=health_summary,

        explanation=explanation,

        decisions=decisions,

        python_code="\n".join(code),

    )
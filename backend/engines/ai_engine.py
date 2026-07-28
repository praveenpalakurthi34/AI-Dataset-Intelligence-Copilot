import json
import re
from google import genai
from backend.config import settings
from backend.schemas.audit import AuditReport
from backend.schemas.ai import AIAnalysisResponse, Recommendation
from backend.engines.prompts import build_gemini_prompt

def run_ai_reasoning_service(report: AuditReport) -> AIAnalysisResponse:
    """
    Executes AI Reasoning Service on AuditReport JSON using Gemini 2.5 Flash.
    Gemini NEVER receives raw CSV.
    If GEMINI_API_KEY is not set, returns deterministic fallback reasoning.
    """
    prompt = build_gemini_prompt(report)

    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY.strip())
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )

            response_text = response.text.strip()
            
            # Clean markdown codeblocks if wrapped in ```json ... ```
            clean_json_str = re.sub(r"^```(json)?", "", response_text, flags=re.MULTILINE)
            clean_json_str = re.sub(r"```$", "", clean_json_str, flags=re.MULTILINE).strip()

            parsed = json.loads(clean_json_str)
            return AIAnalysisResponse(**parsed)

        except Exception as e:
            print(f"[Gemini API Call Exception]: {e}. Falling back to deterministic reasoning.")

    # Deterministic Rule-Based Fallback Reasoning
    return _generate_fallback_ai_response(report)


def _generate_fallback_ai_response(report: AuditReport) -> AIAnalysisResponse:
    score = report.readiness_score.overall_score
    issues = report.issues
    dataset_id = report.dataset_id

    health_summary = (
        f"Dataset '{report.filename}' has a Readiness Score of {score}/100 (Grade {report.readiness_score.grade}). "
        f"A total of {len(issues)} data quality issue(s) were identified across {report.summary.total_columns} columns."
    )

    explanation_parts = [
        f"The dataset consists of {report.summary.total_rows} rows and {report.summary.total_columns} columns.",
        f"Missing cells account for {report.summary.total_missing_pct}% of total cells.",
        f"Exact duplicate rows represent {report.summary.total_duplicate_pct}% of the dataset.",
        f"A total of {report.summary.total_outliers} statistical IQR outliers were detected."
    ]
    explanation = " ".join(explanation_parts)

    recommendations = []
    code_lines = [
        "import pandas as pd",
        "import numpy as np",
        "",
        "# 1. Load dataset",
        f"df = pd.read_csv('{report.filename}')",
        "df_clean = df.copy()",
        ""
    ]

    rec_counter = 1
    if report.summary.total_duplicate_rows > 0:
        recommendations.append(Recommendation(
            id=f"rec_{rec_counter}",
            category="duplicate_rows",
            title="Deduplicate Row Records",
            impact="Reduces model overfitting and removes redundant data points.",
            suggested_action="Apply `df.drop_duplicates(inplace=True)`.",
            priority="high"
        ))
        code_lines.append("# Drop duplicate rows")
        code_lines.append("df_clean.drop_duplicates(inplace=True)")
        code_lines.append("")
        rec_counter += 1

    if report.summary.total_missing_cells > 0:
        recommendations.append(Recommendation(
            id=f"rec_{rec_counter}",
            category="missing_values",
            title="Impute or Drop Missing Values",
            impact="Prevents missing value errors during model training.",
            suggested_action="Impute numeric columns with median, categorical columns with mode or 'Missing'.",
            priority="high"
        ))
        code_lines.append("# Fill missing values for numerical and categorical columns")
        code_lines.append("for col in df_clean.columns:")
        code_lines.append("    if df_clean[col].dtype in ['int64', 'float64']:")
        code_lines.append("        df_clean[col].fillna(df_clean[col].median(), inplace=True)")
        code_lines.append("    else:")
        code_lines.append("        df_clean[col].fillna('Missing', inplace=True)")
        code_lines.append("")
        rec_counter += 1

    if report.summary.total_outliers > 0:
        recommendations.append(Recommendation(
            id=f"rec_{rec_counter}",
            category="outliers",
            title="Cap Statistical Outliers using IQR Bounds",
            impact="Prevents skewed gradient updates and extreme loss values.",
            suggested_action="Apply IQR capping (winsorization) to numerical features.",
            priority="medium"
        ))
        code_lines.append("# Cap numerical outliers using IQR method")
        code_lines.append("num_cols = df_clean.select_dtypes(include=[np.number]).columns")
        code_lines.append("for col in num_cols:")
        code_lines.append("    q1 = df_clean[col].quantile(0.25)")
        code_lines.append("    q3 = df_clean[col].quantile(0.75)")
        code_lines.append("    iqr = q3 - q1")
        code_lines.append("    lower_bound = q1 - 1.5 * iqr")
        code_lines.append("    upper_bound = q3 + 1.5 * iqr")
        code_lines.append("    df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)")
        code_lines.append("")
        rec_counter += 1

    code_lines.append("# Save cleaned dataset")
    code_lines.append(f"df_clean.to_csv('cleaned_{report.filename}', index=False)")
    code_lines.append("print('Dataset cleaning completed successfully!')")

    return AIAnalysisResponse(
        dataset_id=dataset_id,
        health_summary=health_summary,
        explanation=explanation,
        recommendations=recommendations,
        python_code="\n".join(code_lines)
    )

import json
from backend.schemas.audit import AuditReport

def build_gemini_prompt(report: AuditReport) -> str:
    """
    Constructs a structured prompt for Gemini 2.5 Flash using ONLY the JSON Audit Report.
    The raw CSV data is NEVER passed to Gemini.
    """
    report_dict = report.model_dump()

    prompt = f"""
You are an expert AI Data Scientist and Dataset Quality Engineer.
Analyze the following structured dataset audit report JSON and generate executive quality reasoning, actionable cleaning recommendations, and an executable Python Pandas script.

CRITICAL CONSTRAINTS:
1. Base your reasoning ONLY on the provided JSON audit report.
2. Return a valid JSON object matching the exact schema specified below.
3. The generated `python_code` must be a self-contained, fully working Python script using `pandas` and `numpy` that loads the dataset, cleans missing values, handles duplicates, addresses data type inconsistencies, and fixes statistical outliers.

JSON AUDIT REPORT:
{json.dumps(report_dict, indent=2)}

EXPECTED OUTPUT JSON STRUCTURE (Return ONLY valid JSON):
{{
  "dataset_id": "{report.dataset_id}",
  "health_summary": "High level executive summary of dataset readiness (2-3 sentences).",
  "explanation": "Detailed explanation of detected quality flaws (missing values, duplicates, outliers, etc.) and their impact on ML model training.",
  "recommendations": [
    {{
      "id": "rec_1",
      "category": "missing_values",
      "title": "Clear recommendation title",
      "impact": "Explanation of ML/data impact",
      "suggested_action": "Specific pandas cleaning technique to apply",
      "priority": "high"
    }}
  ],
  "python_code": "# Complete executable pandas cleaning script\\nimport pandas as pd\\nimport numpy as np\\n..."
}}
"""
    return prompt

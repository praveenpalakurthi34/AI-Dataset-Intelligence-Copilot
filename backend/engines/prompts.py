import json
from backend.schemas.audit import AuditReport


def build_ai_prompt(report: AuditReport) -> str:
    """
    Constructs a structured prompt for Featherless AI.

    IMPORTANT:
    - Only the structured AuditReport JSON is sent.
    - The raw CSV is NEVER sent to the LLM.
    """

    report_dict = report.model_dump()

    prompt = f"""
You are a Senior AI Data Quality Engineer, Machine Learning Engineer, and Data Governance Expert.

Your task is to analyze ONLY the provided dataset audit report.

The dataset itself is NOT available.
DO NOT assume any information outside the supplied JSON.

==================================================
OBJECTIVES
==================================================

1. Evaluate the overall health of the dataset.

2. Explain the major data quality issues.

3. Recommend practical data-cleaning actions.

4. Generate an executable Pandas cleaning script.

==================================================
STRICT RULES
==================================================

• Base every statement ONLY on the supplied JSON.

• Never invent statistics.

• Never fabricate columns.

• Never reference information not present.

• Return ONLY valid JSON.

• Do NOT wrap the response inside markdown.

• Do NOT use ```json.

==================================================
AUDIT REPORT JSON
==================================================

{json.dumps(report_dict, indent=2)}

==================================================
OUTPUT JSON SCHEMA
==================================================

{{
  "dataset_id": "{report.dataset_id}",

  "health_summary": "2-3 sentence executive summary.",

  "explanation": "Detailed explanation of the detected quality issues and their impact on analytics and ML.",

  "recommendations":
  [
    {{
      "id": "rec_1",

      "category": "missing_values",

      "title": "Recommendation title",

      "impact": "Business/ML impact.",

      "suggested_action": "Specific Pandas cleaning action.",

      "priority": "high"
    }}
  ],

  "python_code":
"import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('<filename>')

# Cleaning code

df.to_csv('cleaned_dataset.csv', index=False)"
}}

==================================================
REQUIREMENTS FOR RECOMMENDATIONS
==================================================

Each recommendation should:

• Clearly identify the issue.

• Explain why it matters.

• Suggest one practical cleaning method.

• Assign a priority:
    - high
    - medium
    - low

==================================================
REQUIREMENTS FOR PYTHON CODE
==================================================

The generated code should:

• Import pandas and numpy.

• Read the dataset.

• Remove duplicate rows.

• Handle missing values.

• Correct invalid data types when applicable.

• Handle outliers using IQR capping.

• Save the cleaned dataset.

The code should be executable without modification.

Return ONLY valid JSON.
"""

    return prompt
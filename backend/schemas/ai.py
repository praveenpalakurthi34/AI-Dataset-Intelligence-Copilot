from pydantic import BaseModel, Field
from typing import List


class Decision(BaseModel):
    """
    AI decision generated from the audit report.

    The AI should make an actionable decision instead of merely providing
    recommendations.
    """

    decision: str = Field(
        ...,
        description="Action decided by the AI."
    )

    target: str = Field(
        ...,
        description="Column or dataset element the decision applies to."
    )

    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="AI confidence score (0-100)."
    )

    reason: str = Field(
        ...,
        description="Reason behind the decision."
    )

    expected_impact: str = Field(
        ...,
        description="Expected improvement after applying the decision."
    )

    auto_fix: bool = Field(
        default=True,
        description="Whether this decision can be automatically executed."
    )


class AIAnalysisResponse(BaseModel):
    """
    Final AI analysis returned to the frontend.
    """

    dataset_id: str

    health_summary: str

    explanation: str

    decisions: List[Decision]

    python_code: str
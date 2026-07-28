from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    id: str
    category: str
    title: str
    impact: str
    suggested_action: str
    priority: str  # high, medium, low

class AIAnalysisResponse(BaseModel):
    dataset_id: str
    health_summary: str
    explanation: str
    recommendations: List[Recommendation]
    python_code: str

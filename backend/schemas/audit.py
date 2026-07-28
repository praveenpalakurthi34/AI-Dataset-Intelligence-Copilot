from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.schemas.dataset import DatasetMetadata

class QualityIssue(BaseModel):
    category: str  # missing_values, duplicate_rows, type_inconsistency, outliers
    severity: str  # low, medium, high, critical
    column: Optional[str] = None
    title: str
    description: str
    affected_count: int
    affected_percentage: float

class ReadinessScoreBreakdown(BaseModel):
    completeness_score: float   # Based on missing values
    uniqueness_score: float     # Based on duplicate rows
    type_validity_score: float  # Based on data type consistency
    outlier_score: float        # Based on statistical outliers

class ReadinessScore(BaseModel):
    overall_score: float
    grade: str                  # A, B, C, D, F
    status: str                 # Ready, Minor Issues, Action Required, Critical Issues
    breakdown: ReadinessScoreBreakdown

class ColumnSummary(BaseModel):
    column_name: str
    data_type: str
    missing_count: int
    missing_pct: float
    unique_count: int
    outlier_count: int
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean_value: Optional[Any] = None
    std_value: Optional[Any] = None

class DatasetSummary(BaseModel):
    total_rows: int
    total_columns: int
    total_missing_cells: int
    total_missing_pct: float
    total_duplicate_rows: int
    total_duplicate_pct: float
    total_outliers: int
    column_summaries: List[ColumnSummary]

class AuditReport(BaseModel):
    dataset_id: str
    filename: str
    analyzed_at: str
    metadata: DatasetMetadata
    summary: DatasetSummary
    readiness_score: ReadinessScore
    issues: List[QualityIssue]

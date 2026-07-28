from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    file_size_bytes: int
    uploaded_at: str
    message: str

class ColumnMetadata(BaseModel):
    name: str
    data_type: str
    inferred_type: str
    non_null_count: int
    null_count: int
    null_percentage: float
    unique_count: int
    sample_values: List[Any]

class DatasetMetadata(BaseModel):
    filename: str
    total_rows: int
    total_columns: int
    file_size_bytes: int
    memory_usage_bytes: int
    columns: List[ColumnMetadata]

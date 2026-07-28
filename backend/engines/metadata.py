import pandas as pd
import numpy as np
from pathlib import Path
from typing import List
from backend.schemas.dataset import DatasetMetadata, ColumnMetadata

def extract_metadata(df: pd.DataFrame, filename: str, file_size_bytes: int) -> DatasetMetadata:
    """
    Extracts comprehensive metadata from a pandas DataFrame.
    """
    total_rows, total_cols = df.shape
    memory_usage = int(df.memory_usage(deep=True).sum())
    
    columns_meta: List[ColumnMetadata] = []
    
    for col in df.columns:
        series = df[col]
        null_count = int(series.isnull().sum())
        non_null_count = total_rows - null_count
        null_pct = round((null_count / total_rows * 100), 2) if total_rows > 0 else 0.0
        unique_count = int(series.nunique(dropna=True))
        
        # Sample non-null values (convert numpy types to python native types)
        sample_vals = series.dropna().head(3).tolist()
        sample_vals_cleaned = [
            int(x) if isinstance(x, (np.integer, int)) else
            float(x) if isinstance(x, (np.floating, float)) else
            str(x) for x in sample_vals
        ]
        
        # Infer type
        raw_type = str(series.dtype)
        if pd.api.types.is_numeric_dtype(series):
            inferred_type = "Numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            inferred_type = "Datetime"
        elif pd.api.types.is_bool_dtype(series):
            inferred_type = "Boolean"
        else:
            inferred_type = "Categorical / Text"
            
        columns_meta.append(ColumnMetadata(
            name=str(col),
            data_type=raw_type,
            inferred_type=inferred_type,
            non_null_count=non_null_count,
            null_count=null_count,
            null_percentage=null_pct,
            unique_count=unique_count,
            sample_values=sample_vals_cleaned
        ))
        
    return DatasetMetadata(
        filename=filename,
        total_rows=total_rows,
        total_columns=total_cols,
        file_size_bytes=file_size_bytes,
        memory_usage_bytes=memory_usage,
        columns=columns_meta
    )

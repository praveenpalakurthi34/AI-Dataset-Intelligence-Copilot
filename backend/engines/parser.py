import pandas as pd
from pathlib import Path
from typing import Tuple

def load_csv_dataset(file_path: Path) -> Tuple[pd.DataFrame, str]:
    """
    Loads a CSV file with automatic encoding fallback handling.
    Returns (DataFrame, used_encoding).
    """
    encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "iso-8859-1", "cp1252"]
    
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df, encoding
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
            
    # Final fallback attempt with engine python
    try:
        df = pd.read_csv(file_path, encoding="latin1", engine="python")
        return df, "latin1"
    except Exception as e:
        raise ValueError(f"Failed to parse CSV file: {str(e)}")

import pandas as pd
import numpy as np
from typing import List, Tuple
from backend.schemas.audit import QualityIssue, ColumnSummary, DatasetSummary

def detect_missing_values(df: pd.DataFrame) -> List[QualityIssue]:
    issues = []
    total_rows = len(df)
    if total_rows == 0:
        return issues

    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        if null_count > 0:
            null_pct = round((null_count / total_rows * 100), 2)
            if null_pct > 50:
                severity = "critical"
            elif null_pct > 20:
                severity = "high"
            elif null_pct > 5:
                severity = "medium"
            else:
                severity = "low"

            issues.append(QualityIssue(
                category="missing_values",
                severity=severity,
                column=str(col),
                title=f"Missing Values in '{col}'",
                description=f"Column '{col}' has {null_count} missing value(s) ({null_pct}% of total rows).",
                affected_count=null_count,
                affected_percentage=null_pct
            ))
    return issues


def detect_duplicates(df: pd.DataFrame) -> Tuple[List[QualityIssue], int, float]:
    total_rows = len(df)
    if total_rows == 0:
        return [], 0, 0.0

    dup_count = int(df.duplicated().sum())
    dup_pct = round((dup_count / total_rows * 100), 2)
    issues = []

    if dup_count > 0:
        if dup_pct > 20:
            severity = "critical"
        elif dup_pct > 10:
            severity = "high"
        elif dup_pct > 2:
            severity = "medium"
        else:
            severity = "low"

        issues.append(QualityIssue(
            category="duplicate_rows",
            severity=severity,
            column=None,
            title="Duplicate Rows Detected",
            description=f"Dataset contains {dup_count} exact duplicate row(s) ({dup_pct}% of total rows).",
            affected_count=dup_count,
            affected_percentage=dup_pct
        ))

    return issues, dup_count, dup_pct


def detect_type_inconsistencies(df: pd.DataFrame) -> List[QualityIssue]:
    issues = []
    total_rows = len(df)
    if total_rows == 0:
        return issues

    for col in df.columns:
        series = df[col].dropna()
        if series.empty:
            continue

        # Check for constant column (zero variance / 1 unique value)
        if series.nunique() == 1:
            issues.append(QualityIssue(
                category="type_inconsistency",
                severity="medium",
                column=str(col),
                title=f"Constant Column '{col}'",
                description=f"Column '{col}' has only 1 unique value across all rows and provides zero predictive variance.",
                affected_count=total_rows,
                affected_percentage=100.0
            ))

        # Check if object column contains numeric strings
        if series.dtype == "object":
            numeric_converted = pd.to_numeric(series, errors="coerce")
            num_valid = numeric_converted.notnull().sum()
            num_ratio = num_valid / len(series)
            if 0.5 < num_ratio < 1.0:
                issues.append(QualityIssue(
                    category="type_inconsistency",
                    severity="high",
                    column=str(col),
                    title=f"Mixed Data Types in '{col}'",
                    description=f"Column '{col}' is stored as string/object but {round(num_ratio*100, 1)}% of non-null entries are numeric.",
                    affected_count=int(num_valid),
                    affected_percentage=round(num_ratio * 100, 2)
                ))

    return issues


def detect_outliers_iqr(df: pd.DataFrame) -> Tuple[List[QualityIssue], int, dict]:
    """
    Detects statistical outliers on numerical columns using the Interquartile Range (IQR) method.
    Returns (issues_list, total_outliers_count, outliers_per_column_dict).
    """
    issues = []
    total_outliers = 0
    outliers_per_col = {}
    total_rows = len(df)
    if total_rows == 0:
        return issues, 0, {}

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 5:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers_mask = (series < lower_bound) | (series > upper_bound)
        outlier_count = int(outliers_mask.sum())
        outliers_per_col[str(col)] = outlier_count

        if outlier_count > 0:
            total_outliers += outlier_count
            outlier_pct = round((outlier_count / total_rows * 100), 2)

            if outlier_pct > 15:
                severity = "high"
            elif outlier_pct > 5:
                severity = "medium"
            else:
                severity = "low"

            issues.append(QualityIssue(
                category="outliers",
                severity=severity,
                column=str(col),
                title=f"Statistical Outliers in '{col}'",
                description=f"Column '{col}' contains {outlier_count} IQR outlier(s) ({outlier_pct}% of rows). Bounds: [{round(lower_bound, 2)}, {round(upper_bound, 2)}].",
                affected_count=outlier_count,
                affected_percentage=outlier_pct
            ))

    return issues, total_outliers, outliers_per_col


def build_dataset_summary(df: pd.DataFrame, dup_count: int, dup_pct: float, total_outliers: int, outliers_per_col: dict) -> DatasetSummary:
    total_rows, total_cols = df.shape
    total_cells = total_rows * total_cols if total_rows > 0 and total_cols > 0 else 1
    total_missing_cells = int(df.isnull().sum().sum())
    total_missing_pct = round((total_missing_cells / total_cells * 100), 2)

    col_summaries: List[ColumnSummary] = []
    for col in df.columns:
        series = df[col]
        missing_cnt = int(series.isnull().sum())
        missing_pct = round((missing_cnt / total_rows * 100), 2) if total_rows > 0 else 0.0
        uniq_cnt = int(series.nunique(dropna=True))
        outlier_cnt = outliers_per_col.get(str(col), 0)

        min_val, max_val, mean_val, std_val = None, None, None, None
        if pd.api.types.is_numeric_dtype(series) and not series.dropna().empty:
            min_val = float(series.min()) if not pd.isna(series.min()) else None
            max_val = float(series.max()) if not pd.isna(series.max()) else None
            mean_val = float(series.mean()) if not pd.isna(series.mean()) else None
            std_val = float(series.std()) if not pd.isna(series.std()) else None

        col_summaries.append(ColumnSummary(
            column_name=str(col),
            data_type=str(series.dtype),
            missing_count=missing_cnt,
            missing_pct=missing_pct,
            unique_count=uniq_cnt,
            outlier_count=outlier_cnt,
            min_value=min_val,
            max_value=max_val,
            mean_value=mean_val,
            std_value=std_val
        ))

    return DatasetSummary(
        total_rows=total_rows,
        total_columns=total_cols,
        total_missing_cells=total_missing_cells,
        total_missing_pct=total_missing_pct,
        total_duplicate_rows=dup_count,
        total_duplicate_pct=dup_pct,
        total_outliers=total_outliers,
        column_summaries=col_summaries
    )

from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

import numpy as np
import pandas as pd

from backend.schemas.audit import AuditReport


# ==========================================================
# AUTO FIX RESULT
# ==========================================================

@dataclass
class AutoFixResult:

    success: bool

    output_file: str

    statistics: Dict[str, Any]

    message: str


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _numeric_columns(df: pd.DataFrame):

    return df.select_dtypes(
        include=[np.number]
    ).columns.tolist()


def _categorical_columns(df: pd.DataFrame):

    return df.select_dtypes(
        exclude=[np.number]
    ).columns.tolist()


def _safe_mode(series):

    mode = series.mode()

    if len(mode):

        return mode.iloc[0]

    return None


# ==========================================================
# MAIN ENTRY POINT
# ==========================================================

def apply_auto_fix(

    df: pd.DataFrame,

    report: AuditReport,

    output_directory: str = "outputs",

) -> AutoFixResult:
    """
    Automatically cleans the uploaded dataset
    using the Audit Report.

    Cleaning Steps

    1 Remove duplicate rows

    2 Fill missing values

    3 Correct datatypes

    4 Cap outliers

    5 Save cleaned dataset

    Returns

    AutoFixResult
    """

    df_clean = df.copy()

    Path(output_directory).mkdir(
        parents=True,
        exist_ok=True,
    )

    stats = {

        "rows_before": len(df),

        "rows_after": len(df),

        "duplicates_removed": 0,

        "missing_values_fixed": 0,

        "outliers_capped": 0,

        "datatype_conversions": 0,

        "constant_columns_removed": 0,

    }
        # ==========================================================
    # REMOVE DUPLICATE ROWS
    # ==========================================================

    duplicate_count = int(df_clean.duplicated().sum())

    if duplicate_count > 0:

        df_clean.drop_duplicates(inplace=True)

        stats["duplicates_removed"] = duplicate_count

        stats["rows_after"] = len(df_clean)

    # ==========================================================
    # HANDLE MISSING VALUES
    # ==========================================================

    missing_before = int(df_clean.isna().sum().sum())

    if missing_before > 0:

        # -------------------------------
        # Numeric Columns
        # -------------------------------

        for column in _numeric_columns(df_clean):

            if df_clean[column].isna().sum() == 0:
                continue

            median = df_clean[column].median()

            df_clean[column] = df_clean[column].fillna(
                median
            )

        # -------------------------------
        # Categorical Columns
        # -------------------------------

        for column in _categorical_columns(df_clean):

            if df_clean[column].isna().sum() == 0:
                continue

            mode = _safe_mode(df_clean[column])

            if mode is not None:

                df_clean[column] = df_clean[column].fillna(
                    mode
                )

        missing_after = int(
            df_clean.isna().sum().sum()
        )

        stats["missing_values_fixed"] = (
            missing_before - missing_after
        )
            # ==========================================================
    # AUTOMATIC DATA TYPE CORRECTION
    # ==========================================================

    for column in df_clean.columns:

        # Skip if already numeric
        if pd.api.types.is_numeric_dtype(df_clean[column]):
            continue

        # Skip if datetime
        if pd.api.types.is_datetime64_any_dtype(df_clean[column]):
            continue

        # Try numeric conversion
        try:

            converted = pd.to_numeric(
                df_clean[column],
                errors="raise"
            )

            if not converted.equals(df_clean[column]):

                df_clean[column] = converted

                stats["datatype_conversions"] += 1

                continue

        except Exception:
            pass

        # Try datetime conversion
        try:

            converted = pd.to_datetime(
                df_clean[column],
                errors="raise"
            )

            df_clean[column] = converted

            stats["datatype_conversions"] += 1

        except Exception:
            pass

    # ==========================================================
    # REMOVE CONSTANT COLUMNS
    # ==========================================================

    constant_columns = []

    for column in df_clean.columns:

        unique_count = df_clean[column].nunique(dropna=False)

        if unique_count <= 1:

            constant_columns.append(column)

    if constant_columns:

        df_clean.drop(
            columns=constant_columns,
            inplace=True,
            errors="ignore"
        )

        stats["constant_columns_removed"] = len(
            constant_columns
        )
            # ==========================================================
    # OUTLIER CAPPING (IQR METHOD)
    # ==========================================================

    numeric_columns = _numeric_columns(df_clean)

    total_capped = 0

    for column in numeric_columns:

        series = df_clean[column]

        # Ignore columns with insufficient data
        if series.dropna().shape[0] < 5:
            continue

        q1 = series.quantile(0.25)

        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if pd.isna(iqr) or iqr == 0:
            continue

        lower_bound = q1 - (1.5 * iqr)

        upper_bound = q3 + (1.5 * iqr)

        below_mask = series < lower_bound

        above_mask = series > upper_bound

        capped_count = int(
            below_mask.sum() + above_mask.sum()
        )

        if capped_count == 0:
            continue

        df_clean[column] = series.clip(
            lower=lower_bound,
            upper=upper_bound
        )

        total_capped += capped_count

    stats["outliers_capped"] = total_capped

    # ==========================================================
    # FINAL CLEANING SUMMARY
    # ==========================================================

    stats["rows_after"] = len(df_clean)

    stats["columns_after"] = len(df_clean.columns)

    stats["remaining_missing_values"] = int(
        df_clean.isna().sum().sum()
    )

    stats["remaining_duplicates"] = int(
        df_clean.duplicated().sum()
    )
        # ==========================================================
    # APPLY AI DECISIONS (OPTIONAL)
    # ==========================================================

    applied_decisions = []

    try:

        if hasattr(report, "ai_analysis"):

            analysis = report.ai_analysis

            if analysis and hasattr(analysis, "decisions"):

                for decision in analysis.decisions:

                    if getattr(decision, "auto_fix", False):

                        applied_decisions.append({

                            "decision": decision.decision,

                            "target": decision.target,

                            "confidence": decision.confidence

                        })

    except Exception:

        # Auto Fix should never fail because
        # AI decisions are unavailable.
        pass

    stats["applied_decisions"] = applied_decisions

    # ==========================================================
    # DATASET QUALITY SUMMARY
    # ==========================================================

    rows_removed = (
        stats["rows_before"] -
        stats["rows_after"]
    )

    stats["rows_removed"] = rows_removed

    stats["quality_summary"] = {

        "duplicates_removed":
            stats["duplicates_removed"],

        "missing_values_fixed":
            stats["missing_values_fixed"],

        "outliers_capped":
            stats["outliers_capped"],

        "datatype_conversions":
            stats["datatype_conversions"],

        "constant_columns_removed":
            stats["constant_columns_removed"],

        "remaining_missing_values":
            stats["remaining_missing_values"],

        "remaining_duplicates":
            stats["remaining_duplicates"]

    }

    # ==========================================================
    # DETERMINE OUTPUT FILE
    # ==========================================================

    filename = report.filename

    if filename.lower().endswith(".csv"):

        cleaned_name = (
            filename[:-4] +
            "_cleaned.csv"
        )

    else:

        cleaned_name = (
            filename +
            "_cleaned.csv"
        )

    output_path = (
        Path(output_directory) /
        cleaned_name
    )
        # ==========================================================
    # SAVE CLEANED DATASET
    # ==========================================================

    try:

        df_clean.to_csv(

            output_path,

            index=False,

        )

    except Exception as e:

        return AutoFixResult(

            success=False,

            output_file="",

            statistics=stats,

            message=f"Unable to save cleaned dataset: {str(e)}",

        )

    # ==========================================================
    # VERIFY OUTPUT
    # ==========================================================

    if not output_path.exists():

        return AutoFixResult(

            success=False,

            output_file="",

            statistics=stats,

            message="Cleaned dataset could not be created.",

        )

    file_size = output_path.stat().st_size

    stats["output_file_size_bytes"] = file_size

    stats["output_file_name"] = output_path.name

    stats["output_directory"] = str(output_path.parent)

    stats["columns_after"] = len(df_clean.columns)

    stats["rows_after"] = len(df_clean)

    # ==========================================================
    # CLEANING SUCCESS MESSAGE
    # ==========================================================

    message = (

        "Dataset cleaned successfully. "

        f"{stats['duplicates_removed']} duplicate rows removed, "

        f"{stats['missing_values_fixed']} missing values fixed, "

        f"{stats['outliers_capped']} outliers capped."

    )
        # ==========================================================
    # RETURN RESULT
    # ==========================================================

    return AutoFixResult(

        success=True,

        output_file=str(output_path),

        statistics=stats,

        message=message,

    )


# ==========================================================
# FILE-BASED WRAPPER
# ==========================================================

def apply_auto_fix_from_file(
    file_path: str,
    report: AuditReport,
    output_directory: str = "outputs",
) -> AutoFixResult:
    """
    Convenience wrapper used by the API.

    Parameters
    ----------
    file_path : str
        Path to the uploaded CSV.

    report : AuditReport
        Audit generated by the auditor.

    output_directory : str
        Folder where cleaned dataset is stored.

    Returns
    -------
    AutoFixResult
    """

    df = pd.read_csv(file_path)

    return apply_auto_fix(
        df=df,
        report=report,
        output_directory=output_directory,
    )


# ==========================================================
# DOWNLOAD INFORMATION
# ==========================================================

def get_download_information(
    result: AutoFixResult,
) -> Dict[str, Any]:
    """
    Converts AutoFixResult into a JSON-friendly
    dictionary for the frontend.
    """

    return {

        "success": result.success,

        "message": result.message,

        "download_file": result.output_file,

        "statistics": result.statistics,

    }


# ==========================================================
# SIMPLE HEALTH CHECK
# ==========================================================

def validate_cleaned_dataset(
    file_path: str,
) -> Dict[str, Any]:
    """
    Performs lightweight validation on the cleaned dataset.
    """

    df = pd.read_csv(file_path)

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing_values": int(
            df.isna().sum().sum()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "numeric_columns": len(
            df.select_dtypes(include=[np.number]).columns
        ),

        "categorical_columns": len(
            df.select_dtypes(exclude=[np.number]).columns
        ),

    }



from backend.schemas.audit import (
    ReadinessScore,
    ReadinessScoreBreakdown
)


def calculate_readiness_score(
    total_missing_pct: float,
    duplicate_pct: float,
    type_issue_count: int,
    total_outliers: int,
    total_rows: int,
    total_columns: int
) -> ReadinessScore:
    """
    Calculates the overall dataset readiness score.

    The scoring model is intentionally stricter than the original one
    so that dirty datasets do not receive unrealistically high scores.
    """

    # ==========================================================
    # COMPLETENESS SCORE
    # ==========================================================

    # Penalize missing values aggressively
    completeness_score = max(
        0.0,
        100 - (total_missing_pct * 2.0)
    )

    # ==========================================================
    # UNIQUENESS SCORE
    # ==========================================================

    # Duplicate rows heavily affect ML quality
    uniqueness_score = max(
        0.0,
        100 - (duplicate_pct * 6.0)
    )

    # ==========================================================
    # OUTLIER SCORE
    # ==========================================================

    if total_rows > 0:
        outlier_pct = (total_outliers / total_rows) * 100
    else:
        outlier_pct = 0

    outlier_score = max(
        70.0,
        100 - (outlier_pct * 0.5)
    )

    # ==========================================================
    # TYPE VALIDITY SCORE
    # ==========================================================

    # Mixed datatypes / constant columns
    type_validity_score = max(
        0.0,
        100 - (type_issue_count * 10.0)
    )

    # ==========================================================
    # OVERALL SCORE
    # ==========================================================

    overall_score = (
        completeness_score * 0.40 +
        uniqueness_score * 0.35 +
        outlier_score * 0.05 +
        type_validity_score * 0.20
    )

    # ==========================================================
    # EXTRA GLOBAL PENALTIES
    # ==========================================================

    # These penalties prevent dirty datasets from receiving A grades.

    overall_score -= total_missing_pct * 0.50
    overall_score -= duplicate_pct * 0.80
    overall_score -= type_issue_count * 2

    if total_rows > 0:
        overall_score -= (total_outliers / total_rows) * 100 * 0.50

    overall_score = round(max(0.0, min(100.0, overall_score)), 1)

    # ==========================================================
    # GRADE
    # ==========================================================

    if overall_score >= 90:
        grade = "A"
        status = "Ready for Production / ML"

    elif overall_score >= 80:
        grade = "B"
        status = "Minor Cleaning Required"

    elif overall_score >= 70:
        grade = "C"
        status = "Moderate Cleaning Required"

    elif overall_score >= 60:
        grade = "D"
        status = "Extensive Cleaning Required"

    else:
        grade = "F"
        status = "Not Suitable for ML"

    # ==========================================================
    # RETURN
    # ==========================================================

    return ReadinessScore(
        overall_score=overall_score,
        grade=grade,
        status=status,
        breakdown=ReadinessScoreBreakdown(
            completeness_score=round(completeness_score, 1),
            uniqueness_score=round(uniqueness_score, 1),
            type_validity_score=round(type_validity_score, 1),
            outlier_score=round(outlier_score, 1)
        )
    )
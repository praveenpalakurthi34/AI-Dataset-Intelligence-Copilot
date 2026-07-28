from backend.schemas.audit import ReadinessScore, ReadinessScoreBreakdown

def calculate_readiness_score(
    total_missing_pct: float,
    duplicate_pct: float,
    type_issue_count: int,
    total_outliers: int,
    total_rows: int,
    total_columns: int
) -> ReadinessScore:
    """
    Computes a deterministic, weighted Dataset Readiness Score (0-100).
    """
    # 1. Completeness Score (35% weight)
    completeness = max(0.0, 100.0 - (total_missing_pct * 2.5))

    # 2. Uniqueness Score (25% weight)
    uniqueness = max(0.0, 100.0 - (duplicate_pct * 3.0))

    # 3. Type Validity Score (20% weight)
    type_penalty = min(100.0, type_issue_count * 15.0)
    type_validity = max(0.0, 100.0 - type_penalty)

    # 4. Outlier Score (20% weight)
    total_numeric_cells = max(1, total_rows * total_columns)
    outlier_ratio = total_outliers / total_numeric_cells
    outlier_score = max(0.0, 100.0 - (outlier_ratio * 100.0 * 2.0))

    # Weighted Overall Score
    overall = round(
        (completeness * 0.35) +
        (uniqueness * 0.25) +
        (type_validity * 0.20) +
        (outlier_score * 0.20),
        1
    )

    # Grade determination
    if overall >= 90.0:
        grade = "A"
        status = "Ready for Production / ML"
    elif overall >= 75.0:
        grade = "B"
        status = "Minor Issues Detected"
    elif overall >= 60.0:
        grade = "C"
        status = "Action Required"
    elif overall >= 45.0:
        grade = "D"
        status = "Significant Quality Defects"
    else:
        grade = "F"
        status = "Critical Dataset Flaws"

    breakdown = ReadinessScoreBreakdown(
        completeness_score=round(completeness, 1),
        uniqueness_score=round(uniqueness, 1),
        type_validity_score=round(type_validity, 1),
        outlier_score=round(outlier_score, 1)
    )

    return ReadinessScore(
        overall_score=overall,
        grade=grade,
        status=status,
        breakdown=breakdown
    )

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.engines.parser import load_csv_dataset
from backend.engines.metadata import extract_metadata
from backend.engines.auditor import detect_missing_values, detect_duplicates, detect_outliers_iqr
from backend.engines.readiness import calculate_readiness_score

client = TestClient(app)
SAMPLE_CSV = Path(__file__).resolve().parent.parent.parent / "datasets" / "sample_housing.csv"

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_parser_and_metadata():
    df, encoding = load_csv_dataset(SAMPLE_CSV)
    assert not df.empty
    assert len(df) == 10
    
    metadata = extract_metadata(df, filename="sample_housing.csv", file_size_bytes=1000)
    assert metadata.total_rows == 10
    assert metadata.total_columns == 7

def test_auditor_detectors():
    df, _ = load_csv_dataset(SAMPLE_CSV)
    missing_issues = detect_missing_values(df)
    assert len(missing_issues) > 0  # square_feet, num_bedrooms, price have missing values

    dup_issues, dup_count, dup_pct = detect_duplicates(df)
    assert dup_count == 2  # Row 1 duplicated twice

    outlier_issues, total_outliers, _ = detect_outliers_iqr(df)
    assert total_outliers > 0  # Row 6 has 50000 sq ft & 95m price

def test_readiness_score():
    score = calculate_readiness_score(
        total_missing_pct=10.0,
        duplicate_pct=20.0,
        type_issue_count=1,
        total_outliers=2,
        total_rows=10,
        total_columns=7
    )
    assert 0.0 <= score.overall_score <= 100.0
    assert score.grade in ["A", "B", "C", "D", "F"]

def test_end_to_end_upload_and_analyze():
    with open(SAMPLE_CSV, "rb") as f:
        response = client.post("/api/upload", files={"file": ("sample_housing.csv", f, "text/csv")})
    
    assert response.status_code == 200
    data = response.json()
    dataset_id = data["dataset_id"]
    assert dataset_id is not None

    # Test analyze API
    analyze_resp = client.post(f"/api/analyze/{dataset_id}")
    assert analyze_resp.status_code == 200
    report = analyze_resp.json()
    assert report["dataset_id"] == dataset_id
    assert report["metadata"]["total_rows"] == 10
    assert report["readiness_score"]["overall_score"] > 0
    assert len(report["issues"]) > 0

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
SAMPLE_CSV = Path(__file__).resolve().parent.parent.parent / "datasets" / "sample_housing.csv"

def run_full_system_test():
    print("==================================================")
    print("  AI DATASET INTELLIGENCE COPILOT - E2E AUDIT TEST")
    print("==================================================")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200
    print("1. [PASS] API Health Check")

    # 2. Upload CSV
    with open(SAMPLE_CSV, "rb") as f:
        res = client.post("/api/upload", files={"file": ("sample_housing.csv", f, "text/csv")})
    assert res.status_code == 200
    upload_data = res.json()
    dataset_id = upload_data["dataset_id"]
    print(f"2. [PASS] Upload CSV -> dataset_id: {dataset_id}")

    # 3. Analyze Dataset (Module 1: Dataset Analysis Engine)
    res = client.post(f"/api/analyze/{dataset_id}")
    assert res.status_code == 200
    audit = res.json()
    score = audit["readiness_score"]["overall_score"]
    issues_cnt = len(audit["issues"])
    print(f"3. [PASS] Dataset Analysis Engine -> Readiness Score: {score}/100 | Issues: {issues_cnt}")

    # 4. AI Reasoning Service (Module 2: AI Engine)
    res = client.post(f"/api/analyze-ai/{dataset_id}")
    assert res.status_code == 200
    ai = res.json()
    assert ai["python_code"] != ""
    print(f"4. [PASS] AI Reasoning Service -> Code generated ({len(ai['python_code'].splitlines())} lines)")

    # 5. History API (SQLite Storage)
    res = client.get("/api/history")
    assert res.status_code == 200
    history_list = res.json()
    assert len(history_list) > 0
    print(f"5. [PASS] SQLite History API -> Found {len(history_list)} audit record(s)")

    # 6. PDF Export Engine (Module 3: Report Engine)
    res = client.get(f"/api/dataset/{dataset_id}/export-pdf")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 1000
    print(f"6. [PASS] PDF Report Engine -> Generated {len(res.content)} bytes PDF")

    print("\nALL E2E SYSTEM TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_full_system_test()

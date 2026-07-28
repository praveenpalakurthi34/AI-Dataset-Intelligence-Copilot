import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.tests.test_phase1 import (
    test_health_check,
    test_parser_and_metadata,
    test_auditor_detectors,
    test_readiness_score,
    test_end_to_end_upload_and_analyze
)

if __name__ == "__main__":
    print("Running Phase 1 Backend Verification Tests...")
    test_health_check()
    print("[PASS] test_health_check")
    test_parser_and_metadata()
    print("[PASS] test_parser_and_metadata")
    test_auditor_detectors()
    print("[PASS] test_auditor_detectors")
    test_readiness_score()
    print("[PASS] test_readiness_score")
    test_end_to_end_upload_and_analyze()
    print("[PASS] test_end_to_end_upload_and_analyze")
    print("ALL PHASE 1 BACKEND TESTS PASSED SUCCESSFULLY!")

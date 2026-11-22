<<<<<<< HEAD
# Proactive Insights Full-Coverage Demo

Synthetic FastAPI test fixture for Blitzy Proactive Insights.

## Test layers
- `tests/unit/`: isolated service and validation tests
- `tests/integration/`: API/auth/persistence integration tests
- `tests/e2e/`: complete user workflow
- `tests/non_functional/`: security, resilience, and response-time checks

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

Run tests with `pytest -q`.

## Scan
Connect the repository root, select `main`, and initially leave the environment unset.

This is a synthetic QA fixture, not production software. It uses in-memory storage and demo credentials. Do not deploy it or use real credentials.
=======
# proactive_insights_full_coverage_demo
>>>>>>> 2eee6fee99de85ca7200483f3ee6b9a2349215af

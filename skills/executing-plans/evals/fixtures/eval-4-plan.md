# Cache Hit Counter Plan

**Goal:** Add a runnable endpoint to prove runtime proof evaluation.

---

## Task 1: Add /count endpoint

**Category:** Coding

**Files:**
- Create: app.py

1. Write failing test

```python
from fastapi.testclient import TestClient
from app import app

def test_count_returns_zero():
    client = TestClient(app)
    assert client.get("/count").json() == {"count": 0}
```

2. Verify test fails

```bash
pytest test_app.py  # expect a collection error: app.py missing
```

3. Write minimal implementation

```python
from fastapi import FastAPI

app = FastAPI()
count = 0

@app.get("/count")
def read_count():
    return {"count": count}
```

4. Verify test passes

```bash
pytest test_app.py  # expect 1 passed
```

5. Proof

Run the server, request /count, capture the response body.

```bash
uvicorn app:app --port 8000 &
sleep 1
curl -s http://localhost:8000/count > SESSION_SCRATCH/count.json
kill %1
```

Expected outcome: `SESSION_SCRATCH/count.json` contains `{"count": 0}` and the server stayed alive.

**Done when:**

- Test passes
- Proof artifact captured matching expected outcome

---

## Task 2: Validation

**Category:** Non-coding

Run the integrated app and confirm both the feature runs end-to-end.

1. Start the app and hit the endpoint

```bash
uvicorn app:app --port 8000 &
sleep 1
curl -s http://localhost:8000/count
kill %1
```

Expected outcome: 200 response with JSON body `{"count": 0}`.

**Done when:**

- App runs and returns the expected response

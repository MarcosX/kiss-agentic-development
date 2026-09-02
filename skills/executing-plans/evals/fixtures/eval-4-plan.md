# Cache Hit Counter Plan

**Goal:** Add a runnable endpoint that returns the count of cache hits.

**Acceptance Criteria:**

- AC-1: `/count` endpoint returns JSON `{"count": 0}` on initial request [owned by: Task 1]

---

## Task 1: Add /count endpoint

**Category:** Coding
**Satisfies:** AC-1

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

**Done when:**

- Test passes

---

## AC Evals

### AC-1 Eval: /count endpoint returns initial count

**Procedure:**

1. Start the app:
   ```bash
   uvicorn app:app --port 8000 &
   sleep 1
   ```
2. Exercise the endpoint:
   ```bash
   curl -s http://localhost:8000/count
   ```
3. Capture the response and confirm the server stays alive.

**Expected evidence:** HTTP 200 response with JSON body `{"count": 0}`.

**Dependencies:** None

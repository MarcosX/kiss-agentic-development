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
- Test: test_app.py

**Contract:**

- `app` is a FastAPI application exposing `GET /count`
- On initial request, returns HTTP 200 with JSON body `{"count": 0}`
- No request body, no query parameters

**Done when:**

- Contract behavior verified through the test-first loop (failing test watched for the expected reason, then green, then refactored)
- Full test suite passes with no regressions
- Application starts under uvicorn and answers on port 8000

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

# Cache Hit Counter Plan

**Goal:** Expose a runnable cache-hit counter over HTTP.

**Acceptance Criteria:**

- AC-1: `/count` endpoint returns JSON `{"count": 0}` on initial request [owned by: Task 1]
- AC-2: after a `POST /record`, `/count` returns JSON `{"count": 1}` [owned by: Task 1]

---

## Task 1: Add cache-hit counter endpoints

**Category:** Coding
**Satisfies:** AC-1, AC-2

**Files:**

- Create: app.py
- Test: test_app.py

**Contract:**

- `app` is a FastAPI application exposing `GET /count` and `POST /record`.
- `GET /count` returns HTTP 200 with JSON body `{"count": N}` where N is the number of recorded hits (0 before any record).
- `POST /record` returns HTTP 200 with JSON body `{}` and increments the recorded-hit count.
- Either endpoint accepts no request body and no query parameters.

**Done when:**

- Contract behavior verified through the test-first loop (failing test watched for the expected reason, then green, then refactored)
- Full test suite passes with no regressions
- Application starts under uvicorn and answers on port 8000

---

## AC Evals

### AC-1 Eval: /count returns initial count

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

### AC-2 Eval: /count increments after /record

**Procedure:**

1. Start the app (reuse the instance from AC-1 if still running, otherwise start fresh):
   ```bash
   uvicorn app:app --port 8000 &
   sleep 1
   ```
2. Record a hit:
   ```bash
   curl -s -X POST http://localhost:8000/record
   ```
3. Read the counter:
   ```bash
   curl -s http://localhost:8000/count
   ```
4. Capture both responses.

**Expected evidence:** POST /record returns HTTP 200 with body `{}`; the subsequent GET /count returns HTTP 200 with body `{"count": 1}`.

**Dependencies:** AC-1

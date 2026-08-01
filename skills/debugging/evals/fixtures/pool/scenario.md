Production intermittently fails under load with "connection pool exhausted". Users see requests hang, then 500s.

Code:
- `skills/debugging/evals/fixtures/pool/db.py`
- `skills/debugging/evals/fixtures/pool/worker.py`

`logs/error.log` (last 5 entries):

```
[2026-07-31 09:12:01] DBError: connection pool exhausted: max 3 connections
[2026-07-31 09:12:03] DBError: connection pool exhausted: max 3 connections
[2026-07-31 09:12:05] RetryHandler: attempt 2 of 3, retrying after 1s
[2026-07-31 09:12:08] DBError: connection pool exhausted: max 3 connections
[2026-07-31 09:12:11] RetryHandler: attempt 3 of 3, giving up
```

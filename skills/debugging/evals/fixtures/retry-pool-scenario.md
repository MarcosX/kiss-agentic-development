Our checkout endpoint times out intermittently. Here is the relevant context:

File: `recent-changes.md`

```
Deploy (2 days ago): db.py now uses a connection pool (pool_size: 10).
Deploy (yesterday): checkout requests wrapped in a retry helper — retries: 2, backoff: fixed 100ms.
```

File: `logs/error.log` (last 8 entries)

```
[22:47:11.040] Checkout.TimedOut: request to /checkout timed out after 5s
[22:47:11.042] DB.Warn: could not get connection from pool (pool exhausted, 10/10 in use)
[22:47:11.146] Checkout.TimedOut: request to /checkout timed out after 5s
[22:47:11.149] DB.Warn: could not get connection from pool (pool exhausted, 10/10 in use)
[22:47:11.254] Checkout.TimedOut: request to /checkout timed out after 5s
[22:47:11.256] DB.Warn: could not get connection from pool (pool exhausted, 10/10 in use)
[22:47:11.358] Checkout.TimedOut: request to /checkout timed out after 5s
[22:47:11.361] DB.Warn: could not get connection from pool (pool exhausted, 10/10 in use)
```

File: `config/db.py` (note)

```
# Checkout borrows a pooled connection for the request and holds it until the
# handler finishes — under normal load about 200ms from borrow to release.
```
We run an e-commerce checkout. The currency conversion step recently changed. Here is the relevant context:

File: `deploy-notes.md`

```
Deploy (2026-09-10): checkout now reads USD→EUR conversion rate from Redis cache
(key `fx:usd:eur`), falling back to the live FX API only on cache miss.
```

File: `logs/app.log` (last 20 entries)

```
[2026-09-09 08:12:04] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 1/2)
[2026-09-09 08:12:06] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 2/2)
[2026-09-09 08:12:06] Checkout.Warn: currency conversion unavailable, using stale rate
[2026-09-09 14:33:19] Redis.Warn: min connections too low, scaling up 2→8
[2026-09-09 14:33:22] Checkout.Info: order 88213 placed (channel web)
[2026-09-10 09:01:22] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 1/2)
[2026-09-10 09:01:24] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 2/2)
[2026-09-10 09:01:24] Checkout.Warn: currency conversion unavailable, using stale rate
[2026-09-10 14:02:11] Deploy: rates-cache rollout complete (Redis cache in front of fx-api)
[2026-09-10 14:02:40] RateCache.Miss: key 'fx:usd:eur' not found, fetching from upstream
[2026-09-10 14:02:41] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 1/2)
[2026-09-10 14:02:43] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 2/2)
[2026-09-10 14:02:43] Checkout.Warn: currency conversion unavailable, using stale rate
[2026-09-10 14:05:58] RateCache.Miss: key 'fx:usd:eur' not found, fetching from upstream
[2026-09-10 14:05:59] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 1/2)
[2026-09-10 14:06:01] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 2/2)
[2026-09-10 14:06:01] Checkout.Warn: currency conversion unavailable, using stale rate
[2026-09-11 08:04:58] RateCache.Miss: key 'fx:usd:eur' not found, fetching from upstream
[2026-09-11 08:05:00] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 1/2)
[2026-09-11 08:05:02] FxApi.TimeoutError: upstream 'fx-api' timed out after 3s (attempt 2/2)
[2026-09-11 08:05:02] Checkout.Warn: currency conversion unavailable, using stale rate
```

Note: the FX API typically responds in 1–2 seconds under normal conditions.
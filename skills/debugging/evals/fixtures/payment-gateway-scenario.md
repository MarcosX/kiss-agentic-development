We have a small e-commerce codebase. Here is the relevant context:

File: `config/payment.php`

```php
<?php
return [
    'gateway' => 'stripe',
    'timeout' => 5, // seconds — changed from 30 to 5 last deploy
    'retries' => 0,
    'api_key' => env('STRIPE_API_KEY'),
];
```

File: `logs/error.log` (last 5 entries)

```
[2026-07-28 14:23:45] PaymentGateway.Timeout: Connection timed out after 5 seconds
[2026-07-28 14:23:46] PaymentGateway.Timeout: Connection timed out after 5 seconds
[2026-07-28 14:23:47] Checkout.Error: Unable to complete checkout after timeout
[2026-07-28 14:24:01] PaymentGateway.Timeout: Connection timed out after 5 seconds
[2026-07-28 14:24:02] Checkout.Error: Unable to complete checkout after timeout
```

Note: The Stripe API typically responds in 10-15 seconds under normal conditions.

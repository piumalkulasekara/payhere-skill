---
name: payhere
description: Build, review, and troubleshoot PayHere Sri Lanka payment integrations. Use when working with PayHere Checkout API, JavaScript SDK, Android/iOS/React Native/Flutter SDKs, Recurring API, Preapproval and Charging API, Authorize and Capture API, Refund or Retrieval APIs, sandbox testing, PayHere Links/Buttons, shopping-cart plugins, merchant onboarding, callbacks, hashes, OAuth tokens, or PayHere-specific payment status handling.
---

# PayHere

Use this skill to implement or diagnose PayHere integrations without rediscovering PayHere's product model, API flows, hash rules, callback behavior, and sandbox details.

## First Steps

1. Identify the PayHere path:
   - One-time web payment: Checkout API or JavaScript SDK.
   - Onsite web popup: JavaScript SDK.
   - Native app: Android, iOS, React Native, or Flutter SDK.
   - Subscription: Recurring API plus Subscription Manager API.
   - Tokenized/on-demand payment: Preapproval API plus Charging API.
   - Hold now, capture later: Authorize API plus Capture API.
   - Operations: Retrieval API, Refund API, PayHere portal, Links, Buttons, or plugins.
2. Ask for or locate environment values: sandbox/live, merchant ID, domain/app-specific merchant secret, allowed domain/app package, callback URL, order ID, currency, amount, and relevant tokens.
3. Protect secrets. Never put merchant secrets, app secrets, authorization codes, access tokens, customer tokens, or authorization tokens in client-side code, logs, fixtures, or public examples.
4. Treat `return_url` as user navigation only. Rely on `notify_url` server callbacks and signature verification before updating orders, subscriptions, tokens, or captures.
5. Check the relevant reference:
   - PayHere product, account, limits, and operational behavior: `references/system-overview.md`
   - API endpoints, parameters, statuses, hash/OAuth rules: `references/api-reference.md`
   - Web/mobile SDKs and shopping-cart plugins: `references/sdk-and-plugin-reference.md`
   - Crawled knowledge-base URL map and source freshness notes: `references/source-map.md`

## Implementation Rules

- Generate the checkout/request `hash` on the server:

```text
HASH = UPPER(MD5(merchant_id + order_id + amount_with_two_decimals + currency + UPPER(MD5(merchant_secret))))
```

- Verify callback `md5sig` before marking anything paid, approved, tokenized, captured, refunded, or canceled:

```text
MD5SIG = UPPER(MD5(merchant_id + order_id + payhere_amount + payhere_currency + status_code + UPPER(MD5(merchant_secret))))
```

- Format amounts with exactly two decimal places and no thousands separators before hashing.
- Use a public `notify_url`; localhost cannot receive PayHere callbacks. For local testing, use a tunnel or deploy a temporary callback endpoint.
- Parse callbacks as `application/x-www-form-urlencoded`, not JSON, for redirect-style APIs and SDK notifications.
- Store merchant-side order/payment state before redirecting or opening a popup. Callback delivery and browser return are separate events.
- Make payment updates idempotent by `order_id` plus PayHere `payment_id` or subscription/preapproval token.
- For live merchant REST APIs, expect both allowed-domain/app restrictions and IP whitelisting. Guide the merchant to request PayHere support whitelisting for the server IP when needed.
- Keep sandbox and live credentials completely separate. Sandbox accounts cannot be converted into live accounts.

## Helper Script

Use `scripts/payhere_crypto.py` to calculate hashes, callback signatures, and OAuth Basic authorization strings while implementing or debugging:

```bash
python scripts/payhere_crypto.py request-hash \
  --merchant-id 121XXXX \
  --order-id Order123 \
  --amount 1000 \
  --currency LKR \
  --merchant-secret "$PAYHERE_MERCHANT_SECRET"

python scripts/payhere_crypto.py notification-sig \
  --merchant-id 121XXXX \
  --order-id Order123 \
  --payhere-amount 1000.00 \
  --payhere-currency LKR \
  --status-code 2 \
  --merchant-secret "$PAYHERE_MERCHANT_SECRET"
```

Use examples with fake credentials only. If a user provides real secrets, avoid echoing them back.

## Source Freshness

The PayHere support knowledge base changes. If the user asks for the latest pricing, limits, SDK versions, approval rules, or live operational requirements, verify against the current PayHere documentation before answering or changing code.

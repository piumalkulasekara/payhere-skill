# PayHere API Reference

## Environments

Hosted redirect/form APIs:

- Checkout: sandbox `https://sandbox.payhere.lk/pay/checkout`, live `https://www.payhere.lk/pay/checkout`
- Recurring: same checkout endpoint as Checkout API.
- Preapproval: sandbox `https://sandbox.payhere.lk/pay/preapprove`, live `https://www.payhere.lk/pay/preapprove`
- Authorize: sandbox `https://sandbox.payhere.lk/pay/authorize`, live `https://www.payhere.lk/pay/authorize`

Merchant REST APIs:

- OAuth token: sandbox `https://sandbox.payhere.lk/merchant/v1/oauth/token`, live `https://www.payhere.lk/merchant/v1/oauth/token`
- Charge: sandbox `https://sandbox.payhere.lk/merchant/v1/payment/charge`, live `https://www.payhere.lk/merchant/v1/payment/charge`
- Capture: sandbox `https://sandbox.payhere.lk/merchant/v1/payment/capture`, live `https://www.payhere.lk/merchant/v1/payment/capture`
- Refund: sandbox `https://sandbox.payhere.lk/merchant/v1/payment/refund`, live `https://www.payhere.lk/merchant/v1/payment/refund`
- Retrieval: sandbox `https://sandbox.payhere.lk/merchant/v1/payment/search?order_id={order_id}`, live `https://www.payhere.lk/merchant/v1/payment/search?order_id={order_id}`
- Subscriptions: sandbox/live `/merchant/v1/subscription`, `/merchant/v1/subscription/{subscription_id}/payments`, `/merchant/v1/subscription/retry`, `/merchant/v1/subscription/cancel`

## Merchant Credentials

Redirect APIs and SDK checkout use:

- `merchant_id`: unique to the PayHere merchant account.
- `merchant_secret`: specific to an allowed domain or app package. Generate it in PayHere Merchant Portal under integrations/domains and credentials.

REST APIs use:

- `app_id` and `app_secret` from a PayHere API key or Business App.
- OAuth Basic authorization string: Base64 encode `app_id:app_secret`.
- Access token endpoint body: `grant_type=client_credentials`.
- Header: `Authorization: Basic <base64-app-id-colon-app-secret>`.
- API calls use `Authorization: Bearer <access_token>`.

Live merchant APIs can require allowed domain/app configuration and server IP whitelisting through PayHere support.

## Hashes And Callback Signatures

Request hash for Checkout, Recurring, Preapproval, Authorize, JavaScript SDK, and mobile SDK flows:

```text
UPPER(MD5(merchant_id + order_id + amount + currency + UPPER(MD5(merchant_secret))))
```

Use exactly two decimals for `amount`, for example `1000.00`.

Preapproval special case:

- If optional `amount` is sent, hash that amount.
- If no `amount` is sent, use `10.00` for `LKR` or `1.01` for other currencies when generating the hash.

Callback signature:

```text
UPPER(MD5(merchant_id + order_id + payhere_amount + payhere_currency + status_code + UPPER(MD5(merchant_secret))))
```

Only trust a callback if the locally generated signature equals `md5sig`. Only mark success after signature verification and an accepted success status.

## Callback Handling

Common callback fields:

- `merchant_id`
- `order_id`
- `payment_id`
- `payhere_amount`
- `payhere_currency`
- `status_code`
- `md5sig`
- `custom_1`
- `custom_2`
- `method`
- `status_message`
- Card fields when relevant: `card_holder_name`, `card_no`, `card_expiry`

Status codes for Checkout, JavaScript SDK notification, Recurring payment notification, Preapproval notification, and Charging response:

- `2`: success
- `0`: pending
- `-1`: canceled
- `-2`: failed
- `-3`: chargebacked, used in payment callbacks where documented

Rules:

- `notify_url` must be publicly reachable. Do not use localhost.
- Callbacks are server-to-server and are not visible in the browser.
- No authoritative payment status is passed to `return_url`; display status by reading your own server-side order state.
- Redirect-style callback params are `application/x-www-form-urlencoded`.
- Make callback processing idempotent.

## Checkout API

Use for one-time hosted web payments.

Required POST fields:

- Merchant and URLs: `merchant_id`, `return_url`, `cancel_url`, `notify_url`
- Customer: `first_name`, `last_name`, `email`, `phone`, `address`, `city`, `country`
- Order: `order_id`, `items`, `currency`, `amount`, `hash`

Optional fields include delivery address, itemized fields (`item_name_1`, `item_number_1`, `amount_1`, `quantity_1`, etc.), `platform`, `custom_1`, and `custom_2`.

## Recurring API

Use for subscriptions charged on a fixed schedule. It is a hosted POST flow through the checkout endpoint.

Required fields are Checkout fields except recurring also requires:

- `recurrence`: e.g. `1 Month`, `2 Week`, `1 Year`
- `duration`: `Forever` or a compatible duration such as `1 Year`, `3 Month`

Optional fields include `startup_fee`, itemized fields, delivery fields, `platform`, `custom_1`, and `custom_2`.

Recurring notifications add:

- `subscription_id`
- `recurring`: `1` or `0`
- `message_type`: examples include `AUTHORIZATION_SUCCESS`, `AUTHORIZATION_FAILED`, `RECURRING_INSTALLMENT_SUCCESS`, `RECURRING_INSTALLMENT_FAILED`, `RECURRING_COMPLETE`, `RECURRING_STOPPED`
- `item_recurrence`, `item_duration`, `item_rec_status`, `item_rec_date_next`, `item_rec_install_paid`

## Preapproval API

Use for tokenizing a customer's card for later merchant-initiated charges. Automated Charging is documented as Visa/MasterCard only.

Required fields:

- `merchant_id`, `return_url`, `cancel_url`, `notify_url`
- Customer details
- `order_id`, `items`, `currency`, `hash`

Optional fields:

- `amount`: capture an initial amount in addition to preapproval.
- `platform`, `custom_1`, `custom_2`

Successful callback includes `customer_token`; store it securely and associate it with the customer. The preapproval flow can charge a small amount and refund it as part of authorization, per PayHere's current docs.

## Charging API

Use after Preapproval API when the merchant has a `customer_token`.

Request:

```json
{
  "type": "PAYMENT",
  "order_id": "Order12345",
  "items": "Taxi Hire 123",
  "currency": "LKR",
  "amount": 345.67,
  "customer_token": "TOKEN",
  "custom_1": "optional",
  "custom_2": null,
  "notify_url": "https://example.com/payhere/notify",
  "itemList": [
    { "name": "Item", "number": "ITEM_1", "quantity": 1, "unit_amount": 300.00 }
  ]
}
```

`type` can be:

- `PAYMENT`: charge immediately.
- `AUTHORIZE`: authorize/hold and return an `authorization_token`.

Optional fields: `custom_1`, `custom_2`, `notify_url`, `itemList`.

Successful response status is top-level `status: 1` with `data.status_code`. The `authorization_token` is populated only for `AUTHORIZE`.

Common errors: invalid or expired access token, invalid token, invalid currency, invalid amount, authentication error.

## Authorize API

Use for Hold on Card flows where funds are reserved and captured later.

Hosted endpoint fields mirror Checkout API and require `amount`. The authorization callback includes `authorization_token`; store it securely. Capture within 7 days and only for an equal or lower amount. Hold on Card is documented as Visa/MasterCard credit cards only.

## Capture API

Use after Authorize API or Charging API with `type: AUTHORIZE`.

Request:

```json
{
  "authorization_token": "TOKEN",
  "amount": 80.00,
  "deduction_details": "Item1 is out of stock"
}
```

Response uses top-level `status: 1` and nested `data.status_code`:

- `2`: success
- `0`: unknown
- `-2`: failed

Captured payments settle after capture according to PayHere's settlement rules.

## Retrieval API

Use to search successful payments by merchant `order_id`.

Request: `GET /merchant/v1/payment/search?order_id={order_id}` with Bearer token.

Top-level status:

- `1`: request/payment successful
- `0`: payment pending
- `-1`: no records found
- `-2`: declined/authentication-style failure depending on context

Payment `data[*].status` values include `RECEIVED`, `REFUND REQUESTED`, `REFUND PROCESSING`, `REFUNDED`, and `CHARGEBACKED`.

PayHere does not guarantee merchant `order_id` uniqueness, so code must handle multiple records.

## Refund API

Use Bearer token and POST JSON to `/merchant/v1/payment/refund`.

Refund a payment:

```json
{
  "payment_id": "320027150501",
  "description": "Item is out of stock"
}
```

Refund an authorization:

```json
{
  "authorization_token": "74d7f304-7f9d-481d-b47f-6c9cad32d3d5",
  "description": "Order canceled"
}
```

Partial refunds include `amount` as a decimal string/amount. Do not send both `payment_id` and `authorization_token` unless current docs explicitly allow it; choose the one matching the refund type.

Refund response status:

- `1`: success
- `0`: error initiating refund
- `-1`: refund failed; inspect `msg`

`data` contains the refund number for payment refunds.

## Subscription Manager API

Use for subscriptions created by Recurring API.

Endpoints:

- `GET /merchant/v1/subscription`: list subscriptions.
- `GET /merchant/v1/subscription/{subscription_id}/payments`: list payments for one subscription.
- `POST /merchant/v1/subscription/retry`: body `{ "subscription_id": 420075032251 }`.
- `POST /merchant/v1/subscription/cancel`: body `{ "subscription_id": 420075032251 }`.

Subscription statuses include `ACTIVE`, `COMPLETED`, and `FAILED`.

Top-level API status:

- `1`: success
- `-1`: failed; inspect `msg`
- `-2`: authentication error in documented error cases

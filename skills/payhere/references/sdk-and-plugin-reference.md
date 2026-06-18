# PayHere SDK And Plugin Reference

## JavaScript SDK

Use `payhere.js` for onsite checkout when the merchant wants a popup/iframe instead of redirecting the customer to a hosted PayHere page.

Script:

```html
<script type="text/javascript" src="https://www.payhere.lk/lib/payhere.js"></script>
```

Core payment object fields mirror Checkout API:

- `sandbox`: boolean
- `merchant_id`, `return_url`, `cancel_url`, `notify_url`
- `order_id`, `items`, `amount`, `currency`, `hash`
- Customer fields: `first_name`, `last_name`, `email`, `phone`, `address`, `city`, `country`
- Optional delivery, itemized, platform, and custom fields

Generate `hash` on the backend and fetch it into the frontend. Do not expose merchant secret in browser code.

Events:

- `payhere.onCompleted(orderId)`: checkout completed, but still verify callback/server status before showing final success.
- `payhere.onDismissed()`: customer closed popup.
- `payhere.onError(error)`: invalid params or SDK-side error.

Call `payhere.startPayment(payment)` to open the payment UI.

JavaScript SDK can also request:

- Preapproval: set `preapprove: true`.
- Recurring: set `recurrence` and `duration`.

## Mobile SDKs

Mobile SDKs initiate payment inside the app and return immediate SDK responses, but server-side `notify_url` verification remains the authoritative integration path.

Android:

- Add JitPack repository.
- Dependency documented as `com.github.PayHereDevs:payhere-android-sdk:v3.0.18`.
- Add `android.permission.INTERNET`.
- Use `InitRequest`, set merchant/order/customer/currency/amount fields, set `PHConfigs.SANDBOX_URL` for sandbox, and launch `PHMainActivity`.

iOS:

- Install through CocoaPods with `pod 'payHereSDK'`.
- Minimum platform in the docs is iOS 11.0.
- Import `payHereSDK`.
- Use `PHInitialRequest` and present through `PHPrecentController`.
- Supports one-time payment, recurring payment, preapproval, and hold-on-card request patterns.

React Native:

- Use the PayHere React Native SDK page for current package/version and platform setup.
- Expect the same product flows as native/mobile: one-time, recurring, preapproval, and hold-on-card where supported.

Flutter:

- Dependency documented as `payhere_mobilesdk_flutter: ^3.2.2`.
- Android prerequisites include PayHere's Maven repository, manifest merge rule, and ProGuard keep rules for Retrofit/OkHttp/PayHere classes.
- iOS requires `pod install`.
- Whitelist the app package name in PayHere Merchant Portal under Domains & Credentials and use the generated app-specific merchant secret.
- Flutter payment object includes `sandbox`, `merchant_id`, `merchant_secret`, `notify_url`, order fields, customer fields, delivery fields, and custom fields.

Always re-check SDK package versions before adding dependencies.

## Shopping-Cart Plugins

Use official PayHere plugins when the merchant is on a supported cart and does not need custom behavior.

General plugin setup pattern:

1. Install/download the plugin for the specific platform and version.
2. Enable PayHere as a payment method in the platform admin.
3. Enter Merchant ID.
4. Enter Merchant Secret or Secret Key exactly matching PayHere portal/domain settings.
5. Enable sandbox only for sandbox testing.
6. Let the platform/plugin handle return URLs when documented.
7. Save and test with sandbox cards before live use.

Platform notes:

- OpenCart: install through OpenCart extension flow; configure under Extensions > Payments.
- WooCommerce: install the WordPress plugin, activate it, configure under WooCommerce checkout/payment settings.
- Magento: plugin differs for Magento 1.x, Magento 2.0-2.2, 2.3-2.4.5, and 2.4.6+; run Magento setup/upgrade and clear cache for Magento 2.
- PrestaShop: plugin differs for 1.6 and 1.7; upload to `modules/` and configure PayHere.
- ShopHere: built-in payment settings in ShopHere dashboard.
- Shopify: PayHere has a Shopify one-click plugin path; verify the current setup page.
- WHMCS, CS-Cart, Moodle: use the platform-specific page for current download and configuration details.

## Links And Buttons

PayHere Links are best for social commerce, invoices, email/chat/SMS payments, and simple order collection without a custom website checkout. The merchant creates a PayHere Link in the portal and shares it.

PayHere Buttons are best for embedding simple payment actions into a website without building a full checkout integration.

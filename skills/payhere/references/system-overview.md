# PayHere System Overview

## Product Model

PayHere is a Sri Lankan online payment gateway for business payments. It supports local and global online payment methods through a merchant account, with customer payment via cards, bank-account methods, and mobile wallets.

Core actors and objects:

- Merchant: Sri Lankan business entity using PayHere to accept online payments.
- Customer: payer using PayHere to pay the merchant.
- Payment: money received for goods or services.
- Payout: funds transferred from PayHere balance to the merchant bank account.
- PayHere account/balance: virtual merchant account holding received payments before payout.
- Refund: reversal to the customer.
- Chargeback/dispute: card or wallet-provider reversal or query.

## Merchant Onboarding

Eligible applicants are Sri Lankan businesses selling goods or services locally or globally. Common accepted business types include private limited companies, sole proprietorships, partnerships, clubs/associations, home-based businesses, freelance businesses, and government organizations.

Typical prerequisites:

- Valid business or accepted proof of business.
- Local bank account. Business bank account is expected for registered companies, partnerships, and sole proprietorships; personal accounts can be used for home-based or freelance businesses.
- Website/app/page that is complete if the merchant plans to integrate PayHere there.
- Terms, return/refund policy, privacy policy, and visible business contact details on the website/app.

Important constraints:

- PayHere is for business payments where goods or services are provided. It is not for general donations.
- Some categories and models are unsupported, including gems/jewellery, unauthorized software licenses, outbound tours, dating, astrology, drop-shipping, print-on-demand, and multi-vendor platforms.
- Approval is handled by partner banks. Business review commonly takes 1 to 3 days, while domain/app merchant-secret approval can take up to 24 hours or one business day depending on context.

## Payment Methods And Currencies

Supported methods documented by PayHere include:

- Cards: Visa, MasterCard, American Express, Discover, Diners Club.
- Bank-account method: HelaPay.
- Wallets and local methods: Frimi, Genie, iPay, Q Plus, Sampath Vishwa, and others documented in callback method values.

Supported currencies listed across docs include `LKR`, `USD`, `GBP`, `EUR`, and `AUD`. Some API pages show only `LKR/USD` for older forms, so verify the current method-specific currency list before making claims.

## Settlement, Refunds, And Payouts

- PayHere sends merchant email notifications, customer receipts, portal payment updates, and HTTP callbacks where integrated.
- General settlement is described as daily payouts on a T+2 cycle after payment notification.
- Instant refunds apply when reversing same-day transactions before day end and appear as a void.
- Delayed refunds apply after payout and can take several days, commonly 5-10 days or longer, because funds must be recovered and processed.
- USD Payouts let eligible registered Sri Lankan businesses collect foreign customer payments directly into a USD bank account, with PayHere Plus or Premium plan requirements noted in the knowledge base.

## Product Decision Guide

- Use PayHere Links when the merchant does not need a custom checkout or is selling through social media, chat, invoice links, email, or SMS.
- Use PayHere Buttons for embedding simple payment buttons on a website without building a full API integration.
- Use shopping-cart plugins for WooCommerce, OpenCart, Magento, PrestaShop, Shopify, WHMCS, CS-Cart, Moodle, and similar platforms.
- Use Checkout API for one-time web payments with hosted PayHere redirect.
- Use JavaScript SDK for an onsite popup/iframe checkout on web or cross-platform web views.
- Use mobile SDKs for native app payment UI without browser redirects.
- Use Recurring API for subscriptions where PayHere charges on a fixed recurrence.
- Use Preapproval API plus Charging API for customer-approved tokenized on-demand charges.
- Use Authorize API plus Capture API for hold-on-card flows where the merchant reserves funds and captures the final equal-or-lower amount later.

## Sandbox

Sandbox is a separate test environment and does not process real payments. It cannot be converted into a live account.

Sandbox successful test cards:

- Visa: `4916217501611292`
- MasterCard: `5307732125531191`
- AMEX: `346781005510225`

Decline scenarios:

- Insufficient funds: Visa `4024007194349121`, MasterCard `5459051433777487`, AMEX `370787711978928`
- Limit exceeded: Visa `4929119799365646`, MasterCard `5491182243178283`, AMEX `340701811823469`
- Do not honor: Visa `4929768900837248`, MasterCard `5388172137367973`, AMEX `374664175202812`
- Network error: Visa `4024007120869333`, MasterCard `5237980565185003`, AMEX `373433500205887`

Use any valid name, CVV, and expiry date for sandbox testing.

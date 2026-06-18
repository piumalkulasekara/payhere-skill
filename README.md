# PayHere Skill

[skills.sh](https://skills.sh/piumalkulasekara/payhere-skill)
[PayHere docs](https://support.payhere.lk/)
[Skill](skills/payhere/SKILL.md)
[Python helper](skills/payhere/scripts/payhere_crypto.py)

Agent skill for building, reviewing, and troubleshooting PayHere Sri Lanka payment integrations.

## Install

```bash
npx skills add https://github.com/piumalkulasekara/payhere-skill --skill payhere -a codex
```

Install for all detected agents:

```bash
npx skills add https://github.com/piumalkulasekara/payhere-skill --skill payhere
```

List discoverable skills before installing:

```bash
npx skills add https://github.com/piumalkulasekara/payhere-skill --list
```

## Skill

- Skill name: `payhere`
- Invocation: `$payhere`
- Source: `skills/payhere/SKILL.md`

The skill includes PayHere API references, SDK/plugin guidance, sandbox cards, callback and signature rules, and a helper script for PayHere request hashes, notification signatures, and OAuth Basic values.

## Official Documentation

- [PayHere Knowledge Base](https://support.payhere.lk/)
- [Sandbox & Testing](https://support.payhere.lk/sandbox-and-testing)
- APIs: [Checkout](https://support.payhere.lk/api-%26-mobile-sdk/checkout-api), [Recurring](https://support.payhere.lk/api-%26-mobile-sdk/recurring-api), [Preapproval](https://support.payhere.lk/api-%26-mobile-sdk/preapproval-api), [Charging](https://support.payhere.lk/api-%26-mobile-sdk/charging-api), [Retrieval](https://support.payhere.lk/api-%26-mobile-sdk/retrieval-api), [Subscription Manager](https://support.payhere.lk/api-%26-mobile-sdk/subscription-manager-api), [Refund](https://support.payhere.lk/api-%26-mobile-sdk/refund-api), [Authorize](https://support.payhere.lk/api-%26-mobile-sdk/authorize-api), and [Capture](https://support.payhere.lk/api-%26-mobile-sdk/capture-api)
- SDKs: [JavaScript](https://support.payhere.lk/api-%26-mobile-sdk/javascript-sdk), [Android](https://support.payhere.lk/api-%26-mobile-sdk/android-sdk), [iOS](https://support.payhere.lk/api-%26-mobile-sdk/ios-sdk), [React Native](https://support.payhere.lk/api-%26-mobile-sdk/react-native-sdk), and [Flutter](https://support.payhere.lk/api-%26-mobile-sdk/flutter-sdk)
- Links, buttons, and plugins: [PayHere Links](https://support.payhere.lk/links-%26-buttons/payhere-links), [PayHere Buttons](https://support.payhere.lk/links-%26-buttons/payhere-buttons), and [Shopping Cart Plugins](https://support.payhere.lk/shopping-cart-plugins/payhere-plugins)

## skills.sh

After the public GitHub repository is installed with the `skills` CLI, it should become visible at:

```text
https://skills.sh/piumalkulasekara/payhere-skill
```

The same badge is included at the top of this README:

```md
[![skills.sh](https://skills.sh/b/piumalkulasekara/payhere-skill)](https://skills.sh/piumalkulasekara/payhere-skill)
```

## Validate

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/payhere
python3 -m py_compile skills/payhere/scripts/payhere_crypto.py
```


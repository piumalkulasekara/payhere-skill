# PayHere Skill

Agent skill for building, reviewing, and troubleshooting PayHere Sri Lanka payment integrations.

## Install

Replace `YOUR_GITHUB_USER` with the GitHub owner after publishing this repository:

```bash
npx skills add YOUR_GITHUB_USER/payhere-skill --skill payhere -a codex
```

Install for all detected agents:

```bash
npx skills add YOUR_GITHUB_USER/payhere-skill --skill payhere
```

List discoverable skills before installing:

```bash
npx skills add YOUR_GITHUB_USER/payhere-skill --list
```

## Skill

- Skill name: `payhere`
- Invocation: `$payhere`
- Source: `skills/payhere/SKILL.md`

The skill includes PayHere API references, SDK/plugin guidance, sandbox cards, callback and signature rules, and a helper script for PayHere request hashes, notification signatures, and OAuth Basic values.

## skills.sh

After the public GitHub repository is installed with the `skills` CLI, it should become visible at:

```text
https://skills.sh/YOUR_GITHUB_USER/payhere-skill
```

Badge:

```md
[![skills.sh](https://skills.sh/b/YOUR_GITHUB_USER/payhere-skill)](https://skills.sh/YOUR_GITHUB_USER/payhere-skill)
```

## Validate

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/payhere
python3 -m py_compile skills/payhere/scripts/payhere_crypto.py
```

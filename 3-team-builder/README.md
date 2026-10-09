# Stage 3 · Team builder: a class plugin marketplace and a shared team tool

Teams build things other people install and use together. There are two patterns.

## Pattern A: team skills, distributed as a plugin

[`plugins/month-end-close-toolkit`](plugins/month-end-close-toolkit) is a plugin that bundles two skills
a close team uses the same way:

- `close-checklist` builds and tracks the close task list.
- `flux-commentary` drafts variance explanations with the team's thresholds and labels.

This repository is also a **plugin marketplace**: the file
[`/.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) lists the plugin.
A teammate installs it in Claude Code with two commands:

```bash
claude plugin marketplace add summersbyu/ai-course-distribution-examples
claude plugin install month-end-close-toolkit@byu-ai-course-examples
```

Then, in a Claude Code session, run `/month-end-close-toolkit:close-checklist`.

**Updating everyone:** edit a skill, raise `version` in `plugin.json`, and push. Teammates receive the
new version. That's change control, a natural governance lesson for an AIS course.

**For the course:** one class marketplace repository. Each team adds its plugin through a pull request,
and a TA reviews it before merging. That's review-before-sharing in practice.

## Pattern B: a shared team tool with no hosting

[Month-End Close Board](https://claude.ai/artifact/4wZM4pzV7hgpmuNXhRj6h8) is a published Claude artifact
with a shared data store. Everyone on the team opens one link and sees the same checklist. When
someone changes a status, everyone sees it live. No server, database setup, or API key is involved.

The owner shares the artifact from its **Share** menu. Until then, only the owner can open it.

## When a team tool needs real hosting

A team tool that runs Python, queries an outside system, or needs its own database moves to Stage 4,
on Streamlit. A free Streamlit account allows one private app, with viewers invited by email.

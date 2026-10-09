# Stage 2 · Personal builder: skills and vibe-coded apps

Students build things for their own workflow. There are three kinds here, and each shares differently.

| What | Example | Where it lives | How a classmate gets it |
| --- | --- | --- | --- |
| A skill | [`journal-entry-reviewer`](skills/journal-entry-reviewer/SKILL.md) | This repo (and the ZIP in [`dist/`](dist/)) | Download the ZIP, then upload it in Claude under **Customize > Skills** |
| A plain web page | [Depreciation Schedule Builder](https://summersbyu.github.io/ai-course-distribution-examples/apps/depreciation-calculator.html) | `docs/apps/` in this repo, served by GitHub Pages | Open the link. No account needed. |
| An AI-powered app | [Accounting Study Coach](https://claude.ai/artifact/LJDBW7AgBSma4mgikAFMK4) | A published Claude artifact | Open the link. Its AI runs on the classmate's own Claude account. |

## Why not Google Drive?

Drive is fine for the skill ZIP: it's just a file to download. It can't host either app, because
Google stopped serving web pages from Drive in 2016. A classmate would download the HTML file instead
of clicking a link and using it.

## Which app route to choose

- **Needs AI while someone uses it?** Publish it as a Claude artifact. No key, no hosting, no cost to you.
- **No AI at run time** (a calculator, a template, a reference page)? GitHub Pages. Anything on the page is public, so it must never contain a key.
- **Needs Python, a database, or another service's API?** That's Stage 4.

## Packaging a skill

A skill is a folder with a `SKILL.md` file. To share it as a ZIP, the folder name must match the
`name:` in the file. From this folder:

```bash
cd skills && zip -r ../dist/journal-entry-reviewer.zip journal-entry-reviewer
```

Skills enabled in Claude settings also load in Claude Code when you sign in with the same account.

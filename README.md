# AI Course Distribution Examples

## Prepared first exercise pilot

[Start or resume Accounting Lab 01](https://codespaces.new/summersbyu/ai-course-distribution-examples/tree/pilot-expense-sql-lab?quickstart=1)

For this pilot choose the **pilot-expense-sql-lab** branch and **Accounting Lab 01** environment.
The expense form and SQL lab start automatically. If no lab tab opens, use **View > Open View > Ports**,
then open **Accounting Lab** on **8501** in the browser. Keep port visibility **Private**.
No terminal setup commands or AI credentials are needed for the student exercise.

Read the [student handout](pilot-lab/handouts/student-handout.md).
Instructors should first complete the live readiness checks in the [preparation guide](pilot-lab/handouts/instructor-guide.md)
and use the [colleague trial sheet](pilot-lab/handouts/colleague-trial.md) to evaluate onboarding.

## Earlier distribution examples

Working examples of how students share what they build at each stage of the BYU accounting AI course.
Each stage needs a little more infrastructure than the one before. Only Stage 4 needs real hosting.

**Gallery page:** https://summersbyu.github.io/ai-course-distribution-examples/

| Stage | Example | Lives in | Hosting needed |
| --- | --- | --- | --- |
| [1 · Power user](1-power-user/) | A shared prompt library | GitHub (or Drive) | None |
| [2 · Personal builder](2-personal-builder/) | A skill, a vibe-coded web page, an AI-powered study aid | GitHub, GitHub Pages, a Claude artifact | Free, nothing to set up |
| [3 · Team builder](3-team-builder/) | A plugin installed from a class marketplace, and a shared team board | GitHub (this repo is the marketplace), a Claude artifact with shared data | Free, nothing to set up |
| [4 · Developer](4-developer/sql-analyst/) | An AI SQL analyst that uses an API key and a database | GitHub + Streamlit Community Cloud | Free tier; the API key costs money |

All data in this repository is synthetic. No real company, client, or personal data is used.

## The stack in one line

**Claude** (skills and published artifacts) + **GitHub** (files, Pages, and the plugin marketplace) +
**Streamlit Community Cloud** (apps that hold a key). Google Drive works for sharing files but can't run an app.

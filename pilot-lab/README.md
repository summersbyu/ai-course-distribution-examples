# Accounting Lab 01 pilot

This prepared exercise takes an unfamiliar student from their own GitHub account to entering fictional expenses, querying SQLite, exporting evidence, and stopping and resuming the same workspace. Student setup requires no pasted terminal commands or AI credentials.

[Start or resume Accounting Lab 01](https://codespaces.new/summersbyu/ai-course-distribution-examples/tree/pilot-expense-sql-lab?quickstart=1)

Choose the `pilot-expense-sql-lab` branch and Accounting Lab 01 configuration. Installation and app startup run automatically. If a browser tab does not open, use View > Open View > Ports and open Accounting Lab on 8501. Keep port visibility Private.

## Read before starting

- [Student handout](handouts/student-handout.md)
- [Instructor preparation and answer key](handouts/instructor-guide.md)
- [Colleague trial sheet](handouts/colleague-trial.md)

The instructor should complete a live first-launch and stop/resume check before distributing the student handout. Local app tests do not verify GitHub provisioning or network policies.

## Data and runtime

Each workspace starts empty. The database is created in `.lab-data/expenses.db`; code updates do not reset it. `.lab-data` and `.lab-runtime` are ignored by Git. Expenses, successful query runs, saved reflections, and checkpoints persist there. Unsubmitted text does not persist. Keep downloaded backups because a workspace may eventually be deleted.

The interface has Start here, Enter expenses, SQL practice, Save and resume, and Help sections. The SQL editor is read-only, allows queries on expenses with supported functions, limits execution, and caps displayed results. CSV recovery is available only in an empty lab.

## Maintainer validation

Use Python 3.12 and `requirements.lock.txt`. From this folder run `python -m unittest -v test_lab.py test_app.py`. The Linux launch scripts are called by `.devcontainer/devcontainer.json`. They must additionally be verified in a live Codespace before class.

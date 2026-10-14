# Accounting Lab 01 instructor guide

## Prepare and evaluate the first student exercise

This package provides a browser-based expense form, a persistent SQLite database in each student's Codespace, a bounded SQL editor, and downloadable evidence. The student workflow avoids setup commands and multiple terminals. The pilot tests whether that reduction is sufficient for your students and support capacity.

**Recommended first use:** a colleague trial using the student handout alone, followed by a representative 15 to 20 person pilot. Do not move directly from a successful demonstration to 390 students.

### What the package includes

| Component | Purpose |
| --- | --- |
| Student handout | Account setup, launch, guided SQL, independent task, backup, stop and resume |
| Colleague trial sheet | Observe usability, support needs, and learning without coaching |
| This guide | Groundwork, teaching modules, answer key, support, and rollout decisions |
| Prepared source and configuration | Automatic installation and launch on creation and restart |
| Database and UI tests | Check the case, read-only controls, recovery, and saved evidence |

### Scope of this first exercise

The lab introduces records, forms, SQL, validation, and persistence. It supports the foundation of the course's power user stage. Later lessons add joins, team review, tool building, and bounded agents. This exercise does not require Claude Code or runtime AI, and it does not test GitHub Pages or Streamlit Community Cloud publishing.

### Readiness status

Local checks cover record entry, query execution, expected totals, blocked writes, time and display limits, CSV recovery, saved evidence, and a fresh Streamlit session reading the same database. These checks do not establish live GitHub provisioning, port opening, restart hooks, campus network access, or capacity for 390 users.

Treat the live checks on page 3 as required before giving the packet to your colleague. A draft branch can be tried without merging it into the main course repository. The ZIP contains the source and editable handouts if you prefer a dedicated starter repository later.

<!-- PAGEBREAK -->

## Groundwork before giving out the handout

### Use the prepared pilot branch

The pilot branch is **pilot-expense-sql-lab** in **summersbyu/ai-course-distribution-examples**. The student handout points to [Start or resume Accounting Lab 01](https://codespaces.new/summersbyu/ai-course-distribution-examples/tree/pilot-expense-sql-lab?quickstart=1). Keep that branch available for the colleague trial. Students each receive their own workspace storage even though the source repository is shared.

For the trial, students do not fork the repository, create branches, or push records. Their database is excluded from source control. You do not need to merge the draft pull request to test this branch. After a successful pilot, freeze a tested course release and update all launch links together.

### Complete these instructor tasks

1. Confirm the branch exists and the start link selects it. Check the configured environment is named **Accounting Lab 01**, with a two-core machine available.
2. Complete the live first-launch and actual stop/resume checks on page 3. Use a newly created Codespace for this branch, not the workspace used during the earlier manual demonstration.
3. Tell participants where to submit the evidence and CSV. During the colleague trial they can keep the files and show them to you.
4. Choose a help contact and response window. Tell participants before the session how to report a blocked launch. Do not place a colleague's personal account or credentials into student instructions.
5. Prepare the alternate exercise on page 6 for accounts or networks that cannot launch. Students should not need to buy additional usage to demonstrate the SQL learning outcomes.
6. Confirm institutional approval for student-owned cloud accounts, synthetic course data, and the selected submission system. Set a backup and retention expectation for the semester.

### Know the cost model

This lab makes no model API calls. GitHub Free personal accounts currently include 120 core-hours and 15 GB-month of Codespaces storage per month. Two-core compute uses two core-hours for each running hour; that is approximately 60 running hours before other usage. These are individual allowances, not a pooled class budget. Storage continues to count while a workspace is stopped. Check current account usage and published terms before rollout. [GitHub billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)

Do not require GitHub Education approval for this first lab. If the course later relies on educational benefits, arrange and verify them before assignments depend on them. Monitor running time, storage, and unexpected billing prompts separately from future AI costs.

<!-- PAGEBREAK -->

## Run the live readiness check

Perform this check yourself before the colleague trial. Record the date, browser, operating system, and observed launch time. These are acceptance checks, not claims that hosting has already been validated.

### First launch and navigation

1. Use the exact student start link. If you already have a matching workspace, deliberately create a new one for this instructor readiness test. Students should normally resume their existing one.
2. Confirm the selected branch and environment. Start setup, wait for completion, and verify the Accounting Lab opens. No student terminal command should be needed.
3. If automatic tab opening is blocked, verify View > Open View > Ports displays **Accounting Lab** on **8501** and that its browser icon opens the lab. Keep the port Private.
4. Verify all five lab sections are usable, the menu is visible at normal laptop size, and the instructions match the handout. If the sidebar is collapsed, its expansion control must be discoverable.

### Data and actual lifecycle

Enter the case exactly. Run the guided queries, the fourth-record change, and the independent task. Download CSV and evidence. Save a checkpoint; note the Lab ID, four records, and $500.49.

Stop the Codespace using My Codespaces. Resume the same workspace. Verify startup is automatic, the Lab ID is unchanged, all records remain, and the saved query history and reflection remain in a fresh evidence export. Test the named **Restart Accounting Lab** task if startup fails; treat any required typed student command as a pilot defect.

### Account and recovery checks

- Verify a second account can create its own workspace from the public branch without repository write permission.
- Create a separate empty test workspace and restore the expense CSV. Confirm four records and $500.49. Confirm restore is refused in a nonempty lab.
- Test the campus network and a Mac and Windows browser before class. Record blocked domains or account policies and escalate them to the appropriate support owner.
- Confirm the final stopped status and inspect usage. Delete only disposable instructor test workspaces after backups are secured.

**Release condition.** Fix any broken launch link, installation failure, missing port, lost data, or credential requirement before inviting the colleague. A successful app test on a local machine cannot substitute for these live checks.

<!-- PAGEBREAK -->

## Teach the supporting modules

The student handout includes these foundations. Teach them briefly and check understanding before advancing. Times below are planning estimates; the pilot should establish actual timings.

| Module | Approximate time | Learning check |
| --- | --- | --- |
| Account and workspace orientation | 8 to 12 minutes | Find own workspace and distinguish stop from delete |
| Records and exact money storage | 8 minutes | Explain row, column, and 12550 cents |
| Reading and writing basic SQL | 15 to 20 minutes | Predict, filter, total, group, and adapt a query |
| Validation and evidence | 8 minutes | Reconcile the total and name missing accounting support |
| Backup and actual restart | 8 to 12 minutes | Match Lab ID, count, and total after resuming |

### Facilitation suggestions

Ask students to name the accounting question before showing SQL. Demonstrate one query, then have students explain each clause and predict the next result. Use the independent Software task to distinguish understanding from copying.

Ask why a correctly calculated total still does not establish approval, cutoff, occurrence, or classification. Accept examples such as invoices, purchase authorization, receipt of goods or services, a classification policy, or reviewer sign-off. Do not imply this small database represents a complete accounting system.

Keep the form-entry exercise separate from arbitrary database writes. The form is the controlled entry route; the SQL editor is read-only. INSERT, UPDATE, DELETE, and schema changes can be introduced later in disposable practice databases.

### Later modules for the full course

1. **SQL joins and accounting relationships:** customers, invoices, lines, and receipts; explain keys and detect duplicated totals.
2. **Team contribution and change control:** review a query, test against expected totals, propose a change, and explain source control. Introduce GitHub terminology here with a meaningful task.
3. **Tool making:** change a Streamlit report, validate input, write useful checks, and choose a publishing route.
4. **AI assisted work:** configure Claude Code, distinguish subscription and API billing, review generated changes, and validate answers.
5. **Agent building:** define tools and permissions, bound cost and execution, preserve evidence, and require human approval for consequential actions.

<!-- PAGEBREAK -->

## Answer key and assessment

### Expected results

| Task | Expected result |
| --- | --- |
| Query 1 before fourth record | Three vendors and their original amounts |
| Query 2 above $100 | Mountain Travel $300.00 then Campus Office Supply $125.50 |
| Query 3 initial | Count 3 and total $475.49 |
| Query 4 initial | Supplies $125.50, Software $49.99, Travel $300.00; one record each |
| Query 3 after fourth | Count 4 and total $500.49 |
| Query 4 after fourth | Supplies count 2 and $150.50; other categories unchanged |
| Independent Software task | Count 1 and total $49.99 |

One acceptable independent query is:

```sql
SELECT COUNT(*) AS expense_count,
       SUM(amount_cents) / 100.0 AS total_dollars
FROM expenses
WHERE category = 'Software';
```

An expense of exactly $100 is excluded by **> 10000**. **>= 10000** would include it. Dividing by 100.0 preserves dollars and cents. COUNT(*) counts saved rows, not vendors; two expenses from one vendor are still two records.

### Suggested ten point rubric

| Evidence | Points |
| --- | --- |
| Four correct records and reconciled totals | 2 |
| Guided queries with predictions and interpreted results | 2 |
| Independent Software query and explanation | 2 |
| Accounting reflection and independent validation | 2 |
| Actual restart observation, backup, and final stopped workspace | 2 |

Use the rubric for feedback during the pilot. Infrastructure failure should be recorded separately from SQL proficiency. Allow the alternate exercise or a reasonable retry when access fails.

The downloaded evidence includes timestamps, SQL, predictions, results, and reflections. It is a student-controlled learning artifact, not tamper-proof assessment or proof that a workspace was actually stopped. Observe the restart during the pilot; assess understanding with explanation and a small changed query.

<!-- PAGEBREAK -->

## Support recovery and the alternate exercise

### Support triage

Ask for the visible error, workspace name, lab section, and the last successful action. Never ask for passwords, tokens, verification codes, or API keys. First classify the issue as account or quota, launch or port, wrong workspace, record entry, or SQL understanding.

For a blank lab, compare Lab ID and workspace name before doing any recovery. For a missing app, inspect setup completion and port 8501; then try the named restart task once. For an incorrect total, inspect records before changing code.

### Correcting an accidental record

Students should note the record ID and ask for help. During the pilot, the instructor can guide a correction in the student's own workspace without taking their credentials. A maintainer may inspect the local SQLite file and make a parameterized update after confirming the intended record and value. Export a backup first. Do not silently modify the record to make an answer key match.

If entry errors are frequent, add a clearly labeled edit workflow before the next pilot. Do not make students recreate the whole environment for a mistyped amount. The initial package intentionally limits SQL to reading; correction is an instructor support action.

### Backup recovery

The app restores a downloaded CSV only into an empty lab. It validates headers, IDs, dates, categories, and positive integer cents. Expense recovery does not restore query history or reflections; those are retained in the separate evidence download. Remind students to download both before stopping and again after the restart observation.

### Alternate exercise when cloud access fails

Give the student the expense table on page 4 of the handout. Have them annotate each guided query, predict its rows and totals, write the Software query, and explain the fourth-record change. Collect these answers and a short reflection. Schedule the hands-on persistence check once access is restored.

This alternative meets the query interpretation and accounting validation goals, but it does not establish successful environment setup or database persistence. Record that distinction. Do not require payment to remove a technical access barrier.

For a live demonstration outage, prepare your own saved screenshots and an evidence export in advance. A recording or screenshot is an explanation aid; it is not evidence that the participant completed the workflow.

<!-- PAGEBREAK -->

## Technical groundwork and maintenance

One person must own the starter configuration, dependencies, and recovery process. Automated student setup reduces support work but does not eliminate maintenance. Keep technical instructions in this guide and source files, outside the student exercise flow.

### How startup and storage are organized

The dev container selects Python 3.12. Its creation hook installs the supplied dependency lock into **.lab-runtime/venv**. Its start hook launches Streamlit in the background, checks readiness, and exits. Port 8501 is forwarded and labeled Accounting Lab, with a request to open a browser tab. Browser policy may still require the Ports fallback.

The startup script uses a lock and checks an existing healthy server, so ordinary reconnects do not deliberately launch duplicate copies. The named Restart Accounting Lab task calls the same script. If a server is stuck rather than absent, a maintainer may need to inspect its log and restart it; do not turn that into student terminal coaching.

The expense database lives at **.lab-data/expenses.db** under the repository workspace. Runtime files and student data are excluded from Git. Ordinary source updates do not replace that database. Setup does not seed, reset, or delete existing records. Preserve this separation in future changes.

### Maintainer checks

Run the database and Streamlit UI tests from pilot-lab with the prepared Python environment:

```bash
python -m unittest -v test_lab.py test_app.py
```

For a startup problem, inspect **.lab-runtime/app.log** and the creation log. Rebuild only after checking the problem and securing backups. Records under /workspaces survive container rebuilds, but database migrations must still be designed and tested. Delete and recreate is not a routine repair for student data.

Top-level dependencies and resolved versions are pinned. The container image tag is specified but is not frozen by digest. Recheck image availability, Linux dependency installation, startup, and the handout after any release change. Keep a known working branch during a course run; do not automatically pull untested changes into student workspaces.

### Limits of the current package

The SQL runner uses a read-only connection, SQLite authorization rules, a supported function list, a progress timeout, and a display cap. These are controls for this small synthetic teaching dataset, not a claim of unrestricted hostile-query isolation. Some valid SQL functions are intentionally unsupported.

This lab is a development workspace, not an always-on published app. A stopped Codespace cannot serve the lab. For later published applications that need durable form entries, choose persistent database hosting; local SQLite changes on Streamlit Community Cloud are not guaranteed to survive restarts.

<!-- PAGEBREAK -->

## Decide whether to expand the pilot

After the colleague trial, revise the most common navigation or wording failures and repeat the same fresh-start test. Then invite 15 to 20 representative users, including Windows and Mac laptops, new GitHub users, and the campus network.

### Measure the support load

Record account setup time, first launch time, completion rate without intervention, total support minutes, successful actual restart rate, and evidence submission success. Suggested targets for a broader pilot are at least 90 percent completing without observer intervention, all completed restart tests preserving records, and no requirement to type setup commands. These are decision targets, not demonstrated results.

Extrapolate observed support demand honestly. If 20 percent need ten minutes of individual help, a class of 390 creates roughly 13 hours of help demand. A technically successful stack can still exceed the available support budget.

Before rollout, assign a maintainer and help owner, test accessibility at typical laptop widths and zoom levels, verify account and network access, publish the alternate route, freeze the tested release, and establish backup, retention, and semester-end deletion guidance. Do not assume every student has unused free quota.

### Sources and verification date

Platform behavior and allowances were checked on **October 14, 2026**. Recheck these sources before a semester launch. Actual GitHub screens may change; update navigation using the live readiness check.

- [Creating a GitHub account](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github)
- [Creating a Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository)
- [Creating and resuming through a course link](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces)
- [Forwarding ports and private visibility](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)
- [Workspace files and container rebuilds](https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace)
- [Automatic Codespace deletion](https://docs.github.com/en/codespaces/setting-your-user-preferences/configuring-automatic-deletion-of-your-codespaces)
- [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
- [Python SQLite connections and authorization](https://docs.python.org/3/library/sqlite3.html)
- [Streamlit app testing](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)
- [Streamlit cloud local storage limitations](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data)

**Decision to record:** Expand the pilot, revise and repeat, or select a simpler delivery environment. Preserve the observations behind that decision rather than relying on the appeal of the demonstration.

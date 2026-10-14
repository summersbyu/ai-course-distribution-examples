# Accounting Lab 01

## Enter expenses and answer questions with SQL

You will record fictional expenses through a browser form, query the saved records, and check that they remain after stopping and resuming your workspace. Your task is to explain and verify the answers, not simply produce a working screen.

**Allow 50 to 65 minutes for this first lab.** Account verification or a slow first launch may take longer. Work individually using your own GitHub account on a Windows or Mac laptop.

### What you need

- A laptop, internet connection, and a current browser with JavaScript and downloads enabled.
- Your own GitHub account and access to the email used for that account.
- This handout and a place to save downloaded evidence files.

No prior programming or SQL experience is required. You do not need to install Python, SQLite, Streamlit, or a desktop editor. You do not need a Claude subscription, an API key, or a Streamlit account for this lab.

### Begin from ground zero

1. Open [GitHub](https://github.com). If you have an account, sign in. Otherwise choose **Sign up**, follow the account creation steps, and verify your email. Choose the free account option. Keep your password and any verification codes private.
2. Open your profile menu and confirm your username. Use the same account whenever you return to the lab.
3. Bookmark [My Codespaces](https://github.com/codespaces). This is where you find, resume, and stop your workspace.
4. Open [Start or resume Accounting Lab 01](https://codespaces.new/summersbyu/ai-course-distribution-examples/tree/pilot-expense-sql-lab?quickstart=1). Continue on page 2.

**Cost checkpoint.** This lab uses GitHub computing resources. Personal accounts include a monthly allowance, but prior usage can reduce what you have available. Do not add a payment method or upgrade a plan to complete this exercise. If GitHub requests payment, reports exhausted usage, or blocks creation, contact the instructor for the alternate exercise.

### Your working notes

GitHub username: ____________________

Workspace name: ____________________

Lab ID: ____________________

Keep this handout beside your browser. The next page explains the two screens you will encounter.

<!-- PAGEBREAK -->

## Open your personal workspace

### First launch

1. On the start page, check the repository is **summersbyu/ai-course-distribution-examples** and the branch is **pilot-expense-sql-lab**. If a configuration choice appears, select **Accounting Lab 01**. Use **2 cores** if a machine choice appears.
2. Check that the usage will be charged to your own account. Choose **Create codespace** once. Wait for setup to finish; do not create another workspace because the first one seems slow.
3. You will see a workspace editor with files on the left. The prepared lab installs and starts automatically. Allow several minutes on the first launch. You do not type setup commands.
4. A separate browser tab should open with **Accounting Lab 01**. If GitHub offers **Open in Browser**, select it. Keep the workspace editor tab open as well.
5. In the lab tab, choose **Start here**. Record the workspace name and Lab ID shown in its left menu.

### If the lab tab does not open

In the workspace editor choose **View > Open View > Ports**. You can also select an already visible **Ports** tab near the bottom. Find **Accounting Lab** on port **8501**, then choose its **Open in Browser** icon. Keep port visibility **Private**. A port is simply the address through which you open this running app.

If the menu bar is hidden, open the menu at the upper left. If setup shows an error or no lab appears after about ten minutes, use the help steps on page 8. You are not expected to repair installation commands.

### Know which screen you are using

| Screen | What it does | What you do here |
| --- | --- | --- |
| GitHub repository | Holds the supplied exercise files | Launch the prepared workspace |
| Workspace editor | Runs your personal copy of the lab | Open the lab and manage the workspace |
| Accounting Lab browser tab | Presents the exercise interface | Enter expenses, write SQL, save evidence |

The lab menu contains **Start here**, **Enter expenses**, **SQL practice**, **Save and resume**, and **Help**. All accounting and SQL work takes place in this menu.

**Returning later.** Use My Codespaces and click the workspace name you recorded. The start link can also offer **Resume this codespace**. Choose the existing workspace rather than **Create a new one**. A new workspace starts with separate, empty data.

<!-- PAGEBREAK -->

## Understand the records before querying them

### The accounting case

You are reviewing expense records entered by a fictional accounting team. You will ask which expenses exceed $100, how much was spent in total, and how much belongs to each category. These records are practice data, not approved journal entries or evidence of actual purchases.

### Four terms you will use

| Term | Meaning in this lab |
| --- | --- |
| Database | The saved collection of records in your workspace |
| Table | A set of records with the same columns; ours is expenses |
| Row | One saved expense |
| Column | One type of information, such as vendor or amount |

The form writes records into an SQLite database. SQL is the language you use to ask questions about those records. Streamlit is the software that presents the form and query editor in your browser.

### Your table

| Column | Meaning | Example |
| --- | --- | --- |
| id | Unique record number | 1 |
| expense_date | Date in YYYY-MM-DD format | 2026-09-15 |
| vendor | Vendor name | Campus Office Supply |
| category | Expense classification | Office supplies |
| amount_cents | Amount stored as whole cents | 12550 |

**Why cents?** Whole cents make money storage exact for this exercise. $125.50 is stored as 12550. Divide by **100.0** to display dollars. The decimal point matters: dividing integers by 100 can discard cents in SQLite.

### Read your first query

```sql
SELECT vendor, amount_cents / 100.0 AS amount_dollars
FROM expenses;
```

**SELECT** chooses what to display. **FROM expenses** names the table. **AS amount_dollars** gives the calculated column a readable label. This query reads existing records; it does not change them.

**Working habit.** Before every query, write a short prediction in the app. After running it, compare the result with your prediction and check the arithmetic or rows independently. An answer can be syntactically valid and still answer the wrong accounting question.

<!-- PAGEBREAK -->

## Enter and inspect three expenses

### Enter the records

Choose **Enter expenses**. Use **September 15, 2026** for all three records. Enter each row below and click **Save expense** once. Check it appears in **Saved expenses** before continuing.

| Vendor | Category | Amount in dollars |
| --- | --- | --- |
| Campus Office Supply | Office supplies | 125.50 |
| Mountain Travel | Travel | 300.00 |
| Ledger Software | Software | 49.99 |

Do not enter dollar signs in the amount field. If you save a duplicate or an incorrect amount, note its ID and use Help. Do not delete the workspace or enter negative expenses to hide the mistake.

### Query 1 Inspect the records

Choose **SQL practice**. In **My prediction**, describe the three rows you expect. Replace the SQL box with this query and choose **Run query**.

```sql
SELECT vendor, category,
       amount_cents / 100.0 AS amount_dollars
FROM expenses
ORDER BY id;
```

**Check.** You should see the three vendors, categories, and amounts you entered. ORDER BY id puts the records in entry order. The app saves your successful query and prediction for your evidence file.

### Query 2 Find expenses above 100 dollars

Predict which vendors will appear. Then run:

```sql
SELECT vendor,
       amount_cents / 100.0 AS amount_dollars
FROM expenses
WHERE amount_cents > 10000
ORDER BY amount_cents DESC;
```

**Explain.** WHERE keeps only qualifying records. 10000 means $100 in cents. DESC sorts from largest to smallest. Why is the software expense excluded? Would an expense of exactly $100 appear with this condition?

Write your explanation in your notes; you will include it in the final reflection.

<!-- PAGEBREAK -->

## Reconcile totals and add a fourth expense

### Query 3 Calculate the initial total

Add the three amounts using a calculator or spreadsheet first. Record your prediction, then run:

```sql
SELECT COUNT(*) AS expense_count,
       SUM(amount_cents) / 100.0 AS total_dollars
FROM expenses;
```

COUNT(*) counts rows. SUM adds the stored cents before converting the total to dollars. Compare the count and total with your form records and independent calculation.

### Query 4 Summarize by category

Predict the category totals, then run:

```sql
SELECT category, COUNT(*) AS expense_count,
       SUM(amount_cents) / 100.0 AS total_dollars
FROM expenses
GROUP BY category
ORDER BY category;
```

GROUP BY produces one row for each category. Add the category totals and reconcile them to Query 3. A grouped query may return three rows even though it summarizes many expense records.

### Change the data and check again

Return to **Enter expenses**. Save a fourth expense: **Campus Office Supply**, **Office supplies**, **$25.00**, dated **September 15, 2026**.

Return to **SQL practice**. Predict the new count and total. Rerun Query 3, then predict and rerun Query 4. These are two additional saved query runs. Explain which category changed and why.

### Independent SQL task

Write a query that displays the number of **Software** expenses and their total dollars. Use SELECT, COUNT(*), SUM, FROM, and WHERE. Put the category text in single quotes, as in **'Software'**. Record your prediction before running it.

**Accounting judgment.** Does a correct total prove the expenses are legitimate, properly classified, and approved? Name two documents or checks you would still want. Include your answer in your reflection.

<!-- PAGEBREAK -->

## Save evidence before stopping

Choose **Save and resume**. Its current count and total provide a second view of your saved database.

### Save your reflection

In **Reflection**, answer these questions in your own words, then click **Save reflection**:

1. What do SELECT, WHERE, SUM, and GROUP BY do in this exercise?
2. Why is $100 represented by 10000? Why did we divide by 100.0?
3. How did you independently check the initial and updated totals?
4. Which category changed after the fourth expense? How much did it change?
5. What additional support or review is needed before treating these records as valid accounting expenses?

Leave **Restart observation** blank until you actually complete the restart test on page 7. Unsubmitted text is not saved; use the button before moving away.

### Download your work

1. Click **Save restart checkpoint**. Record its expense count and total below.
2. Click **Download expense backup CSV**. Save the file in a folder you can find on your laptop.
3. Click **Download lab evidence**. Save this file in the same folder. A filename ending in .md is a text document; it can be opened with a text editor or uploaded as evidence.
4. Confirm both downloaded files are present. The CSV backs up expenses. The evidence file records your successful SQL queries, predictions, results, reflection, and restart observation.

| Before stopping | Your value |
| --- | --- |
| Workspace name | ____________________ |
| Lab ID | ____________________ |
| Expense count | ____________________ |
| Total dollars | ____________________ |

**Saving is different from publishing.** Your SQLite records are saved in your Codespace. They are not automatically uploaded as changes to the GitHub repository. Downloads give you copies outside the Codespace. Your lab URL is private and temporary; submit downloaded evidence rather than using that URL as a public project link.

**Data rule.** Use only the fictional transactions in this handout. Do not enter real client, employer, financial account, or personal data.

<!-- PAGEBREAK -->

## Stop and resume the same workspace

### Perform the restart test

1. Keep the downloaded files from page 6. Open [My Codespaces](https://github.com/codespaces).
2. Find the exact workspace name you recorded. Open its **...** menu and choose **Stop codespace**. Closing the browser tab is not the same action.
3. Wait until the workspace shows it is stopped or offers to resume. Click that same workspace name to open it again. Do not create a new workspace.
4. The prepared lab should start automatically. If its tab does not open, use **Ports > Accounting Lab > Open in Browser** in the editor. Keep visibility Private.
5. In the lab, compare your **Lab ID** with your notes. Choose **Enter expenses** and check the records. Choose **Save and resume** and compare the current count and total with the saved checkpoint.
6. Enter your actual before and after observations in **Restart observation**, then click **Save reflection**. Download **lab evidence** again so your final file includes this observation.

### Record what happened

Same Lab ID before and after: ____________________

Expense count before and after: ____________________

Total dollars before and after: ____________________

If the values differ, describe what you did and ask for help. Do not report a successful restart simply because the app opened.

### What this demonstrates

The app process starts again, while its committed SQLite records remain in the workspace. This is a test of persistence in the same Codespace. It does not prove that a different hosting service will preserve local database changes.

Stopped workspaces can eventually be automatically deleted under GitHub retention settings. Keep the downloaded CSV and evidence. Do not choose **Delete codespace** until your work has been submitted and you are ready to remove that workspace.

### Finish

Submit your final **lab-01-evidence.md** and **lab-01-expenses.csv** through the location your instructor provides. If no submission location has been assigned during a colleague trial, keep both files and show them to the person running the trial.

Stop the Codespace again after your final downloads. Verify its stopped status in My Codespaces.

<!-- PAGEBREAK -->

## Help and completion check

### If something goes wrong

- **GitHub asks for payment or says usage is exhausted.** Stop here and contact the instructor. Do not upgrade a plan for this lab.
- **The workspace editor appears, but the lab does not.** Use View > Open View > Ports and open Accounting Lab on 8501. Allow setup to finish first.
- **The lab is empty after returning.** Compare your workspace name and Lab ID. Resume the original workspace in My Codespaces. A new workspace has separate data.
- **The lab still will not open after resuming.** In the editor choose Terminal > Run Task > Restart Accounting Lab. Choose the named task once; no command typing is needed. If it fails, send the instructor the visible error and workspace name. Never send a password or verification code.
- **A SQL query fails.** Check expenses, column spellings, commas, and single quotes around text. Run one query at a time. The SQL editor cannot change the saved expense records.
- **A count or total is unexpected.** Inspect the saved table for missing records, duplicates, incorrect amounts, or extra test records. Note the record IDs and ask the instructor for help.
- **The original workspace was deleted.** If necessary, open a new prepared workspace. In Save and resume, expand Restore a backup into an empty lab, upload your downloaded CSV, confirm, and restore. Only expenses are recovered; earlier query runs and reflections remain in your evidence download.

### Self check

| Check | Expected after following the case exactly |
| --- | --- |
| Initial records | 3 expenses totaling $475.49 |
| Expenses above $100 | Travel $300.00 and supplies $125.50 |
| After the fourth entry | 4 expenses totaling $500.49 |
| Updated office supplies | 2 expenses totaling $150.50 |
| Software task | 1 expense totaling $49.99 |

### Completion checklist

- I saved the four fictional records and reconciled their totals.
- I recorded predictions and ran the six guided query runs plus my Software query.
- I explained the SQL and the limits of the accounting evidence.
- I performed an actual stop and resume and recorded what I observed.
- I downloaded final evidence and a CSV backup, and stopped my workspace.

**Next lesson.** We will query related tables using joins and examine how duplicate matches can distort accounting totals. AI assistance comes after you can explain and check the query yourself.

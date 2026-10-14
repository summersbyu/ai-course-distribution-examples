"""Student-facing accounting lab. No terminal or AI credentials required."""
from datetime import date
import json
import os
import pandas as pd
import streamlit as st
import lab

st.set_page_config(page_title="Accounting Lab 01", page_icon="🧾", layout="wide")
lab.initialize()
STARTER = """SELECT vendor,
       category,
       amount_cents / 100.0 AS amount_dollars
FROM expenses
ORDER BY id;"""
with st.sidebar:
    st.title("Accounting Lab 01")
    page = st.radio("Choose a section", ["Start here", "Enter expenses", "SQL practice", "Save and resume", "Help"], key="section")
    st.caption(f"Lab ID: {lab.meta('lab_id')}")
    workspace = os.environ.get("CODESPACE_NAME", "local practice")
    st.caption(f"Workspace: {workspace}")
    st.link_button("My Codespaces", "https://github.com/codespaces")
    st.caption("Use fictional transactions only. This lab does not call an AI service.")

st.title(page)

if page == "Start here":
    st.write("Record fictional expenses, ask questions with SQL, and check that your data survives stopping and resuming your workspace.")
    st.subheader("What you will learn")
    st.markdown("1. Save a transaction through a form.\n2. Read a table with SELECT, filter with WHERE, and total with SUM.\n3. Predict and independently check results.\n4. Export evidence and resume the same workspace.")
    st.subheader("Before you begin")
    st.write("Keep the workspace editor tab and this lab tab open. You work in this lab tab. No terminal commands, software installation, Claude account, or API key are needed for the exercise.")
    st.write("Write down the workspace name and Lab ID shown on the left. They help you return to your saved work.")
    st.subheader("A small accounting case")
    st.write("You are reviewing four expense records for a fictional accounting team. First enter three records dated September 15, 2026. Query them, then add the fourth and reconcile the new total.")
    st.table(pd.DataFrame([
        ["Campus Office Supply", "Office supplies", "$125.50"],
        ["Mountain Travel", "Travel", "$300.00"],
        ["Ledger Software", "Software", "$49.99"],
    ], columns=["Vendor", "Category", "Amount"]))
    st.info("Next: choose Enter expenses in the left menu. Save each record once.")

elif page == "Enter expenses":
    st.write("Use September 15, 2026 for the exercise date. Save each fictional expense once.")
    with st.form("expense_form", clear_on_submit=True):
        expense_date = st.date_input("Expense date", value=date(2026, 9, 15), key="expense_date")
        vendor = st.text_input("Vendor", max_chars=100, key="vendor")
        category = st.selectbox("Category", lab.CATEGORIES, key="category")
        amount = st.number_input("Amount in dollars", min_value=0.01, max_value=1000000.0, value=0.01, step=0.01, format="%.2f", key="amount")
        submitted = st.form_submit_button("Save expense", type="primary")
    if submitted:
        try:
            identifier = lab.add_expense(expense_date.isoformat(), vendor, category, amount)
            st.success(f"Expense {identifier} saved. Check it in the table below before entering another.")
        except ValueError as error:
            st.error(str(error))
    st.subheader("Saved expenses")
    rows = lab.expenses()
    if rows:
        frame = pd.DataFrame(rows, columns=["ID", "Date", "Vendor", "Category", "Amount in cents"])
        frame["Amount in dollars"] = frame.pop("Amount in cents") / 100
        st.dataframe(frame, hide_index=True, width="stretch",
                     column_config={"Amount in dollars": st.column_config.NumberColumn(format="$%.2f")})
    else:
        st.info("No expenses saved yet. Use the form above to add your first one.")
    st.caption("If you see a duplicate or a wrong amount, use Help and ask the instructor. Do not delete your workspace.")

elif page == "SQL practice":
    st.write("SQL asks a database a question. Predict the result, run your query, and explain what the result means.")
    with st.expander("Table and column guide", expanded=True):
        st.write("Table name: expenses. Each row is one expense.")
        st.table(pd.DataFrame([
            ["id", "Unique record number"], ["expense_date", "Date stored as YYYY-MM-DD"],
            ["vendor", "Vendor name"], ["category", "Expense category"],
            ["amount_cents", "Amount as whole cents; divide by 100.0 for dollars"],
        ], columns=["Column", "Meaning"]))
    with st.form("sql_form"):
        prediction = st.text_area("My prediction", placeholder="What rows or total do you expect, and why?", key="prediction", max_chars=2000)
        sql = st.text_area("SQL query", value=STARTER, height=190, key="sql", max_chars=12000)
        run = st.form_submit_button("Run query", type="primary")
    if run:
        try:
            if not prediction.strip():
                raise ValueError("Record your prediction first. It can be a short sentence.")
            columns, rows, truncated = lab.query(sql, prediction)
            st.session_state.last_result = (columns, rows, truncated)
            st.success("Query completed. Your prediction, SQL, and result are saved in your evidence.")
        except ValueError as error:
            st.session_state.pop("last_result", None)
            st.error(str(error))
    if "last_result" in st.session_state:
        columns, rows, truncated = st.session_state.last_result
        st.subheader("Query result")
        st.dataframe(pd.DataFrame(rows, columns=columns), hide_index=True, width="stretch")
        st.caption("Showing the first 500 rows." if truncated else f"{len(rows)} row(s) returned. Compare with your prediction.")
    with st.expander("SQL reference"):
        st.markdown("- **SELECT** chooses columns or calculations.\n- **FROM** names the table.\n- **WHERE** keeps rows that meet a condition.\n- **ORDER BY** sorts results; DESC puts larger amounts first.\n- **SUM** adds amounts; COUNT(*) counts rows.\n- **GROUP BY** produces one result per category.")
    st.caption("The editor permits one read-only query. Saved expenses cannot be changed here. Queries have a time limit and a 500-row display limit.")

elif page == "Save and resume":
    count, total = lab.summary()
    st.write(f"Your database currently contains {count} expenses totaling ${total / 100:,.2f}.")
    st.subheader("Record what you learned")
    with st.form("reflection_form"):
        reflection = st.text_area("Reflection", value=lab.meta("reflection"), height=140,
            help="Explain SELECT, WHERE, and SUM; why amounts are stored in cents; and how you checked your results.", key="reflection_input", max_chars=6000)
        observation = st.text_area("Restart observation", value=lab.meta("restart_observation"),
            placeholder="After the actual stop/resume test, record before and after counts, totals, and Lab ID.", key="restart_input", max_chars=2000)
        if st.form_submit_button("Save reflection"):
            lab.save_meta("reflection", reflection)
            lab.save_meta("restart_observation", observation)
            st.success("Reflection saved to your database.")
    st.subheader("Before stopping your workspace")
    if st.button("Save restart checkpoint"):
        saved_count, saved_total = lab.save_checkpoint()
        st.success(f"Checkpoint saved: {saved_count} expenses, ${saved_total / 100:,.2f}.")
    checkpoint = lab.meta("checkpoint")
    if checkpoint:
        saved = json.loads(checkpoint)
        st.write(f"Saved checkpoint: {saved['count']} expenses, ${saved['cents'] / 100:,.2f}. Compare these with the current database after resuming.")
    st.download_button("Download expense backup CSV", lab.export_csv(), "lab-01-expenses.csv", "text/csv")
    st.download_button("Download lab evidence", lab.evidence(), "lab-01-evidence.md", "text/markdown")
    st.write("Download both files before stopping. The CSV backs up expenses; the evidence file contains saved query runs and reflections. Download again after recording your restart observation.")
    st.subheader("Stop and return")
    st.markdown("1. Open **My Codespaces** from the left menu.\n2. Find your recorded workspace name and choose **... > Stop codespace**. Closing this tab alone does not stop it.\n3. Click that same workspace name to resume.\n4. The lab should start automatically. If its tab does not open, use **Ports > Accounting Lab > Open in Browser** in the editor.\n5. Compare the Lab ID, expense count, and total. Then save your restart observation here.")
    with st.expander("Restore a backup into an empty lab"):
        st.write("First look for your original workspace. Use this only if you must recover expenses into a new, empty lab. CSV recovery does not restore prior query runs or reflections.")
        uploaded = st.file_uploader("Choose your lab expense backup CSV", type="csv")
        confirm = st.checkbox("I checked My Codespaces and want to restore into this empty lab.")
        if st.button("Restore expenses", disabled=not (uploaded and confirm)):
            try:
                restored = lab.restore_csv(uploaded.getvalue())
                st.success(f"Restored {restored} expenses. Choose Enter expenses to inspect them.")
            except ValueError as error:
                st.error(str(error))

elif page == "Help":
    st.subheader("If the editor opens instead of the lab")
    st.write("The editor holds your workspace; the lab is a separate browser tab. In the editor choose View > Open View > Ports, find Accounting Lab (8501), and choose its Open in Browser icon. Keep visibility Private.")
    st.subheader("If the lab is empty")
    st.write("Check your Lab ID and workspace name against your notes. Open My Codespaces and resume the original workspace. A new workspace has its own empty database.")
    st.subheader("If a SQL query fails")
    st.write("Check the table name expenses, column names, commas, and single quotes around text. Amounts are cents: $100 is 10000 cents. Failed queries do not change expenses.")
    st.subheader("If you entered a wrong or duplicate expense")
    st.write("Ask the instructor to correct the identified record. Keep your workspace. For now, note the mistake and explain its effect on your total.")
    st.subheader("If the lab will not open after resuming")
    st.write("In the editor choose Terminal > Run Task > Restart Accounting Lab. This is a named menu action; you do not type a command. Try once, then contact the instructor with the visible error and your workspace name.")
    st.subheader("What stays saved")
    st.write("Expenses, successful query runs, saved reflections, and checkpoints are stored in SQLite in your workspace. Unsubmitted text is not saved. Stopping is different from deleting. Inactive workspaces can eventually be automatically deleted, so keep downloaded backups.")

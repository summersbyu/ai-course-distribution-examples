"""AI SQL Analyst: ask a question in plain English, see the SQL, see the answer.

Developer-stage example for the BYU AI course. The data is synthetic.
Key safety is the point of this example:
  - The API key lives in Streamlit secrets, never in the code or the repository.
  - If the owner sets APP_PASSWORD, visitors must enter it before using the owner's key.
  - If no key is configured, visitors paste their own key, which is kept only for their session.
"""
import json
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from sql_guard import UnsafeSQL, run_readonly, schema_text

DB_PATH = Path(__file__).parent / "data" / "summit_outfitters.db"
MODELS = {"Claude Haiku 5.5 (cheapest)": "claude-haiku-5-5", "Claude Sonnet 5.5": "claude-sonnet-5-5"}
SAMPLE_QUESTIONS = [
    "Which 5 customers had the highest total sales in 2026?",
    "What is total open accounts receivable by region?",
    "List vendor bills that have no approver.",
    "Are there vendor bills with the same vendor, date, and amount?",
    "Which paid invoices were short-paid, and by how much?",
]

st.set_page_config(page_title="AI SQL Analyst", page_icon="🧾", layout="wide")


def secret(name: str):
    try:
        return st.secrets.get(name)
    except Exception:  # no secrets file at all
        return None


# ---------- Access and key handling ----------
owner_key = secret("ANTHROPIC_API_KEY")
app_password = secret("APP_PASSWORD")

with st.sidebar:
    st.header("Access")
    if owner_key and app_password:
        entered = st.text_input("Class password", type="password")
        if entered != app_password:
            st.info("Enter the class password to use this app.")
            st.stop()
        api_key = owner_key
        st.success("Using the app owner's API key.")
    elif owner_key:
        api_key = owner_key
        st.warning("This app uses its owner's key with no password. Anyone with the link spends the owner's credit.")
    else:
        api_key = st.text_input("Your Anthropic API key", type="password",
                                help="Kept only for this browser session. Never stored or logged.")
        if not api_key:
            st.info("Paste your own API key to ask questions. You can still browse the schema.")
    model_label = st.selectbox("Model", list(MODELS))
    st.caption("Data: Summit Outfitters, a synthetic company. No real data.")

st.title("🧾 AI SQL Analyst")
st.write("Ask a question about Summit Outfitters' sales, receipts, and vendor bills. "
         "The app shows the SQL it wrote so you can check it before you trust the answer.")

schema = schema_text(DB_PATH)
with st.expander("Database schema"):
    st.code(schema, language="sql")

if "question" not in st.session_state:
    st.session_state.question = ""
cols = st.columns(len(SAMPLE_QUESTIONS))
for c, q in zip(cols, SAMPLE_QUESTIONS):
    if c.button(q, use_container_width=True):
        st.session_state.question = q
question = st.text_area("Your question", key="question", height=80)

SYSTEM = f"""You are an accounting data analyst who writes SQLite SQL.
Write ONE read-only SELECT query that answers the user's question using only this schema:

{schema}

Rules:
- SQLite dialect. Dates are TEXT in YYYY-MM-DD form; use strftime or string comparison.
- Exclude invoices with status 'Void' from sales totals unless the user asks about voids.
- Invoice totals are SUM(quantity * unit_price) from invoice_lines.
- Round money to 2 decimals. Give columns readable aliases.
- If the question cannot be answered from this schema, return sql as an empty string and explain why.

Respond with only a JSON object: {{"sql": "...", "explanation": "one or two plain-English sentences on how the query answers the question", "check": "one way a person could verify the result independently"}}"""


def ask_claude(q: str, key: str, model: str) -> dict:
    import anthropic  # imported here so the page loads even before a key is entered

    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(model=model, max_tokens=1000, system=SYSTEM,
                                 messages=[{"role": "user", "content": q}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("The model did not return JSON. Try rephrasing the question.")
    out = json.loads(match.group(0))
    out["usage"] = {"input_tokens": msg.usage.input_tokens, "output_tokens": msg.usage.output_tokens}
    return out


if st.button("Ask", type="primary", disabled=not (api_key and question.strip())):
    with st.spinner("Writing SQL..."):
        try:
            result = ask_claude(question.strip(), api_key, MODELS[model_label])
        except Exception as e:  # show the error without exposing the key
            st.error(f"The AI request failed: {type(e).__name__}. Check the key and try again.")
            st.stop()

    if not result.get("sql"):
        st.warning(result.get("explanation", "The question can't be answered from this data."))
        st.stop()

    st.subheader("1. The SQL the AI wrote")
    st.code(result["sql"], language="sql")
    st.caption(result.get("explanation", ""))

    st.subheader("2. The result")
    try:
        columns, rows, truncated = run_readonly(DB_PATH, result["sql"])
        st.dataframe(pd.DataFrame(rows, columns=columns), use_container_width=True)
        st.caption(f"{len(rows)} rows" + (" (showing the first 500)" if truncated else ""))
    except UnsafeSQL as e:
        st.error(f"Blocked by the safety check: {e}")
    except Exception as e:
        st.error(f"The query failed to run: {e}")

    st.subheader("3. Before you trust it")
    st.info(f"**Verify independently:** {result.get('check', 'Recompute the answer another way.')}")
    u = result["usage"]
    st.caption(f"Tokens used: {u['input_tokens']} in, {u['output_tokens']} out. Each question spends a small amount of API credit.")

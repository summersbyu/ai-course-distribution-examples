# Stage 4 · Developer: AI SQL Analyst (Streamlit)

A working app that turns a plain-English question into SQL, shows the SQL, runs it on a
read-only copy of a synthetic company's database, and tells the user how to verify the answer.

**Why this stage needs hosting:** the app holds a secret (an API key) and runs Python on a server.
A Google Drive file or a static web page cannot do either.

## What's in the folder

| File | Purpose |
| --- | --- |
| `app.py` | The Streamlit app |
| `sql_guard.py` | Safety checks: one SELECT only, blocked keywords, read-only connection, 500-row cap |
| `test_sql_guard.py` | Tests for the safety checks (`python test_sql_guard.py`) |
| `build_db.py` | Rebuilds `data/summit_outfitters.db`, the synthetic database |
| `.streamlit/secrets.toml.example` | What goes in Streamlit's Secrets box. Never commit the real file. |

The data includes a few planted exceptions for students to find: vendor bills with no approver,
duplicate-looking vendor bills, and short-paid invoices.

## Run it on your laptop

```bash
pip install -r requirements.txt
streamlit run app.py
```

With no secrets file, the app asks each visitor for their own API key.

## Deploy it on Streamlit Community Cloud (about 5 minutes)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app** > **Deploy a public app from GitHub**.
3. Repository: this repo. Branch: `main`. Main file path: `4-developer/sql-analyst/app.py`.
4. Choose one of three key setups:
   - **Visitors bring their own key** (safest, no setup): add no secrets.
   - **Your key, password-protected** (recommended for class demos): open **Advanced settings** > **Secrets**
     and paste both lines from `secrets.toml.example`, with your real key and a password.
   - **Your key, no password**: only `ANTHROPIC_API_KEY`. Anyone with the link spends your credit. Avoid.
5. Click **Deploy**.

## The key-safety lesson in five rules

1. A key never goes in code, a notebook, a screenshot, or a GitHub commit.
2. It lives in a secrets store (Streamlit Secrets here; environment variables elsewhere).
3. Set a monthly spend limit on the API account, so a leak can only cost so much.
4. A public app that uses your key needs a password, or visitors should bring their own key.
5. If a key ever leaks, revoke it in the Anthropic Console and create a new one. That takes a minute.

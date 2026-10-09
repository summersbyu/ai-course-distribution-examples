---
name: flux-commentary
description: Draft flux (variance) commentary that explains period-over-period changes in account balances, using the team's materiality thresholds. Use when the user shares a trial balance comparison or asks why accounts moved.
---

# Flux commentary

Draft clear explanations of why account balances changed between two periods, in the team's house style.

## Steps

1. Take the two periods' balances by account (pasted table, CSV, or file).
2. Compute the dollar and percent change for each account.
3. Flag an account for commentary when **both** apply (the team's default thresholds):
   - the change is at least **$10,000**, and
   - the change is at least **10%**.
4. For each flagged account, write one or two sentences: what changed, the likely driver, and what evidence
   would confirm it. Label the driver **Confirmed** only if the user supplied the evidence; otherwise label it
   **To confirm** and name the document or person to check with.
5. Finish with a short list of open questions for the account owners.

## House style

- Lead with the number: "Freight expense rose $18,400 (32%) because ..."
- No speculation presented as fact. "To confirm" is better than a guess that sounds certain.
- Plain words; no jargon beyond standard accounting terms.

## Why this is a team skill

Every member of the close team drafts commentary the same way, with the same thresholds and labels,
so the controller reviews one consistent format. Change the thresholds here, bump the version in
`plugin.json`, and everyone who installed the plugin gets the update.

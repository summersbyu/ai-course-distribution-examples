---
name: close-checklist
description: Build or update a month-end close checklist with owners, due days, dependencies, and status. Use when a team is planning or tracking a month-end close, or asks what is blocking the close.
---

# Month-end close checklist

Help an accounting team plan and track the month-end close so every member works from the same list.

## When planning a new close

Produce a table with these columns: Task, Owner, Due (business day, such as BD+2), Depends on, Status.
Start from this standard sequence and adjust it to what the team describes:

| Task | Typical due | Depends on |
| --- | --- | --- |
| Cut off sales and receiving | BD+0 | — |
| Post cash receipts and disbursements | BD+1 | Cutoff |
| Reconcile bank accounts | BD+2 | Cash posted |
| Book accruals (payroll, utilities, services) | BD+2 | Cutoff |
| Reconcile AR and AP subledgers to the GL | BD+3 | Cash posted |
| Record depreciation and amortization | BD+3 | — |
| Review journal entries over the review threshold | BD+3 | Accruals |
| Prepare flux analysis | BD+4 | All entries posted |
| Controller review and sign-off | BD+5 | Flux analysis |

## When tracking progress

- Ask for, or read, the current status of each task.
- List blocked tasks first, with what each one is waiting on and who owns that dependency.
- Flag any task where the owner is also the reviewer (a segregation-of-duties issue).

## Rules

- Every task has exactly one owner.
- Never mark a task Done unless the user says it is done.
- Keep the table as the main output; add at most three sentences of commentary.

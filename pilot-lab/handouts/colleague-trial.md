# Accounting Lab colleague trial

## Test the student experience from a fresh start

This trial tests whether an unfamiliar user can launch the prepared lab, complete the accounting and SQL work, and recover the same saved records without terminal coaching. A functioning app alone is not a successful trial.

One colleague trial is a usability check, not evidence of readiness for 390 students. Follow it with a representative 15 to 20 person pilot across Windows, Mac, unfamiliar accounts, and the campus network.

### Before the session

The instructor must first complete the live readiness checks in the instructor guide. Reserve about 60 minutes, with extra time if the participant needs a new GitHub account. Use the colleague's own laptop, browser, and account. An instructor's already configured workspace is not an onboarding test.

Give the participant **only the student handout** at the start. Keep the instructor guide and answer key out of view. The participant may use the handout and the lab Help page. Do not send a pre-opened lab URL as a substitute for launching their own workspace.

### Instructions to the participant

Work through the student handout as if you were a student new to GitHub and SQL. Say what you expect to happen before each action. If a step is confusing, describe what you see and where you would click. Do not guess at payment, deletion, or account sharing prompts. Keep your login credentials private.

### Instructions to the observer

1. Record the participant's browser, operating system, prior GitHub experience, and whether the account is new. Observe without pointing to controls.
2. Start timing when the participant opens GitHub. Record account verification separately from workspace launch time.
3. At each checkpoint below, record **Unassisted**, **Used handout Help**, or **Observer intervention**. Note the exact confusing words or screen.
4. If the participant cannot make progress for two minutes, ask what they are looking for. If you intervene, record the intervention rather than treating the checkpoint as unassisted.
5. Stop the trial for billing demands, unexpected data exposure, or an unrecoverable launch error. Preserve the error message. Do not improvise terminal repairs during the student trial.

### Participant record

Participant: ____________________  Date: ____________________

Operating system and browser: ____________________

Prior GitHub experience: None / Limited / Regular

Account setup time: ______  Workspace launch time: ______

Total exercise time: ______  Number of observer interventions: ______

<!-- PAGEBREAK -->

## Observe the checkpoints and make a decision

| Checkpoint | Outcome and elapsed time |
| --- | --- |
| Signs in with own account and finds launch link | ____________________ |
| Opens the lab without typing setup commands | ____________________ |
| Distinguishes editor from lab and records Lab ID | ____________________ |
| Saves three expenses and finds the saved table | ____________________ |
| Predicts and runs the filter and total queries | ____________________ |
| Explains cents and the changed category total | ____________________ |
| Writes the Software query with the reference | ____________________ |
| Downloads evidence and expense backup | ____________________ |
| Stops and resumes the same workspace | ____________________ |
| Confirms matching data and stops after finishing | ____________________ |

### Ask after the exercise

1. Which step was hardest to understand, and what wording would have helped?
2. Could you explain the difference between a saved database, the source repository, and a downloaded backup?
3. What does WHERE amount_cents > 10000 mean? Would an expense of exactly $100 appear?
4. Did the app help you learn SQL, or did you mainly copy text? What would improve that balance?
5. Would you feel comfortable repeating this with only the handout? Why or why not?

### Suggested pilot acceptance criteria

- The participant reaches the lab with no terminal typing, payment change, credential sharing, or observer setup intervention.
- The participant correctly interprets the filter and totals, rather than only matching the answer key.
- Saved records and Lab ID match after an actual stop and resume.
- Both evidence files are downloaded and the final workspace is stopped.
- Any UI fallback is completed using the handout. Repeated observer intervention means the workflow needs revision before a larger pilot.

**Decision:** Proceed to a broader pilot / Revise and repeat / Choose a different environment

Reason and highest priority change: ______________________________________


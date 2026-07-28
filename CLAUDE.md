# PhishGuard (CAI2C08 MLDP) — working rules

**Read `PROGRESS.md` first, before any other file or tool call.** It records the exact
stage the last session stopped at, what is committed, and the next action. Do not start
work from the guideline alone — it describes the target, not the current state.

**Before ending a work chunk** (or if a session looks like it may be cut short):
update `PROGRESS.md` §Current state, §Next action, §Decision log — then commit. A stage
is only "done" if there is a commit for it.

Source of truth, in priority order:
1. `CAI2C08 MLDP Apr 2026 Sem - Project Specification (1).pdf` — the graded spec/rubric.
2. `MLDP Program Codes Submission Template.ipynb` — prescribed notebook section numbering.
3. `PHISHGUARD_GUIDELINE.md` — my build plan. Where it conflicts with 1 or 2, the spec wins.

Hard constraints: scikit-learn only for models · `RandomizedSearchCV` only, exactly 2
hyperparameters, ≤3 values each · feature *selection* not engineering (say so explicitly)
· `random_state=42` everywhere · one commit per stage, real messages.

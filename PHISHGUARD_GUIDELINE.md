# PhishGuard — Build Guideline for Claude Code

**Module:** CAI2C08 MLDP | **Component:** Program Code (50%, due 31 Jul 5pm)
**Dataset:** UCI Phishing Websites (id=327) — 11,055 rows, 30 categorical features (-1/0/1), target `Result` (phishing/legitimate). Tutor-approved.
**Goal:** Hit A-band (≥80%) on every rubric row. A-band is earned by *depth and justification*, not just working code — read each section below before writing that part.

---

## Hard constraints — do not violate

- **scikit-learn ONLY** for model implementation. No XGBoost, LightGBM, imbalanced-learn, etc.
- **RandomizedSearchCV only** for tuning. Max 3 values per hyperparameter. Must tune **exactly 2 hyperparameters** on the best model, with logged before/after comparison.
- Do not fabricate "feature engineering" on already-engineered columns. These 30 features were pre-extracted by the original researchers from raw URLs/HTML — there is no raw URL string to engineer from. **Use feature selection, not engineering, and say so explicitly in the notebook** (this is honest and matches the "and/or" wording in the spec).
- Every code cell that does something non-trivial needs a markdown cell above it explaining *why*, not just what.
- Git commit after each major stage below (not one dump commit at the end) — commit history is graded.

---

## 1. Code Clarity & Documentation (8%)
- Organize notebook into clearly headed sections matching the stages below.
- Every preprocessing/modeling decision gets 1-3 sentences of rationale in markdown, not just a code comment.
- Consistent naming, no dead code, no unexplained magic numbers.
- Commit after: initial setup, EDA, feature selection, baseline models, tuning, final model. Six distinct commits minimum, each with a real message (not "update").

## 2. EDA & Interpretation (8%)
- Class balance plot for `Result` — state the imbalance ratio and what it means for metric choice (foreshadow section 5).
- Crosstab / stacked bar of each of the 30 features against `Result` (or at minimum the ~10-15 features feature selection later confirms as important) — categorical, so use crosstabs/bar charts, not histograms.
- Correlation heatmap on the encoded feature set.
- **For every plot, write 2-3 sentences interpreting it in security/business terms** — e.g. why would an absent SSL certificate or a suspiciously young domain age correlate with phishing, and what does that imply for which features the model should lean on. This is the single highest-leverage place to move from B to A — don't skip it or make it generic.

## 3. Model Diversity, Comparison & Selection (8%)
- Train **3 distinct algorithms**: LogisticRegression, RandomForestClassifier, GradientBoostingClassifier.
- Report test-set metrics for all three against a **majority-class baseline** (e.g. `DummyClassifier`).
- Present both quantitative (metrics table) and qualitative comparison (e.g. interpretability of LR vs RF, training time, overfitting risk from train/test gap).
- Justify the model you carry forward to tuning based on performance **and** interpretability/deployment needs — not just "highest accuracy."

## 4. Feature Selection with Rationale (10%)
- Use RandomForest feature importances **and** a statistical method (`SelectKBest` with mutual information, since features are categorical) — cross-check the two.
- Show a before/after: model trained on all 30 features vs. reduced feature set. Report whether performance held, improved, or traded off, and tie the decision to reduced complexity / deployment practicality for the app, not just to a metric number.
- Explicitly state in a markdown cell: "This project uses feature selection rather than feature engineering because [reason above]."

## 5. Hyperparameter Tuning (4%)
- RandomizedSearchCV on your selected model, 2 hyperparameters, ≤3 values each.
- Log the parameter grid, the search results table, and the best params found.
- Compare tuned vs. untuned (baseline) test performance explicitly — a table or printed diff, not just "the tuned model got X%."
- Confirm reproducibility: set and state `random_state` throughout.

## 6. Evaluation Metric Selection (4%)
- Justify metric choice against the class balance found in EDA and the business cost of errors: a missed phishing site (false negative) is worse than flagging a safe site (false positive), so lean toward **recall or F1** over raw accuracy — but state this reasoning explicitly, don't just assert it.
- Report the full picture (precision, recall, F1, confusion matrix), not just the single metric you optimize for.

## 7. Streamlit App (8% combined)
- Inputs limited to the features feature-selection identified as important (not all 30) — the UI should reflect that decision, reinforcing the app's design story.
- **Input validation + user-facing error messages** required for A-band — don't let the app silently fail or crash on bad input.
- Must be visibly interactive: prediction changes when inputs change, clear labeled output, no dead buttons.
- Clean, appropriate visual design — doesn't need to be fancy, needs to be legible and consistent (labels, spacing, no placeholder text left in).
- Take the 3 required screenshots directly from the deployed app once it's live: (1) before any option selected, (2) after selection showing a prediction, (3) after changing selection showing the prediction change.

## 8. Deliverables checklist (don't submit without these)
- [ ] Jupyter notebook (.ipynb) — code + documentation + analysis, all inline, runs top-to-bottom cleanly
- [ ] Streamlit app (.py)
- [ ] Word doc from template: Declaration of Originality (cite Claude Code use — allowed, doesn't cost marks), dataset source, GitHub link, Streamlit link, 3 screenshots, dev log screenshots (git history)
- [ ] Zipped as `<Name in TP-LMS>_2503051A.zip`, not RAR, verified not empty/corrupted before upload

## Note on Gen AI use
Per the module's Gen AI policy: assistance is fine, but you must be able to explain every modeling decision yourself at the Aug 17 demo, where you'll face live questions and a case challenge. Don't let Claude Code produce reasoning you can't personally defend — especially the metric justification (section 6) and feature selection rationale (section 4), since those are exactly the kind of thing a lecturer will probe in Q&A.

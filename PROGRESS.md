# PhishGuard — Session Resume State

**Purpose:** if a session dies mid-work (credits, crash, laptop), this file is the
only thing a fresh session needs to read to pick up exactly where it left off.

**Protocol — non-negotiable:**
1. At the **start** of every session: read this file top-to-bottom before touching anything.
2. At the **end** of every work chunk (and before any long-running step): update
   §Current state, §Next action, and §Decision log. Then `git commit`.
3. Never leave this file describing work that isn't committed. If it says a stage is
   done, the commit exists.

**Deadline:** Program Code — **31 Jul (Fri) 5.00pm** · Demo/slides — 17 Aug (Mon) 5.00pm
Late: <1 day −10% of 100 · 1–2 days −20% · ≥2 days zero.

---

## Current state

**Stage:** S0 — Setup (not started)
**Last commit:** _none — repo has no commits yet_
**Working files:** none created yet

Nothing has been built. The folder currently holds only source material:
`Training Dataset.arff`, `Phishing Websites Features.docx` (feature definitions),
the spec PDF, `MLDP Program Codes Submission Template.ipynb`, `PHISHGUARD_GUIDELINE.md`.

## Next action

Resolve the **GitHub repo question** (see §Open questions), then S0.

---

## Stage checklist

Tick only when committed. Each stage = one commit, message in the format
`S<n>: <what changed>` (the commit history is a graded 4% rubric row — see §Rubric map).

- [ ] **S0 Setup** — venv, `requirements.txt`, load `.arff` → DataFrame, `random_state=42`
      constant, notebook skeleton built on the *submission template's* section numbering
      (see §Notebook structure), Declaration of Originality filled in.
- [ ] **S1 Business understanding** — problem framing, cost-of-error argument written
      *before* modelling so the metric choice in S7 has something to point back to.
- [ ] **S2 EDA** — class balance, per-feature crosstabs, correlation heatmap.
      Every plot gets 2–3 sentences of security/business interpretation.
- [ ] **S3 Data prep** — dtype/missing checks, stratified train/test split.
- [ ] **S4 Baselines** — `DummyClassifier` + LogisticRegression + RandomForest +
      GradientBoosting on **all 30 features**. Metrics table saved to `artifacts/`.
- [ ] **S5 Feature selection** — RF importances × `SelectKBest(mutual_info_classif)`,
      cross-checked. Re-run the 3 models on the reduced set. Before/after table.
- [ ] **S6 Tuning** — `RandomizedSearchCV`, exactly 2 hyperparameters, ≤3 values each,
      on the selected model. Tuned vs untuned table.
- [ ] **S7 Final evaluation** — precision/recall/F1/confusion matrix, metric
      justification, assumptions stated. Model + feature list pickled to `artifacts/`.
- [ ] **S8 Streamlit app** — `app.py`, inputs = selected features only, input
      validation + user-facing error messages. Deployed, link recorded below.
- [ ] **S9 Submission** — Word doc (template), 3 screenshots, git-history screenshots,
      zip as `<Name in TP-LMS>_2503051A.zip`.

---

## Artifacts — where recomputable work is cached

Anything expensive gets written to `artifacts/` so a resumed session never re-runs it.

| File | Written by | Contains |
| --- | --- | --- |
| `artifacts/baseline_metrics.csv` | S4 | all-30-feature test metrics, 4 models + dummy |
| `artifacts/selected_features.json` | S5 | final feature list + why each survived |
| `artifacts/reduced_metrics.csv` | S5 | same models on reduced set (before/after pair) |
| `artifacts/search_results.csv` | S6 | full `cv_results_` table from RandomizedSearchCV |
| `artifacts/final_model.pkl` | S7 | fitted model the Streamlit app loads |

_(none exist yet)_

## Links

- GitHub repo: _TBD — see §Open questions_
- Streamlit app: _TBD_
- Dataset source: UCI Phishing Websites, id=327 — https://archive.ics.uci.edu/dataset/327/phishing+websites

---

## Decision log

Every modelling decision + **the reason**, recorded as it's made. This exists because
the 17 Aug demo is a live Q&A with a case challenge — the reasoning has to survive a
session boundary, not just the code.

| # | Decision | Reason | Stage |
| --- | --- | --- | --- |
| 1 | UCI Phishing Websites (id=327), 11,055 rows | Tutor-approved at Checkpoint 1; real (not synthetic), tabular, no text/images/time-series — meets spec's dataset rules | pre-S0 |
| 2 | Feature **selection**, not engineering | The 30 columns are already researcher-extracted from raw URLs/HTML; no raw URL string exists to engineer from. Spec says "and/or", so selection alone is compliant — but it must be stated explicitly in the notebook | pre-S0 |
| 3 | Load `Training Dataset.arff` — **never `.old.arff`** | `.old.arff` is a different file from the same UCI download: `@relation test`, only 2,456 rows, and it encodes binary features as **{0,1}** instead of {-1,1}. Loading it by mistake would silently invert/shift feature meanings with no error | pre-S0 |
| 4 | Metric argument rests on **cost asymmetry, not class imbalance** | Actual split is 6157 legitimate / 4898 phishing = 1.26:1 — near balanced, so imbalance does *not* rule out accuracy. The case for recall is that a false negative lands a user on a credential-harvesting page while a false positive costs one dismissed warning. Do **not** say "the data was imbalanced so I used recall" at the demo | pre-S0 |

## Open questions / blockers

1. **GitHub repo — blocking S0.** The vault repo (`C:\Brain\knowledgeable`) has *zero
   commits and no remote*. The submission needs a **public** GitHub link, and Streamlit
   Community Cloud deploys from a public repo. Publishing the whole vault to satisfy
   that would expose every module note. Needs a decision: separate repo for this project
   vs. something else.
2. Confirm exact **student name as it appears in TP-LMS** for the zip filename and the
   Declaration of Originality.

---

## Notebook structure (follow the submission template, not the guideline's headings)

`MLDP Program Codes Submission Template.ipynb` prescribes the section numbering. Use it
verbatim and fold the guideline's stages into it:

| Template section | Guideline stage |
| --- | --- |
| Declaration of Originality | fill in name — this is *in addition to* the Word doc copy |
| Libraries | S0 |
| 1. Business Understanding | S1 |
| 2. Data Understanding (2.1 load, 2.2 summary stats, 2.3 visualisation) | S2 |
| 3. Data Preparation (3.1 cleaning, 3.2 train-test split) | S3 |
| 4. Modelling | S4 |
| 5. Model Evaluation | S7 |
| 5.x Iterative model development / further feature selection | S5, S6 |

## Rubric map (Program Code = 50 marks)

| Rubric row | Marks | Stage that earns it |
| --- | --- | --- |
| Code Clarity & Documentation | 4 | all — markdown rationale above every non-trivial cell |
| Version Control / Development Logs | 4 | **the per-stage commits** + screenshots in S9 |
| EDA & Interpretation | 8 | S2 |
| Model Diversity, Comparison & Selection | 8 | S4 |
| Feature Engineering / Selection with Rationale | 10 | S5 |
| Hyperparameter Tuning | 4 | S6 |
| Evaluation Metric Selection & Justification | 4 | S1 + S7 |
| App: correct output, no errors, input validation | 2 | S8 |
| App: interactive, responsive, user-friendly | 6 | S8 |

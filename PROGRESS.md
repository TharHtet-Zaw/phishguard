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

**Stage:** S0 — Setup, **done**
**Last commit:** see `git log -1` (S0 scaffolding + skeleton)
**Working files:** `PhishGuard.ipynb`, `requirements.txt`, `PROGRESS.md`, `CLAUDE.md`

Standalone git repo initialised here on branch `main`, author `TharHtet-Zaw`
<htetthar2003@gmail.com> (repo-local config; the machine has no global git identity).
This folder is git-ignored by the vault repo so the two never collide.

`.venv/` created on Python 3.13.14 with `requirements.txt` installed (git-ignored —
recreate with `python -m venv .venv && ./.venv/Scripts/python.exe -m pip install -r
requirements.txt`). Run the notebook with the `.venv` kernel.

`PhishGuard.ipynb` (57 cells) is built on the submission template's numbering. Code that
loads the data and splits it is written and **verified to run**; every analysis/rationale
cell is a `> **TODO (my own words):**` prompt — those are mine to write, not Claude's.

## Next action

**S1** — write the Business Understanding section in my own words (the cost-of-error
framing is the anchor for the metric justification in §5). Then S2 EDA.

---

## Stage checklist

Tick only when committed. Each stage = one commit, message in the format
`S<n>: <what changed>` (the commit history is a graded 4% rubric row — see §Rubric map).

- [x] **S0 Setup** — venv, `requirements.txt`, load `.arff` → DataFrame, `random_state=42`
      constant, notebook skeleton built on the *submission template's* section numbering
      (see §Notebook structure). _Declaration of Originality name still blank — see
      §Open questions._
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

- GitHub repo: `https://github.com/TharHtet-Zaw/phishguard` — **not created/pushed yet**;
  waiting on `gh` install + `gh auth login`. Local commits are safe meanwhile.
- Streamlit app: _TBD (S8) — needs the GitHub repo public first_
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
| 5 | **Duplicates are the real data issue — decision still OPEN** | 11,055 rows collapse to 5,785 unique feature vectors (47% dupes), and 64 vectors carry both labels (357 rows) = irreducible error ceiling. Keeping duplicates leaks ~half the test set into training and inflates scores; dropping them halves the data. Must be decided and defended at S3 — quantified in notebook §3.1 | pre-S0 |
| 4 | Metric argument rests on **cost asymmetry, not class imbalance** | Actual split is 6157 legitimate / 4898 phishing = 1.26:1 — near balanced, so imbalance does *not* rule out accuracy. The case for recall is that a false negative lands a user on a credential-harvesting page while a false positive costs one dismissed warning. Do **not** say "the data was imbalanced so I used recall" at the demo | pre-S0 |

## Open questions / blockers

1. ~~GitHub repo strategy~~ — resolved: standalone repo, separate from the vault. Remote
   still needs creating once `gh` is installed and authenticated.
2. **Exact student name as it appears in TP-LMS** — still unconfirmed. Needed for the zip
   filename (`<TP-LMS name>_2503051A.zip`) and the Declaration of Originality in *both*
   the notebook and the Word doc. Likely "Thar Htet Zaw" (from the GitHub handle
   `TharHtet-Zaw`), but **do not ship on that guess** — verify against TP-LMS.

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

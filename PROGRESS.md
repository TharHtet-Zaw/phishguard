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

**Stage:** S4 — baselines, **code done, my interpretations still to write**
**Last commit:** see `git log -1` (S3 cleaning + S4 baselines)
**Working files:** `PhishGuard.ipynb`, `requirements.txt`, `PROGRESS.md`, `CLAUDE.md`

Standalone git repo initialised here on branch `main`, author `TharHtet-Zaw`
<htetthar2003@gmail.com> (repo-local config; the machine has no global git identity).
This folder is git-ignored by the vault repo so the two never collide.

`.venv/` created on Python 3.13.14 with `requirements.txt` installed (git-ignored —
recreate with `python -m venv .venv && ./.venv/Scripts/python.exe -m pip install -r
requirements.txt`). Run the notebook with the `.venv` kernel.

`PhishGuard.ipynb` (61 cells) is built on the submission template's numbering. All code
through §4.2 (load → EDA → clean → split → baselines) is written and **verified to run
top-to-bottom**; every analysis/rationale cell is a `> **TODO (my own words):**` prompt —
those are mine to write, not Claude's. Section 5 is still `## TODO` code stubs.

Verify the notebook runs with the scratchpad runner `run_nb.py` (execs every code cell in
one namespace, reports the first failure) — `nbconvert` is deliberately **not** in
`requirements.txt`, since that file also provisions Streamlit Cloud at S8.

**Gotcha, cost me a revert at S2:** the notebook declares `nbformat_minor: 5`, which
requires every cell to carry an `id`, but 42 cells had none. Notebook-editing tools that
target cells by id then silently fall back to *position* and land edits on the wrong
cells. Ids are now backfilled — but if cells ever get added by a tool that drops them
again, re-check before trusting an id-targeted edit.

## Next action

Two tracks, in parallel — the writing is mine, the code is not:

1. **Mine (blocks S1–S4 sign-off):** write the `TODO (my own words)` cells, all of which
   are now pre-loaded with the actual measured findings — §1 business framing +
   assumptions, §2.2 cardinality, §2.3.1.1 class balance, §2.3.1.2 feature
   interpretation, §2.3.2 correlation, §3.1 duplicate decision, §4.2 model comparison.
2. **Next code stage: S5** — feature selection (RF importances × mutual information) on
   the canonical deduplicated split. Prediction to check: `Favicon`, `popUpWidnow` and
   `Iframe` should rank last (Decision #8). Then S6 tuning, S7 final eval.

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
      _Code committed and verified. **Not tickable until I write the interpretation
      cells** — the 8 marks are for the interpretation, not the plots._
- [ ] **S3 Data prep** — dtype/missing checks, stratified train/test split.
      _Code committed. Both dataset variants built + split; leakage measured directly.
      Not tickable until I write the §3.1 duplicate argument._
- [ ] **S4 Baselines** — `DummyClassifier` + LogisticRegression + RandomForest +
      GradientBoosting on **all 30 features**. Metrics table saved to `artifacts/`.
      _Code committed, run on **both** variants. Not tickable until I write the §4.2
      quantitative + qualitative comparison._
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
| `artifacts/feature_level_rates.csv` | S2 | per (feature, level): support + phishing rate |
| `artifacts/baseline_metrics.csv` | S4 | all-30-feature test metrics, 4 models + dummy |
| `artifacts/selected_features.json` | S5 | final feature list + why each survived |
| `artifacts/reduced_metrics.csv` | S5 | same models on reduced set (before/after pair) |
| `artifacts/search_results.csv` | S6 | full `cv_results_` table from RandomizedSearchCV |
| `artifacts/final_model.pkl` | S7 | fitted model the Streamlit app loads |

_Exists: `feature_level_rates.csv`._

## Links

- GitHub repo: `https://github.com/TharHtet-Zaw/phishguard` — **created and pushed**,
  `origin/main` tracking. Deliberately **private** for now: the repo tracks TP's spec PDF
  and submission template (redistributing course material), and a public coursework repo
  before the deadline lets a classmate copy it, which implicates me too. Flip at S9 with
  `gh repo edit --visibility public --accept-visibility-change-consequences`.
- Streamlit app: _TBD (S8). Streamlit Community Cloud deploys from private repos, so
  this is not blocked by the visibility choice above._
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
| 5 | **Duplicates are the real data issue — decision still OPEN, recommendation is DROP** | 11,055 rows collapse to 5,785 unique feature vectors (47% dupes), and 64 vectors carry both labels (357 rows) = irreducible error ceiling. Keeping duplicates leaks ~half the test set into training and inflates scores; dropping them halves the data. **The "keep them as frequency information" counter-argument is weak here:** duplicate rows are not repeat observations of one site, they are *different* sites colliding because 30 mostly-binary codes is a coarse space. Collision from low feature resolution is not frequency signal. 5,785 rows is still ample for 30 low-cardinality features. Must be decided and defended at S3 — quantified in notebook §3.1 | pre-S0, rec. added S2 |
| 4 | Metric argument rests on **cost asymmetry, not class imbalance** | Actual split is 6157 legitimate / 4898 phishing = 1.26:1 — near balanced, so imbalance does *not* rule out accuracy. The case for recall is that a false negative lands a user on a credential-harvesting page while a false positive costs one dismissed warning. Do **not** say "the data was imbalanced so I used recall" at the demo | pre-S0 |
| 6 | EDA screens features by **conditional phishing rate per level ("spread"), not marginal distribution** | A bar chart of a {-1,1} column shows two bars and says nothing. `P(phishing \| level)` vs the 44.3% base rate is the quantity that actually carries information, and it produces the ranking S5 later has to agree with or explain away | S2 |
| 7 | The high correlations in the heatmap are an **artefact of skew, not redundancy** | The top 8 pairs (`popUpWidnow`↔`Favicon` ρ=0.94, etc.) are all between features where 81–87% of rows sit in one level. Two near-constant columns correlate whatever they measure. Nothing in the *informative* tier is mutually correlated — `SSLfinal_State` and `URL_of_Anchor` hit 0.74/0.70 against the target but not each other, so there is no multicollinearity problem to fix | S2 |
| 9 | **Duplicates: RESOLVED — deduplicate, and keep the kept-duplicates run as evidence** | `df_dedup` (5,849 rows) is canonical for 5.x onward; `df_kept` is run once at S4 purely to quantify the difference. Measured, not assumed: **65.8%** of test rows have an identical twin in train when duplicates are kept, vs **1.8%** deduplicated. Supersedes the open half of Decision #5 | S3 |
| 10 | **The leakage inflation is model-specific — this is the demo-worthy finding** | LR and GB move ≤0.2pp on recall; only RandomForest inflates (recall 0.9612→0.9404, accuracy 0.9742→0.9419). An unpruned forest can memorise individual rows, so duplicate twins reward it specifically. Corroborated by RF's train/test gap *growing* 0.016→0.049 after dedup: deduplication did not hurt RF, it **revealed** overfitting the duplicates were masking. Do not say "leakage inflates all scores" — it doesn't, and that's the interesting part | S4 |
| 11 | **Deduplication flips the majority class** | Kept = 55.7% legitimate; deduped = 51.6% *phishing*. So `DummyClassifier` flips from phishing recall 0.00 to **1.00** (accuracy 0.52). A baseline with perfect recall is the cleanest argument for reporting precision/recall/F1 together instead of optimising recall alone — use it in §5 | S4 |
| 12 | `pos_label=-1` **everywhere** in metrics | "Positive" must mean *phishing*, the class whose misses are expensive. sklearn defaults to `1`, which here is *legitimate* — so an unset `pos_label` silently reports recall for the wrong class and the whole §1 cost argument stops matching the numbers | S4 |
| 8 | **Three features are provably dead**: `Favicon`, `popUpWidnow`, `Iframe` | Their phishing rate equals the base rate at *every* level (spread 0.000, 0.0001, 0.006) — zero univariate signal. Predicts what S5 should find; if RF importance or mutual information disagrees, that needs explaining, not ignoring. Caveat for the demo: flat ≠ skewed. `Prefix_Suffix` is 87% one level and still has spread 0.51 | S2 |

## Open questions / blockers

1. ~~GitHub repo strategy~~ — resolved: standalone private repo, pushed 28 Jul. `gh` was
   already installed and authenticated; the earlier note claiming otherwise was stale.
2. **Schedule risk — as of 28 Jul there are 3 days to the 31 Jul 5pm Program Code
   deadline.** S5–S9 outstanding including a *deployed* Streamlit app and the Word doc,
   plus every `TODO (my own words)` cell. The external dependency (GitHub) is now
   cleared, so the critical path is my writing plus the S8 deploy.
3. **Exact student name as it appears in TP-LMS** — still unconfirmed. Needed for the zip
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

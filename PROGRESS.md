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

**Stage:** S7 — final evaluation, **code done, my interpretations still to write**
**Last commit:** see `git log -1` (S7 final evaluation)
**Working files:** `PhishGuard.ipynb`, `requirements.txt`, `PROGRESS.md`, `CLAUDE.md`

Standalone git repo initialised here on branch `main`, author `TharHtet-Zaw`
<htetthar2003@gmail.com> (repo-local config; the machine has no global git identity).
This folder is git-ignored by the vault repo so the two never collide.

`.venv/` created on Python 3.13.14 with `requirements.txt` installed (git-ignored —
recreate with `python -m venv .venv && ./.venv/Scripts/python.exe -m pip install -r
requirements.txt`). Run the notebook with the `.venv` kernel.

`PhishGuard.ipynb` (70 cells) is built on the submission template's numbering.
**All notebook code is now written and verified to run top-to-bottom** — load → EDA →
clean → split → baselines → feature selection → tuning → threshold → final eval → pickle.
No `## TODO` code stubs remain. Every analysis/rationale cell is a
`> **TODO (my own words):**` prompt — those are mine to write, not Claude's, and they are
now the only thing standing between here and a finished notebook.

A full top-to-bottom run now takes ~2 min: the §5.1 CV sweep is 450 model fits (k = 1..30
× 3 models × 5 folds) and accounts for ~100s of it.

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

1. **Mine (blocks S1–S7 sign-off, and it is now the whole critical path for the
   notebook):** write the `TODO (my own words)` cells, all of which are pre-loaded with
   the actual measured findings — §1 business framing + assumptions, §2.2 cardinality,
   §2.3.1.1 class balance, §2.3.1.2 feature interpretation, §2.3.2 correlation, §3.1
   duplicate decision, §4.2 model comparison, §5 metric selection, §5.1 feature-selection
   rationale (10 marks — the largest single row), §5.2 tuning, §5.3 final write-up.
   **§1 is now load-bearing for code too:** `FN_TO_FP_COST = 5` in §5.3 sets the decision
   threshold, and therefore what the app warns on. If §1's cost argument lands somewhere
   else, change that one line and re-run §5.3 (1:1 → t=0.51, 3:1 → t=0.27, 10:1 → t=0.05).
   **§4.2 is now load-bearing for code, not just prose:** `SELECTED_MODEL` in §5.1 is
   hard-coded to `GradientBoosting`. If the §4.2 argument lands on a different model,
   change that one constant and re-run §5.1 onward — the chosen `k` is model-specific
   (16 for GB, 21 for RF, 8 for LR).
2. **Next code stage: S8 — the Streamlit app, and it is the schedule risk.** `app.py`
   loads `artifacts/final_model.pkl`, which already carries the model, the 16-feature
   list *in training column order*, and the threshold. 16 inputs, input validation with
   user-facing errors, then deploy to Streamlit Community Cloud from the private repo and
   record the link below. Then S9 (Word doc, screenshots, zip).

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
      _Code committed and verified. 30 → **16** features, chosen by a 1-SE rule on 5-fold
      CV F1 inside the training split. Not tickable until I write the §5.1 rationale._
- [ ] **S6 Tuning** — `RandomizedSearchCV`, exactly 2 hyperparameters, ≤3 values each,
      on the selected model. Tuned vs untuned table.
      _Code committed and verified. `max_depth` × `learning_rate`, best (5, 0.2).
      **CV improved, test did not** — see Decision #18. Not tickable until I write §5.2._
- [ ] **S7 Final evaluation** — precision/recall/F1/confusion matrix, metric
      justification, assumptions stated. Model + feature list pickled to `artifacts/`.
      _Code committed and verified. Decision threshold **0.08** (Decision #19/#20): test
      recall **0.9901**, precision 0.8592, 6 of 604 phishing sites missed. Not tickable
      until I write §5 metric selection + §5.3._
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
| `artifacts/feature_ranking.csv` | S5 | per feature: RF importance + std, MI, both ranks |
| `artifacts/feature_sweep.csv` | S5 | CV recall/F1 (+SE) for k=1..30 × 3 models |
| `artifacts/selected_features.json` | S5 | final feature list, the selection rule, dropped list |
| `artifacts/reduced_metrics.csv` | S5 | same models on reduced set (before/after pair) |
| `artifacts/search_results.csv` | S6 | full `cv_results_` table from RandomizedSearchCV |
| `artifacts/threshold_curve.csv` | S7 | out-of-fold precision/recall/FN/FP at t = 0.05…0.95 |
| `artifacts/final_metrics.csv` | S7 | test metrics at t = 0.50 vs the chosen threshold |
| `artifacts/final_model.pkl` | S7 | dict: fitted model **+ feature list in column order + threshold** + metadata — the app needs all three, and a column-order mismatch fails silently |

_All ten exist; the notebook rewrites them on a full run._

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
| 13 | **`k` is chosen by a 1-SE rule on CV inside the training split, never by test score** | The two rankings order the features; they do not say where to cut. Re-scoring the test set at each `k` would pick the cut that flatters the test set, and the before/after table would then be comparing a tuned "after" against an untuned "before". So: 5-fold CV *within* train, take the smallest `k` within one standard error of the best. Result **k = 16**, F1 0.9452 best at k=30, SE 0.0042, threshold 0.9410 | S5 |
| 14 | **Cut on F1, not on recall** — even though the project prioritises recall | By recall alone the same rule keeps only **k = 5** (CV recall 0.9354 at k=5 vs 0.9395 at k=30). Features 6–16 buy *precision*, not recall. Recall alone is gameable — §4.1's dummy scores 1.000 on it — so a feature set sized to maximise recall is sized to maximise a number a useless model already wins. This is the S5 answer to "why not just take five features?" | S5 |
| 15 | **S5 confirmed the S2 prediction, and the prediction was recorded first** | `Favicon` (mean rank 24.5), `popUpWidnow` (24.0), `Iframe` (29.0) all landed in the bottom seven of 30 — Decision #8 was written at S2 from conditional phishing rates alone and survived two model-based rankings. The two rankings agree overall (Spearman ρ = **0.899**); the four real disagreements (`Submitting_to_email` RF 21 vs MI 30, `Shortining_Service` 24 vs 15, `Abnormal_URL` 23 vs 14, `Statistical_report` 19 vs 12) are all below the cut, so nothing rides on them | S5 |
| 17 | **The two hyperparameters were chosen by measurement, not by habit** | The spec caps tuning at 2 parameters × 3 values, so *which two* is the decision. Scanned one-at-a-time on the same CV folds, everything else at default: `learning_rate` spread **0.0126**, `max_depth` **0.0115**, `n_estimators` 0.0034, `subsample` 0.0021. Searched as pairs, `max_depth`×`learning_rate` reaches 0.9491, beating every other pair. Boundary checked too — extending to depth {3,5,8,12} × lr {0.1,0.2,0.3,0.5} scores *worse* everywhere (0.9375 at depth 8, 0.9339 at depth 12/lr 0.2), so the corner optimum is a real interior peak, not a grid wall. The scan itself is **not** in the notebook (it would look like a 4-parameter search and violate the cap); the numbers live here and in the §5.2 markdown | S6 |
| 18 | **Tuning improved CV and regressed on test — report it, don't bury it** | Best CV F1 0.9426 → **0.9491** (+0.65pp) at `max_depth=5, learning_rate=0.2`. Test: F1 0.9474 → 0.9421, accuracy −0.60pp, precision −1.41pp, recall **+0.33pp**, train−test gap 0.0013 → **0.0346** (27×). Mean train F1 0.9489 → 0.9786. Same failure mode as RandomForest in §4.2: the higher score is memorisation. Both moves are ≈1 SE, so the claim is "tuning produced no real improvement", not "tuning made it worse". **Do not swap back to the untuned model on the strength of the test table** — that is selecting on the test set, the exact error §5.1 avoided when choosing `k`. If it is swapped, the reason must be the train−test gap, which is visible without test metrics | S6 |
| 19 | **The decision threshold, not the hyperparameters, is the lever for the recall/precision trade** | Hyperparameters move precision and recall together and unpredictably — S6 is the proof. `predict_proba` with a moved threshold trades them against each other on purpose, which is what a recall-prioritised brief actually calls for. S7 picks the threshold by CV on the training split and reports it once on test. This is also what makes §1's cost argument operational instead of decorative | S6 |
| 20 | **Operating point: threshold 0.08, from `FN_TO_FP_COST = 5`** | Chosen on out-of-fold *training* probabilities (`cross_val_predict`), never on test — same discipline as the §5.1 `k` choice. Test result: recall 0.9421 → **0.9901** (35 → **6** of 604 phishing sites missed), precision 0.9421 → 0.8592 (35 → 98 false alarms), accuracy 0.9402 → 0.9111. Sensitivity is in the notebook and matters at the demo: 1:1 → t=0.51 (i.e. sklearn's default is what "no asymmetry" gives), 3:1 → t=0.27, 10:1 → t=0.05. The 5 is an *assumption from §1*, not something the data supports — say so before being asked | S7 |
| 21 | **Two feature encodings run backwards from the dataset documentation** | `Domain_registeration_length` codes 1 as ">1 year registered", the nominally legitimate level, but that level is **60.2%** phishing vs 36.4% for the short-registration level. `SSLfinal_State` is non-monotone: the "suspicious" middle level 0 is **98.2%** phishing, worse than "no HTTPS" at 85.8%. Both hold on the full 11,055 rows, so it is not a dedup artefact. Found via the §5.3 smoke-test row, which is built from measured per-level phishing rates rather than by hand — which is why it surfaced at all. Retrospectively justifies Decision #6 | S7 |
| 16 | **Feature selection held performance; it did not improve it** | GB on 16 features vs 30: F1 0.9474 vs 0.9475, accuracy identical at 0.9462, recall −0.0017, precision +0.0015. Do **not** claim selection made the model better. The two real gains are the train−test gap (0.0062 → **0.0013**, 5× tighter) and 14 fewer inputs for the Streamlit user. Note the cut is flat, not knife-edge: k=13 scores 0.9409 against a 0.9410 threshold, and the curve is level from ~13 to 30 — claiming 16 is *optimal* would be false precision | S5 |

## Open questions / blockers

1. ~~GitHub repo strategy~~ — resolved: standalone private repo, pushed 28 Jul. `gh` was
   already installed and authenticated; the earlier note claiming otherwise was stale.
2. **Schedule risk — as of 29 Jul there are 2 days to the 31 Jul 5pm Program Code
   deadline.** S6–S9 outstanding including a *deployed* Streamlit app and the Word doc,
   plus every `TODO (my own words)` cell. The external dependency (GitHub) is now
   cleared, so the critical path is my writing plus the S8 deploy. S6 and S7 are small;
   **S8 is the one that can eat a day** — start the deploy before the prose is finished.
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

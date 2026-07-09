# REVISION_NOTE.md — BABEL paper v1 → v1.1 (tracked-change summary)

**Date:** 2026-07-08 · **By:** REVISION CC · **Governing brief:** REVISION_BRIEF_2026-07-07.md
(STAGE 1) · **External input:** STANFORD_REVIEW.md (paperreview.ai, 2026-07-07).
**Scope:** Stage 1 only — reanalysis of *existing frozen artifacts* + text. **No new GPU
experiments** (those are proposals in STAGE2_PROPOSAL.md; Will greenlights each). **Nothing
publishes** — `PAPER_V1_1_DRAFT.md` stays a draft until Will fires the Zenodo-v2 / GitHub update.
**No frozen number was altered and no artifact was renamed;** every added statistic is a new
reanalysis of frozen data, pre-registered where required and logged propose-only in the pen.

Source of the revised draft: `PAPER_V1_1_DRAFT.md` (byte-copy of `PAPER_DRAFT_V1.md`, then the
edits below). Reanalysis harnesses + outputs: `_rev_fdr.py`/`_rev_fdr.out`,
`_rev_fdr_channel.py`/`_rev_fdr_channel.out`, `_rev_floor.py`/`_rev_floor.out`. Pen blocks (all
propose-only): `REVISION-FDR — PRE-REGISTRATION`, `REVISION-FDR — RESULTS`,
`REVISION-FLOOR — RESULTS` (2026-07-08).

---

## A. Substantive reanalyses (Stage 1A)

### 1. FDR / FWER control on the naming battery (review Q2 — top priority)
- **Pre-registered before computing** (pen `REVISION-FDR — PRE-REGISTRATION`, locked α = 0.05 BH,
  sensitivity 0.01/0.10, tail-model + re-derivation rule) — brief item 1 satisfied.
- **Validation gate passed:** re-deriving NAMED from the raw stored statistics with the frozen
  `obs > null95` rule reproduces the frozen L1 verdicts **0 mismatches / 312** → the BH
  re-derivation is trustworthy.
- **Result (312 channels with frozen per-gate stats; frozen NAMED 149 = 47.8 %):** per-gate BH
  q = 0.05 → **6.7 %** named (q = 0.01 → 1.9 %, q = 0.10 → 16.3 %); channel-level (conjunction-aware,
  post-hoc) BH q = 0.05 → **25.6 %** (q = 0.01 → 9.0 %, q = 0.10 → 35.6 %); Holm FWER → 1 channel;
  global-null assumption-free bound → FDP ≈ **10 %**. N = 20 nulls floor the empirical p at ≈ 0.048
  → continuous p are tail-model extrapolations; a definitive FDR is a Stage-2 high-N re-draw.
- **Draft changes:** Abstract naming sentence re-scoped + corrected fractions; **new §6.1
  multiplicity paragraph + table**; §6.5 number 3 re-scoped; **new Appendix B** (full procedure,
  both null models, Holm, global-null, scope). The 53.6 %/46.4 % figures are **retained** as the
  frozen gate-level record and everywhere re-labelled "under the L1 σ-null battery at N = 20".

### 2. Floor-construction sensitivity for the 39/39 closure (review Q1)
- **Result:** 36/39 legacy closure is floor-construction-robust; **39/39 is reached only at the
  full norm-relative recalibration (β = 1)** — β ≤ 0.5 → 36/39, β = 0.75 → 37/39. The three
  recal-only cells (code_b12, rep_b11, rep_b12) close because the norm-scaled floor there is
  1.5–2.7× the legacy floor (tracks ρ²) — documented norm-geometry, meter-dependent, labelled so.
  Recal closure tolerates loosening (39/39 for c ≥ 1) but is sensitive to a 10 % tightening
  (34/39 at c = 0.9); 13/39 cells pass "tight" (KL/floor 0.8–1.0).
- **Honest gap:** per-token substitution KL is **not frozen** (only per-cell means) → the
  bootstrap-CI-vs-floor half of Q1 is **not computable CPU-only**; deferred to Stage 2.
- **Draft changes:** Abstract 39/39 clause scoped; **new §4.1 floor-sensitivity paragraph**;
  §8.5 sensitivity note; **new Appendix C** (β-sweep, interpolation, multiplier, margin bands, the
  3 gap cells, the CI constraint).

### 3. Student (executable-rung) methods appendix (review Q6)
- Extracted every training/val detail from `_v6_result.json`/`_v7_result.json`/`_v6.py`/`_v7.py`,
  **all numbers verified against the frozen JSON**.
- Key clarification for the reviewer: the linear student is **Adam-MSE (lr = 1e-3, 4000 steps),
  with NO ridge / weight decay** — its regularizer is *capacity*, not a penalty. Splits: 96 train
  periods (seeds 7000–7095), 16 SACRED (seed 3, never-seen), 16 HOLD2 (8000–8015), period 64.
  Twin = permuted rep-era targets; pass = real ≤ 0.5 × twin.
- **Draft change:** **new Appendix D** (task/inputs, data/splits, fit, architectures/params, twin,
  full results table, non-recoverable list).

### 4. No-gloss scope reframe (review Q7)
- **Draft change:** §8.4 rewritten — every "word-less" claim now means *no gloss under the
  CH-WU/CH-INT/CH-FIELD battery at N = 20*, not "provably carries no content"; named battery
  **extensions** listed as future work (syntax/dependency probes, morphology, non-vocabulary
  probes, causal-scrubbing readouts, SAE decoders; §9). Two bounding facts stated: the FDR
  re-analysis shows the battery is if anything *generous* (so no-gloss is more likely an under- than
  over-estimate), and L6's dark-complement edge (2/8 faint) shows the honest limit.

## B. Text changes (Stage 1B)

- **5. Scope (title/abstract).** Title keeps "State Space" (unchanged). Abstract sentence 2 adds an
  explicit boundary-grain / within-block scope line; §1.4 already carried it (unchanged).
- **6. Glossary.** New **§1.5** — one-page neologism table (door, seam, meter, floor, folded read,
  dark mass, corridor, core, rung, gloss, no-gloss, transplant, gauge/lever, twin, DEAF axis, …).
- **7. Related work.** New **§7 paragraph** adding causal scrubbing (Chan et al., AF 2022), DLA /
  attribution patching (2310.10348) / ACDC (2304.14997), and mechanistic benchmarks (Tracr
  2301.05062, RAVEL Huang 2024), each mapped to the Table-1 four axes where honest. (SAE decoding
  and probing debates were already in §7; unchanged.)
- **8. Artifacts (Q8).** Every "pending release" replaced with the **live** release: Zenodo DOI
  10.5281/zenodo.21230108 (concept 10.5281/zenodo.21230107), github.com/wpferrell/babel-codec-gpt2,
  huggingface.co/wpferrell/babel-codec-gpt2 — header line, §7 falsifiability line ([GITHUB-URL]),
  and §10 artifact statement.

## C. Editor notes / NOTES-for-Will

- New NOTES-for-Will item 12 added to the draft's review-comment block (delete before release).
- **New §7 citations need the same live-page verification** as the existing ones before release:
  causal scrubbing (Alignment Forum, no arXiv), attribution patching (2310.10348), ACDC
  (2304.14997), Tracr (2301.05062), RAVEL (Huang et al., 2024 — exact ID to confirm).

## D. What did NOT change
- No frozen result, floor, hash, or artifact name. The L5/L6 certified negatives, the 39/39 recal
  headline, the seam law, the transplant 94.7 %, and the wall student all stand. The revision
  *scopes and stress-tests* the naming and closure claims; it does not move them.

## E. Deliverables produced
`PAPER_V1_1_DRAFT.md` · `REVISION_NOTE.md` (this) · `REVIEWER_RESPONSE.md` · `STAGE2_PROPOSAL.md` ·
reanalysis harnesses/outputs (`_rev_fdr*.py/.out`, `_rev_floor.py/.out`) · pen propose-only blocks.


## F. Stage-2 GPU experiments — folded 2026-07-08 (Stage-2 Revision CC)

Will greenlit three Stage-2 items (STAGE2_GREENLIGHT.md); all three ran, each with a byte-replay gate
to the frozen number and pre-registered bands (pen: STAGE2-A/B/C blocks). Results folded into the draft
and REVIEWER_RESPONSE; frozen artifacts untouched (READ-ONLY); propose-only; nothing published.

- **Item B — transplant boundary×regime (Q4; `_s2b.py`).** Gate: b6/prose 16-pair closure = 0.9467
  (dev 0.0). 3×3 grid (b2/b6/b10 × prose/code/repetition), 32 pairs/cell, matched-random null, 10k
  bootstrap CIs. Result: boundary- and prose/repetition-general (median closure 0.82–0.98 across depth);
  code heavy-tailed at early/mid depth (median 0.70/0.60, mean collapsed by outlier pairs), clean at b10
  (0.89). → Abstract + §6.4 table + §8 item 9 scoped; Reviewer Q4 answered.
- **Item C — seam perturbation (Q5; `_s2c.py`).** Gate: global-core cert byte-replays all 36 frozen
  KL_LIN (max dev 0.0). C2a within-span rotation exactly invariant; C2b ±ε jitter 30/30 draws keep
  36/36 TIGHT (ε≤0.10); C1 independent per-seam re-derivation keeps 33/36 LINEAR-TIGHT — the 3 failures
  are all the embed→L0 rewrite seam (prose/code LINEAR-not-TIGHT, repetition BROKEN). → §6.2 amended:
  the linear composition law is a robust *model* property at the 33 propagation seams, field-conditioned
  at the b0 rewrite seam. Reviewer Q5 answered.
- **Item A — door/core rotation robustness (Q3; `_s2a.py`).** Gate: S4 readable + full rank-48 fold KL
  byte-replay all 4 sampled cells (dev 0.0). Across R=20 random orthonormal bases/object: folded-read
  reconstruction KL invariant to 0.0, k* shift 0 (k*=16/40/32/24), 0/80 pass-flips, door/core footprints
  invariant to ≤3e-5, matched-random reconstruction discriminator separates. Core-field per-axis
  identities drift under within-span rotation (0/19) → verdict PARTIAL: necessity/k*/folded-reads
  rotation-stable, the 19 field labels a privileged basis of an intrinsic subspace. → §6.1 note added;
  §8 item 9; Reviewer Q3 answered.

Harnesses/outputs: `_s2b.py`/`_s2b_result.json`, `_s2c.py`/`_s2c_result.json`, `_s2a.py`/`_s2a_result.json`,
logs `_s2{a,b,c}.log`, launch bats `_s2{a,b,c}_run.bat`; pen propose-only pre-registration + results blocks
(STAGE2-A/B/C). None moves a frozen headline; each *scopes* a claim, per the pre-registered kill branches.
DATALAKE registered at closeout. NOTHING published — v1.1 stays draft until Will fires Zenodo v2 / GitHub.

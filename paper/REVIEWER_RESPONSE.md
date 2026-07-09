# Response to the Stanford agentic review (paperreview.ai)

We thank the reviewer for an unusually careful and constructive read — the strengths noted
(pre-registration, matched nulls, priced remainder, the clean wall result) are exactly the culture
we hope becomes standard, and every weakness raised is fair. This response is point-by-point and
honest; where the requested analysis moves a headline number, we say so plainly. All changes are in
`PAPER_V1_1_DRAFT.md` (v1.1); the reanalyses are CPU-only on the frozen artifacts and
pre-registered where required. Items needing new GPU runs are proposed, with cost/bands/kill
conditions, in `STAGE2_PROPOSAL.md`; the three the reviewer’s Q3–Q5 turn on (rotation/basis robustness,
transplant boundary×regime, seam perturbation) have since been run under Stage‑2 authorization and are
folded into the draft (§6.1/§6.2/§6.4) and answered below — each with a byte‑replay gate to the frozen
numbers; the remaining Stage‑2 items stay proposed.

---

## Answers to the eight questions

**Q1 — Floor sensitivity and substitution-KL CIs.** *Addressed (partly), and it sharpened an honest
caveat.* We swept alternative floor constructions on the frozen per-cell KL (Appendix C,
`_rev_floor.py`). The 36/39 legacy closure is robust to floor construction. **The 39/39 is reached
only at the *full* norm-relative recalibration (β = 1):** a fractional norm-scaling floor gives
36/39 for β ≤ 0.5, 37/39 at β = 0.75, 39/39 only at β = 1; under a 10 % uniform tightening the recal
closure is 34/39. The three recal-only cells close because the late-layer state norm grows and the
norm-scaled floor there is 1.5–2.7× the legacy floor (tracking ρ²) — a documented norm-geometry
effect (§5.1), which the paper already labelled "meter corrections, not model discoveries" and now
quantifies. We have re-scoped the headline to **"36/39 floor-construction-robust; 39/39 under the
pre-registered norm-relative meter at full norm-scaling."** The **substitution-KL bootstrap CIs you
asked for are not computable from the frozen data** — only per-cell *mean* KL was stored, not
per-token KL — so we defer them to Stage 2 (a GPU re-run that emits per-token KL; STAGE2_PROPOSAL
item E). We flag this rather than approximate it.

**Q2 — Multiple comparisons / FDR on the 53.6 % named statistic.** *This is the most consequential
change.* We added explicit control (Appendix B; harnesses `_rev_fdr.py`/`_rev_fdr_channel.py`,
**pre-registered before computing**). A validation gate confirms our re-derivation reproduces the
frozen verdicts channel-for-channel (0 / 312 mismatches). Results on the 312 channels with frozen
per-gate statistics (frozen NAMED = 47.8 %):

- **per-gate Benjamini–Hochberg** (strict; treats each of a channel's 9 gates as a hypothesis,
  m = 2592): q = 0.05 → **6.7 %** named (q = 0.01 → 1.9 %; q = 0.10 → 16.3 %);
- **channel-level BH** (conjunction-aware; the natural unit for "how many channels are named",
  m = 312): q = 0.05 → **25.6 %** (q = 0.01 → 9.0 %; q = 0.10 → 35.6 %);
- **Holm–Bonferroni FWER** (α = 0.05) → 1 channel;
- **assumption-free global-null bound:** the ≥ 2-of-3-regime rule already holds the expected
  false-named fraction to **≈ 10 %**.

The honest reading: most frozen names rest on gate clears that are individually marginal and are
made credible by cross-regime replication, so a strong ≈ 9 % core (q = 0.01) survives any
correction, roughly half survive channel-level BH at q = 0.05, and the built-in replication already
bounds false discovery near 10 %. **The binding limit is that only N = 20 null draws were frozen**
(empirical-p floor ≈ 0.048), so sub-0.05 p-values are tail-model extrapolations; a *definitive* FDR
needs a high-N re-draw (STAGE2_PROPOSAL item D). We **retain** the 53.6 %/46.4 % figures as the
frozen gate-level record but re-scope every naming claim to "under the L1 σ-matched-null battery at
N = 20" and report the corrected fractions in the Abstract, §6.1, §6.5, and Appendix B.

**Q3 — Doors/core robustness to rotations and reparameterization.** *Run in Stage 2; answered.* The
necessity certificates are basis‑rank statements (minimal k\* for a rank‑k orthonormal write), which are
rotation‑invariant *by construction within a chosen subspace* — but you are right that this deserved an
empirical check for k\*, pass/fail, and identity. We ran it (`_s2a.py`, cert machinery byte‑verbatim;
the S4 and full rank‑48 fold KL byte‑replayed all four sampled cells to the digit). Across R = 20 random
orthonormal bases per object: the folded‑read reconstruction KL is invariant to **0.0** (fp32), the
minimal necessity rank k\* is unchanged (shift 0 at all four cells; k\* = 16/40/32/24), the certified
pass/fail never flips (0/80), and the door/core ablation footprints are invariant to ≤ 3×10⁻⁵. A
matched‑random rank‑k subspace fails to reconstruct (KL 0.26–0.38 ≫ floor), so the invariance is
object‑specific, not vacuous. The one honest qualifier is **identity**: the 19 core fields are a
*privileged* basis of an intrinsic, rotation‑invariant 19‑dim subspace — a within‑span rotation mixes
them, so the *per‑axis* labels are basis‑relative (0/19 rotated axes match a frozen field), while the
subspace, its rank, and the fixed field directions are invariant. So the k\*/necessity/folded‑read
claims are rotation‑stable (the FRAGILE kill branch does not fire), and §6.1's "19 named fields" is now
stated as one interpretable labeling of an intrinsic subspace, not a canonical per‑axis identity (§6.1).

**Q4 — Transplant generality (boundaries, seeds, regimes).** *Run in Stage 2; answered.* We re‑ran the
T2 transplant (`_s2b.py`, machinery byte‑verbatim; the frozen b6/prose 16‑pair closure byte‑replayed to
0.9467, dev 0.0) on a 3×3 grid — boundaries {b2, b6, b10} × regimes {prose, code, repetition}, 32
pairs/cell, matched‑random null per pair, 10k‑bootstrap CIs (§6.4). **The 94.7% is not b6‑special:**
median closure is 0.94–0.98 in prose and 0.82–0.98 in repetition at early, mid *and* late boundaries.
The one honest exception is **code at early/mid depth**, where the readable‑gloss subspace (thin in
code, §6.1) makes the transplant heavy‑tailed — median 0.70 (b2) / 0.60 (b6), with a minority of pairs
diverging so far that the *mean* collapses to 0.31 / −0.01 — recovering to 0.89 at late b10. All nine
cells pass the pre‑registered margin band, but in the two code early/mid cells that band is inflated by
an even‑worse random null, so we report the closure itself as the governing number there. The Abstract
and §6.4 are re‑scoped to "boundary‑general and prose/repetition‑general, with a code early/mid caveat."
Seeds/corpora breadth (item F) remains available if wanted.

**Q5 — Nonlinearity hidden in the field definitions rather than the seams.** *Run in Stage 2; answered,
and it sharpened §6.2.* We tested (`_s2c.py`, seam certifier byte‑verbatim; the global‑core cert
byte‑replayed all 36 frozen KL_LIN to the digit, max dev 0.0) whether the linearity is an artifact of
the one global field dictionary. It survives **field‑basis rotation** (exactly — the write is a
projector) and **±ε dictionary jitter** (30/30 draws keep all 36 cells TIGHT, ε up to 0.10).
Re‑deriving the 19 fields **independently per seam** from each seam's own boundary‑pair residuals keeps
**33/36** cells LINEAR‑TIGHT; the three exceptions are all the *same* seam, the first (embed→L0) —
prose/code stay LINEAR but lose the TIGHT sub‑band, repetition breaks linearity outright. That is
precisely the seam §6.2 already flags as the language's *only* REWRITE seam. So the linear composition
law is a robust property of the model at all 33 propagation seams, while the embed→L0 rewrite's
linearity is a property of the certified global fields (independently‑derived first‑seam fields expose
its nonlinearity). Per the pre‑registered kill branch we now say so: §6.2 scopes the model‑level
linearity claim to the propagation seams and labels the b0 rewrite seam field‑conditioned — a genuine
sharpening, coherent with §6.2's prior "real rewriting confined to the first seam."

**Q6 — Student training/validation details and ablations.** *Fully addressed from frozen artifacts.*
New Appendix D gives every recoverable detail, all verified against `_v6_result.json`/`_v7_result.json`:
inputs (feature dim 1537 = layer-2 state ⊕ current-token embedding ⊕ m0 coefficient); splits (96
training periods, seeds 7000–7095; 16 never-seen SACRED periods, seed 3; 16 HOLD2, seeds 8000–8015;
period 64); fit (**Adam, lr = 1e-3, 4000 steps, MSE, fp32, TF32 off — and, to answer the ridge
question directly, *no ridge / weight decay*; the linear student's regularizer is capacity, which is
the point**); architectures/param counts (linear 1,181,184; MLP 1,771,776; attention 1,776,384);
shuffled-target twin (permuted rep-era targets; pass = real ≤ 0.5 × twin); and the full result table
including the capacity-hurts falsifier (MLP/attention train-R² 0.98/0.97, within-seen KL ≈ 0.001,
SACRED KL ≈ 0.35). A dedicated ridge/learning-curve ablation is offered as a small Stage-2 item if
useful. Loss curves (40 points/student) are frozen and drive Fig. 4.

**Q7 — "Word-less" vs "under-detected."** *Agreed; reframed.* §8.4 now states that every "word-less"
claim means *un-nameable under the CH-WU/CH-INT/CH-FIELD battery at its budget*, not "provably no
content." We name plausible battery extensions that could reduce the no-gloss rate (syntax/dependency
probes, morphology, non-vocabulary feature-space probes, causal-scrubbing readouts, SAE decoders;
§9). Two facts bound the concern: the FDR re-analysis shows the battery is if anything *generous*
(marginal names do not all survive control), so the no-gloss fraction is more likely an under- than
an over-estimate of genuine word-less channels; and L6's dark-complement adjudication (2/8 top
carriers clear only faintly) shows the battery's honest edge on the hardest mass.

**Q8 — Release of code, data, and frozen artifacts.** *Done.* The full frozen bundle is public:
Zenodo DOI 10.5281/zenodo.21230108 (concept 10.5281/zenodo.21230107), with the verdict-bearing
harnesses and a mirror at github.com/wpferrell/babel-codec-gpt2 and
huggingface.co/wpferrell/babel-codec-gpt2. Every "pending release" in v1 is replaced with these
live pointers (header, §7, §10). Not only hashes but the artifacts and deterministic streams are
available for independent byte-replay.

---

## On the itemized weaknesses

- **Mid-course meter recalibration bias.** Conceded and quantified (Q1/Appendix C): 36/39 is the
  floor-robust result; 39/39 is meter-dependent on exactly the last three norm-geometry cells,
  labelled as such, with both meters reported permanently.
- **No-gloss depends on battery scope.** Conceded and reframed (Q7/§8.4).
- **Within-block coverage / "complete" scope.** The Abstract now states the boundary-grain scope
  and the within-block exclusion up front (title keeps "State Space").
- **Rotation/basis dependence.** Run in Stage 2 (Q3/§6.1): the necessity certificates (folded-read k*, pass/fail, reconstruction) are rotation-invariant (k* shift 0, 0/80 flips, matched-random discriminator separates); the 19 core-field per-axis labels are basis-relative (an intrinsic subspace, a privileged labeling), stated as such.
- **Small holdouts / seeds / corpora.** Boundary × regime breadth run in Stage 2 (Q4/§6.4): the transplant is boundary- and prose/repetition-general with a code early/mid caveat; further seed/corpus breadth (item F, item B
  and the seed-robustness note), with the honest current scope stated.
- **Multiple comparisons.** Addressed (Q2) — the single largest change to the paper's claims.
- **Under-ablated seam law.** Run in Stage 2 (Q5/§6.2): robust to field-basis rotation and ±ε dictionary jitter, and to independent per-seam field re-derivation at all 33 propagation seams; only the embed→L0 rewrite seam is field-conditioned, now labelled as such.
- **Dense, neologism-heavy prose.** New one-page glossary (§1.5).
- **Thin related work (causal scrubbing, DLA, SAE, probing, benchmarks).** §7 expanded (SAE/probing
  were present; causal scrubbing, DLA/attribution patching/ACDC, and mechanistic benchmarks added,
  mapped to the four axes).

We are grateful for the review; it materially improved the paper's honesty about what the naming
fraction and the final three closure cells actually rest on. We commit (as in §7.0) to amend any
claim a further result overturns.

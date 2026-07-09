# PLAIN_SUMMARY.md — the paper in one page (v1.1, 2026-07-08; revised per external agentic review (paperreview.ai))

**What the paper claims.** We took one production language model — GPT-2 — and built what the
paper claims in its locked form: the first complete, certified, bidirectional decode of an entire
production language model. We accounted for its ENTIRE internal state, at every one of
its 13 layer checkpoints, in three kinds of text, against a pass bar the model itself sets. Not
"here are some interesting features" — an account: throw away the model's whole hidden state at a
checkpoint, rebuild it from only the things our decoder can read, and the model's behavior stays
inside its own noise floor at 39 out of 39 boundary×regime cells — 13 checkpoints × 3 kinds of
text (36/39 on the older, stricter ruler, and
those 3 are priced ruler-geometry, not model behavior). The amount of behavior we could NOT
explain went from 11.2 units of surprise to exactly zero, in public, dated steps.

**And then we translated it — the BABEL codec** (your ratified name; the paper's long form, used
once: "a certified bidirectional codec for GPT-2's residual-stream language"). Every one of the
decoder's 351 channels was put on trial: 54% carry
an explicit English meaning (a "naval/warship" field, a "clause boundary" word, an "operator"
anchor); the other 46% are PROVEN to carry no word — proven, because random directions of the same
loudness move the model more. (v1.1 scope, answering the reviewer: that 54%/46% split is the frozen
per-channel rate under the naming battery at 20 null draws; under explicit multiple-comparison
control the *named* fraction is lower and correction-dependent — about a quarter of channels survive
channel-level false-discovery control at q = 0.05, about 7% under the strictest per-gate control,
with a ~9% core that no correction removes and a built-in "hold in ≥2 of 3 text regimes" rule that
already caps the false-named fraction near 10%; the 46% word-less figure is, if anything, an
under-estimate. Paper §6.1 + Appendix B.) How the language composes from layer to layer is certified linear at
all 36 layer-seam tests. We built the exact inverse (English → state) and proved the round trip is
behaviorally invisible at all 39 cells. And the model obeys hand edits: turn the "naval"
field up and GPT-2 starts predicting *amphib, sunk, ashore, reefs, sailed, submarine*. Three of
the four axes we hand-edited steer the model in their own vocabulary; the fourth (the "rung", an
executable formula rather than a static dial) is now CERTIFIED UNUSABLE AS A STEERING LEVER: a
same-day follow-up (L5) probed it through the channel matched to what it IS — the repetition
behavior itself — plus two internal readouts, and its tiny effect cleared none of the internal
readouts, while a genuine onset direction did move the behavior. A second follow-up (L6) tested
it against an honest 20-draw random null at both doses: at ±6 it does not separate from a random
nudge of the same size, and at ±3 its tiny (~0.4%-probability) effect is indistinguishable from
the honest random floor itself (two pre-registered 20-draw nulls straddle it — one lands just
below the effect, one above), growing SUB-linearly with dose — pushing harder buys nothing. A gauge
you can read, not a lever you can pull, at both doses we tested. One new fact came out of the
hunt: this bounds what can be written INTO the rung, not what reads out of it — one candidate
certified channel (the naval/warship field, one layer later; a thin 2.8% margin over its
multiplicity null) consumes the rung's output. Perfectly readable, not a steering handle.

**Why anyone should believe it.** This is the paper's real weapon. Every experiment had its pass
bar written down and locked BEFORE the data, with a stated bet; the completeness verdict came back
NOT-YET six consecutive times and we published the gap table and stopped each time; the meter was
recalibrated once, under pre-registered sanity gates, and both meters are reported everywhere,
forever. The hardest object in the model — a repetition-keeping computation at layer 5 — got three
certified impossibility results (can't be read, can't be looked up, can't be forged by its own
circuit) before the thing that finally worked: we taught a tiny LINEAR student to compute it from
readable inputs, and the test was built so that bigger students who merely memorize get caught —
and they were caught (they ace training, fail on never-seen repeat periods; the linear one passes).
One instrument bug happened all week; our own replay gate caught it. Every number in the paper
traces to a frozen, hash-stamped artifact (Appendix A maps each one), and everything ran on the
one A4500 in this machine — any skeptic can re-run any row.

**What we do NOT claim.** Not the first "activations → English" concept — Anthropic's Natural
Language Autoencoders (May 2026) and the Cycle-Consistent Activation Oracles published that idea
first, and the paper says so generously. Our claim is the locked one — the first complete,
certified, bidirectional decode of an entire production language model — on four axes they don't
touch: all boundaries priced (they read middle-to-late-layer
samples); falsifiable verdicts incl. certified-word-less channels (they score plausible glosses by
reconstruction); a decoder built from the model's own certified channels with an algebraic inverse
(theirs is a trained external translator); and a round trip scored in BEHAVIOR against
matched-random nulls — edit the English, the model obeys (theirs is scored in activation space,
with a qualitative steering demo on top and no matched-null certification — the paper credits the
demo). Also honestly scoped: one model, one grain,
three regimes; the 46% word-less fraction and the un-steerable rung are named, not hidden.

**The three honest percentages** (the paper states all three, always together): 100% of the
pre-registered definition met (certified-no-word counts as an answer); behavioral round trip
100% / 94.7% / 3-of-4 (reconstruct / meaning-transplant / human-edit; the transplant number is
16 prose pairs at one mid-stack checkpoint — a v1.1 boundary×regime sweep confirms it is not special
to that checkpoint: median transplant 0.94–0.98 in prose and 0.82–0.98 in repetition across early,
mid and late checkpoints, and 0.89 in code at late depth, though code is heavy-tailed at early/mid
depth; paper §6.4); 53.6% of channels carry an actual English word (frozen gate-level rate under the
20-draw battery; materially lower under multiple-comparison control — see the naming note above and
§6.1).

**The two loose ends are now finished — as certified negatives (L5, same day).** Neither headline
number moved, and both favorite bets lost. The missing 5.3% of transplantable meaning is NOT
hiding in the certified door channels: adding the certified door read (summarized or in full)
moves the model exactly 0% further —
it is certified to live in genuinely un-charted dark mass outside the whole dictionary. It
resisted every translation method we tried: it transfers only as its exact raw configuration,
never through any compressed or named form. And editing the
rung cleared none of the four channels we can read it through (the honest dose story is above).
Both remainders are
closed properties now, not open wounds; the honest claim is sharper, not bigger.

**And the questions those answers opened are finished too (L6, same day).** We hunted the 5.3% to
ground. It is DIFFUSE: smeared across the entire 329-dimension dark space — no hidden low-rank
concept (we tried every rank up to 256; none captures 80% of the gap, and a RANDOM 256-dim slice
of the dark does nearly as well as the best hand-picked one). And it is mostly word-less: of its
8 biggest directions, only 2 faintly cross the naming bar, through side channels, with no stable
meaning (they're recorded as provisional dark signatures, NOT dictionary entries). The rung stays
steering-unusable at double dose (above). And the one L4 oddity we'd never explained — the "operator"
axis appearing to steer on-manifold when it was predicted inert — dissolves: it was read-out ECHO
(~94% of the response is the injected word-vector riding straight through to the output; the
computed part is inside the noise), so no new capability, and the L4 result's own control always
held. L6's scoreboard: 2 favorite bets hit, 3 lost — every loss logged as a certified finding.
No headline number moved, in any of it.

**Deliverables ready for your review:** PAPER_DRAFT_V1.md (+ 6 figures in paper_figs/, all
regenerable from the frozen JSONs by one script; L5 verdicts in §6.6, L6 verdicts in §6.7, new
Fig. 6 = the dark-mass rank ladder) and the outreach kit (AF post, 4 emails, Zenodo + GitHub
checklists, release sequence, and the new GitHub-front-door README_DRAFT.md you asked for) in
outreach_kit/, all updated post-L6 and standardized to the ratified name "the BABEL codec".
Nothing has been sent, posted, uploaded, or committed anywhere — every send is yours to fire.

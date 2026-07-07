# EXAMPLES -- reading GPT-2's thinking, mid-sentence

*This is the frozen reference transcript for `demo/read_a_mind.py`. Run `python demo/read_a_mind.py`
from the repo root to reproduce every table below (the script self-checks its readout against these
numbers and exits non-zero on any miss).*

**The sentence** (stopped before the model gets to finish it):

> The old captain stared at the horizon, knowing the storm would sink his

**What GPT-2 says next** (top-5 next-token predictions after "...sink his"):

| rank | token | probability |
|---|---|---|
| 1 | ` ship` | **62.8%** |
| 2 | ` ships` | 3.2% |
| 3 | ` vessel` | 2.4% |
| 4 | ` boat` | 2.1% |
| 5 | ` own` | 0.7% |

The model has decided the captain is about to lose his **ship**. Below we open the residual
stream at three depths and read the internal state in the model's own certified vocabulary,
BEFORE that word is ever produced.

---
## HOW THIS WAS READ (method, 1 paragraph)
Demonstration readout only -- frozen certified machinery, READ-ONLY, no new science, no steering.
GATE-0 hash checks all passed (`artifacts/decoder_v7_tensors.pt` `b1d2f464c00c3ef6`,
`artifacts/_l3_encoder.pt` `6be189567c41e91d`, `artifacts/LEXICON_V3.md` `71a51619a9bb25c3`,
`artifacts/_l6_bases.pt` `a60a0ab67b85c410`); the encoder==decoder-reader cross-check was exact
(max|diff| 0.0 on C and mu). One fp32 CPU forward pass; residuals captured at boundaries BUS[0]
(post-embedding), BUS[6] (after block 5) and BUS[11] (after block 10). Each state is decoded as
mu-centered coordinates `(h - mu[b]) @ v` against every lexicon entry certified at that boundary:
the 19 core fields (read at all boundaries), corridor words at their home room, LEXICON_V3
folded-read words at their home/alias cells, and the two LEXICON_V4 provisional dark entries at
b6. Salience `z` = coordinate / that entry's standing std over a 16x512 WikiText-103 prose bank
at the same boundary (the public demo ships those stds frozen and hash-gated in
`demo/standing_stats.json`; live field stds match the decoder's frozen phi_std within
0.96-1.29x). Entries whose certified verdict is CERTIFIED-NO-GLOSS are shown dark, exactly as
certified -- no invented readings.

**How to read z**: z is "how far this coordinate sits from its standing prose mean, in units of
its own normal variation." |z|~1 is unremarkable; |z|>=2 is a genuinely displaced read. Sign is
direction along the certified axis, not goodness.

---
## PROBE 1 -- BUS[0] (post-embedding) at the final token ` his`
*Only the 19 core fields are certified this early; corridor/fold words live deeper.*

| # | entry | verdict | z | certified meaning |
|---|---|---|---|---|
| 1 | field 18 | NAMED (A) | +2.5 | @-format |
| 2 | field 7 | NAMED (A) | -1.5 | formula/markup-symbol |
| 3 | field 3 | **STILL-DARK** | +1.5 | (no gloss -- read as a number only) |
| 4 | field 6 | NAMED-CONDITIONED | -1.4 | epistemic-negative |
| 5 | field 14 | NAMED-CONDITIONED | +1.2 | comma-boundary / dramatic-event |
| 6 | field 9 | NAMED (A) | -1.2 | sports-team |
| 7 | field 0 | NAMED (B) | -0.8 | naval/warship |
| 8 | field 16 | NAMED-CONDITIONED | +0.8 | spatial-preposition/@ |

**What it's noticing:** almost nothing yet. At the embedding layer the word ` his` is a plain
little function word and the certified reads say exactly that: every |z| < 2.5, the code/markup
fields (7) and sports field (9) are mildly *below* their prose mean, and the only positive reads
are format/boundary-flavored (18, 14, 16). Even the naval field (0) is slightly negative here --
at BUS[0] the model sees the token, not the story. The one moderately loud entry after field 18
is field 3, which the lexicon holds as STILL DARK: we can see it move (+1.5) but we have no
certified name for what moved.

---
## PROBE 2 -- BUS[6] (mid-stack) at the token ` storm` (the contrast probe)
*48 certified entries live here: 19 fields, 2 corridor words, 25 code_b6 folded-read words, 2 provisional dark entries. This is the loudest state we probed (residual norm 65.4).*

| # | entry | verdict | z | certified meaning |
|---|---|---|---|---|
| 1 | field 14 | NAMED-CONDITIONED | **+3.0** | comma-boundary / dramatic-event |
| 2 | fold code_b6_d19 | NAMED | **+2.6** | axis whose certified +push raises **SHIP**, SELECT, ... (write-image) |
| 3 | field 3 | **STILL-DARK** | -2.3 | (no gloss) |
| 4 | fold code_b6_d3 | **CERTIFIED-NO-GLOSS** | -2.3 | (dark -- certified, unnamed) |
| 5 | fold code_b6_d24 | **CERTIFIED-NO-GLOSS** | +2.2 | (dark) |
| 6 | fold code_b6_d34 | **CERTIFIED-NO-GLOSS** | +2.2 | (dark) |
| 7 | fold code_b6_d23 | **CERTIFIED-NO-GLOSS** | -2.2 | (dark) |
| 8 | fold code_b6_d21 | **CERTIFIED-NO-GLOSS** | -2.0 | (dark) |

(next: corridor b6_d13 "assignment-context/'='-anchor" at -2.0, i.e. pushed *away* from its
code/'='-context pole -- sensible for a prose token; fold code_b6_d0 "code-whitespace/glitch-pole
carrier" +2.0.)

**What it's noticing / planning at "storm":** two named reads stand out. First, the
comma-boundary / **dramatic-event** field is the single loudest certified entry (+3.0) -- the
storm token sits right where the sentence pivots into its dramatic clause, and the model's
mid-stack state is displaced hard along the axis the lexicon associates with exactly that.
Second -- the demo's best moment -- the folded-read word `code_b6_d19`, whose *certified causal
write-image is "+push raises [SHIP, ...]"*, is elevated at +2.6 at the word ` storm`: four
tokens before the model actually says " ship", a certified ship-writing carrier is already hot.
(Honest scope: that entry's certification is 1/3 channels, stable prose+code; this is a readout
association, not a causal claim about this sentence.) And third, honestly: five of the top eight
entries are CERTIFIED-NO-GLOSS -- most of what is loud in this state is mass the program has
certified as real but has *no name for*. We say "dark," not a story.

---
## PROBE 3 -- BUS[6] (mid-stack) at the final token ` his`

| # | entry | verdict | z | certified meaning |
|---|---|---|---|---|
| 1 | field 18 | NAMED (A) | +1.8 | @-format |
| 2 | field 3 | **STILL-DARK** | -1.6 | (no gloss) |
| 3 | field 15 | NAMED (A) | -1.5 | mixed-measurement |
| 4 | field 8 | NAMED (A) | +1.4 | **harm/casualty** |
| 5 | fold code_b6_d7 | NAMED-REGIME-SPECIFIC (code) | -1.3 | code-whitespace fragment carrier |
| 6 | dark_b6_svd7 | **PROVISIONAL, dark, INCOHERENT** | +1.2 | (crosses NAMED bar by rubric only; no interpretable concept) |
| 7 | fold code_b6_d19 | NAMED | -1.1 | the SHIP-riser axis (here mildly *below* mean) |
| 8 | fold code_b6_d41 | **CERTIFIED-NO-GLOSS** | -1.1 | (dark) |

**What it's noticing:** at ` his` the mid-stack is quiet -- no certified entry reaches |z|=2.
The most story-like read is **harm/casualty at +1.4** (the state just processed "would sink"),
with measurement/number content suppressed (-1.5) -- but at ~1.4 standing sigmas these are
tendencies, not certified spikes, and we flag them as such. Note the SHIP-riser axis that was
hot at "storm" is *not* elevated here (-1.1): at this boundary and position, whatever carries
the upcoming "ship" is not strongly visible in the named vocabulary. One of the two LEXICON_V4
provisional dark entries (svd7) is present at +1.2; the lexicon itself calls it semantically
incoherent, so it contributes no reading.

---
## PROBE 4 -- BUS[11] (late-stack) at the final token ` his`
*60 certified entries live here (fields + rep_b11/code_b11 folded-read words). Residual norm 125.5 -- the state is big, but the named vocabulary reads only modest displacements.*

| # | entry | verdict | z | certified meaning |
|---|---|---|---|---|
| 1 | fold b11_d39 | **CERTIFIED-NO-GLOSS** | -1.9 | (dark) |
| 2 | field 3 | **STILL-DARK** | -1.9 | (no gloss) |
| 3 | fold code_b11_d35 | NAMED | -1.8 | +push raises srf/lessly/etheless... (fragment write-image) |
| 4 | field 12 | NAMED (A) | -1.6 | local-relation/admin |
| 5 | fold b11_d43 | **CERTIFIED-NO-GLOSS** | +1.5 | (dark) |
| 6 | fold b11_d5 | NAMED-REGIME-SPECIFIC (repetition) | +1.4 | repetition-locked alternation carrier |
| 7 | field 18 | NAMED (A) | +1.4 | @-format |
| 8 | field 1 | NAMED-CONDITIONED | -1.3 | collegiate-sports |

**What it's planning -- and the honest punchline:** behaviorally the plan is fully formed one
boundary later (" ship" at 63%). But in the certified vocabulary at BUS[11], nothing nautical
and nothing ship-like is loudly displaced: the top reads are a no-gloss fold dim, the dark
field 3, and word-fragment carriers, all under |z|=2. The plan is *in there* -- the logits prove
it -- but it is being carried by state the certified dictionary mostly cannot name. That is not
a failure of the demo; it is the program's own measured result showing up live: the late-stack
dark mass is diffuse and word-poor (L6: DIFFUSE, 6/8 top dark directions no-gloss; L7: the dark
is NOT-COMPRESSIBLE from the readable subspace). When the dictionary has no word, the honest
read is "dark," and most of this state is dark.

*Context for this probe: after ` storm` (mid-sentence) the model's next-token belief was still
generic continuation -- was 42.5%, would 17.0%, had 9.6% -- so the specific "sink his ship"
commitment crystallized in the last clause, exactly where Probe 2 caught the dramatic-event
field and the SHIP-riser carrier lighting up.*

---
## WHAT THIS DEMO SHOWS (and does not)
- **Shows**: the frozen decoder stack (decoder_v7 reader + LEXICON_V3/V4, hash-gated) can be
  pointed at any single forward pass and produce a certified, per-boundary readout with honest
  dark/no-gloss labels -- mid-sentence, in seconds, on CPU.
- **Best single read**: at ` storm`, mid-stack: dramatic-event field +3.0 plus a certified
  SHIP-writing carrier at +2.6, four tokens before " ship" (63%) is emitted.
- **Does NOT show**: causal claims about this sentence (nothing was steered; all reads are
  observational); a full account of the plan (most late-stack salience is CERTIFIED-NO-GLOSS,
  consistent with L6/L7); anything about the naval/warship field, which stayed quiet (|z|<=0.8)
  at every probe we took -- reported as measured.
- Scope notes: z is display-only normalization against a 16x512 prose standing bank; fields are
  read at all boundaries by decoder convention, corridor/fold words only at their certified
  home/alias boundaries; the two V4 dark entries are provisional and contributed no reading.

Artifacts: `demo/read_a_mind.py` (the runnable readout, self-checking against this transcript),
`demo/standing_stats.json` (frozen z-normalization stds, hash-gated), `artifacts/` (the frozen
certified record this demo reads with). Field-name glosses are the frozen decoder lexicon's
short names (LEXICON_V1/V2 per-field pages, carried unchanged into LEXICON_V3 Section 1).

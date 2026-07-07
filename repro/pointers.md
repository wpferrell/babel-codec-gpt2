# repro/pointers.md — script → artifact map, streams, seeds
## Script → result artifact

| script | regenerates | consumes (frozen, hash-gated at GATE-0) | full-run GPU time | smoke env |
|---|---|---|---|---|
| `_v6.py` | `_v6_result.json` (wall-surrogate certification, capacity-hurts falsifier) | decoder_v6 pair, `_v5_floors_recal.json` | 1821.0 s | `V6_SMOKE=1` |
| `_v7.py` | `_v7_result.json` (final 39/39 both-meter verdict; C1 discharge; b6/b7 onset rungs) | decoder_v7 pair, `_v5_floors_recal.json` | 1553.7 s | `V7_SMOKE=1` |
| `_l1.py` | `_l1_result.json`, `_l1_bases.pt` (351-channel adjudication behind LEXICON_V3.md) | decoder_v7 pair, `_v5_floors_recal.json` | 4647.3 s (leg 3 of 3) | `L1_SMOKE=1` |
| `_l2babel.py` | `_l2babel_result.json`, `_l2babel_maps.pt` (36/36 seam law behind GRAMMAR_TABLE_V1.json) | decoder_v7 pair, LEXICON_V3.md, `_v5_floors_recal.json` | 3172.5 s | `L2B_SMOKE=1` |
| `_l3.py` | `_l3_result.json` (encoder well-posedness M1–M3 behind ENCODER_V1 + WELLPOSEDNESS/OFFSPAN tables) | decoder_v7 pair, GRAMMAR_TABLE_V1.json, `_l2babel_maps.pt` | 129.6 s | `L3_SMOKE=1` |
| `_l4.py` | `_l4_result.json`, `_l4_bases.pt` (speak test T1/T2/T3) | decoder_v7 pair, ENCODER_V1 (`_l3_encoder.pt`), LEXICON_V3.md, floors | 74.9 s | `L4_SMOKE=1` |
| `_l5.py` | `_l5_result.json` (remainder closure: Arm A transplant-gap attribution, Arm B rung read-only) | decoder_v7 pair, ENCODER_V1, floors, LEXICON/GRAMMAR/maps + wellposedness/offspan | 96.1 s | `L5_SMOKE=1` |
| `_l6.py` | `_l6_result.json`, `_l6_bases.pt` (dark-mass DIFFUSE/NAMED-SOME/re-transplant; rung listeners/OQ-4/echo) | same 8-hash set as `_l5.py` | 727.7 s | `L6_SMOKE=1` |

Every script: fp32, eager attention, TF32 off, `torch.manual_seed(1234)`, batch shape MB=4 for
comparison forwards (identity-injection sanity requires capturing clean logits at the SAME batch
shape), BelowNormal process priority, atomic `*.json.tmp → os.replace` checkpoints with
resume-skip.

## Streams (deterministic; identical construction across all harnesses)

- **prose** — `wikitext-2-raw-v1`, `split="test"`, all non-empty lines joined with `\n`,
  GPT-2-tokenized; holdout = token window `[24576, 24576 + 16·512)` viewed as 16 blocks × 512
  tokens (the "fresh window" `FRESH_LO=24576`, disjoint from all fit data).
- **code** — `openai_humaneval` test set, `prompt + canonical_solution` concatenated over all
  tasks, GPT-2-tokenized; holdout = same window arithmetic as prose.
- **repetition** — synthetic induction streams: for each of 16 blocks, draw `IND_SEG=64` tokens
  uniformly from `[0, 50256)` with `torch.Generator().manual_seed(3)` (`REP_SEED=3`) and tile the
  segment to 512 tokens (period 64). Held-out seeds and periods are reserved for the surrogate
  falsifiers (SACRED sets inside `_v6.py`/`_v7.py`).

## Null families and seeds

- Sigma-matched naming nulls (`_l1.py`): B_NULL = 12–20 per channel, seeds logged per entry in
  the result JSON / LEXICON evidence hashes.
- Matched-random substitution/edit nulls (`_l4.py`/`_l5.py`): N_NULLDIR = 3 at the L4/L5 stage
  (pen-disclosed; see the L6 honest-N re-arm and the post-audit N=20 re-draw for the tightened
  ±3σ null).
- L6 fresh null seed family (pre-registered in `_l6.py` header): `20260707 + {3, 11, 17, 23, 29}`
  for {Arm-A rank-null, B1 listeners, B2 write-null, B3 computed-null, OQ-4 dose-null};
  N_NULL_B = 12, N_NULL_OQ4 = 20.

## Verifying without a GPU

`figs/make_paper_figs.py` (CPU, numpy+matplotlib) regenerates all 6 paper figures from 9 frozen
result JSONs alone — run it from a directory whose PARENT contains those JSONs (in the repo:
`cp artifacts/*.json . && python figs/make_paper_figs.py`). Hash verification
(`sha256sum artifacts/*` vs `HASHES.txt`) needs no Python at all.

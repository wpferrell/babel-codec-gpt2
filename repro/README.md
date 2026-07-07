# repro/README.md — reproducing the verdict rows
Everything in the paper ran on ONE workstation GPU (NVIDIA RTX A4500, 20 GB), fp32, eager
attention, TF32 off. There is no scale barrier between you and any number: the cheapest verdict
script below runs in ~75 s, the most expensive in ~78 min.

## Requirements

```
pip install torch transformers datasets numpy   # CUDA build of torch; ~20 GB VRAM for the largest runs
```

The scripts download `gpt2` (124M) from Hugging Face plus two public datasets
(`wikitext-2-raw-v1` test split; `openai_humaneval`). The repetition regime is generated locally
from a fixed seed — see `pointers.md` for the exact stream definitions.

## The one honest deviation you must make

The harnesses are shipped **byte-verbatim** — their sha256[:16] hashes match the paper's
Appendix A. Each one hardcodes the lab directory near the top:

```python
DIR = r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
```

To re-run, place the `artifacts/` files and the script in one directory and set `DIR` to that
directory (one line). This edit changes the script's hash — expected and disclosed; the shipped
file is the one that matches the paper. Everything else must stay untouched: every script starts
with a GATE-0 that re-hashes its frozen inputs (decoder, encoder, floors, lexicon, grammar) against
locked constants and **aborts on any mismatch**, then runs an identity-injection exact-zero check
before any verdict is read. If a gate fails, your inputs differ — that is the system working.

## How to run one row

Each script supports a smoke mode via environment variable (e.g. `L6_SMOKE=1 python _l6.py`) that
exercises the full pipeline at toy sizes first. Then run full:

```
python _l4.py     # example: the speak test (T1/T2/T3) — ~75 s GPU
```

Results are written atomically to the script's `*_result.json`; compare against the shipped
artifact (they should reproduce to the digit at the stated roundings — forward passes are fp32,
TF32 off, fixed seeds, fixed batch shapes). The per-script → artifact map, GPU times, and stream
windows/seeds are in `pointers.md`.

## Which script proves which Table-1 cell

| Table 1 (last row) cell | script | artifact |
|---|---|---|
| (1) whole-model coverage, 39/39 at floor | `_v7.py` | `_v7_result.json` |
| (2) 351/351 channels adjudicated vs sigma-matched nulls | `_l1.py` | `_l1_result.json` (+ LEXICON_V3.md counts) |
| (2)/(3) 36/36 seam-cells linear-certified | `_l2babel.py` | `_l2babel_result.json` (+ GRAMMAR_TABLE_V1.json) |
| (3) exact algebraic inverse, 39/39 well-posed | `_l3.py` | `_l3_result.json` (+ ENCODER_V1) |
| (4) reconstruct / transplant / human-edit | `_l4.py` | `_l4_result.json` |
| remainder certified (5.3% outside dictionary; rung dose story) | `_l5.py`, `_l6.py` | `_l5_result.json`, `_l6_result.json` |
| wall surrogate certification (capacity-hurts falsifier) | `_v6.py` | `_v6_result.json` |

If you re-run a row and get a different digit, open an issue — that is exactly what the hashes
are for.

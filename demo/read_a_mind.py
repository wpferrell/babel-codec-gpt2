"""read_a_mind.py -- live demo: read GPT-2's internal state, mid-sentence, in its own
certified vocabulary (the BABEL codec, https://github.com/wpferrell/babel-codec-gpt2).

Requirements:  pip install torch transformers     (CPU only; first run downloads gpt2, ~500MB)
Run from anywhere inside the cloned repo:         python demo/read_a_mind.py
Custom sentence:                                  python demo/read_a_mind.py --sentence "..."
Extra probe position (0-based token index):       python demo/read_a_mind.py --pos 10

What it does -- READ-ONLY, no steering, no new claims:
1. GATE-0: SHA-256-checks the frozen artifacts (fail loud if missing or modified) and
   cross-checks that the shipped encoder is the exact inverse of the decoder reader.
2. Runs one fp32 CPU forward pass of GPT-2 small on the sentence and captures the residual
   stream at boundaries BUS[0] (post-embedding), BUS[6] (after block 5), BUS[11] (after
   block 10).
3. Decodes each probed state against every lexicon entry certified at that boundary --
   the 19 core fields, LEXICON_V3 corridor words at their home room, LEXICON_V3 folded-read
   words at their home/alias cells, and the two LEXICON_V4 provisional dark entries at b6 --
   and prints the top-8 by salience with their certified verdict labels (NAMED /
   NAMED-CONDITIONED / STILL-DARK / CERTIFIED-NO-GLOSS). Entries certified word-less are
   shown dark, exactly as certified: no invented readings.
4. Prints GPT-2's top-5 next-token predictions for context.

Salience z = mu-centered coordinate (h - mu[b]) @ v divided by that entry's standing std over
a 16x512 WikiText-103 prose bank at the same boundary (display-only normalization; the stds
are shipped frozen in demo/standing_stats.json and hash-gated like everything else).
|z| ~ 1 is unremarkable; |z| >= 2 is a genuinely displaced read.

On the default sentence the script self-checks its readout against the frozen reference values
(tolerance |dz| <= 0.25, |dp| <= 0.02) and exits non-zero on any miss.

Example transcript with full narration: demo/EXAMPLES.md
"""
import argparse
import hashlib
import os
import re
import sys

import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "artifacts")
DEMO = os.path.join(ROOT, "demo")

# locked SHA-256 prefixes (16 hex; full values in HASHES.txt at the repo root / paper Appendix A)
LOCKED = {
    os.path.join(ART, "decoder_v7_tensors.pt"): "b1d2f464c00c3ef6",
    os.path.join(ART, "_l3_encoder.pt"): "6be189567c41e91d",
    os.path.join(ART, "LEXICON_V3.md"): "71a51619a9bb25c3",
    os.path.join(ART, "_l6_bases.pt"): "a60a0ab67b85c410",
    os.path.join(ROOT, "paper", "LEXICON_V4_ADDENDUM.md"): "fa9c86e4667ff932",
    os.path.join(DEMO, "standing_stats.json"): "51e6110af2bdc9ab",
}

DEFAULT_SENTENCE = "The old captain stared at the horizon, knowing the storm would sink his"
BOUNDS = [0, 6, 11]                # BUS[0]=post-embed, BUS[6]=after block 5, BUS[11]=after block 10
TOPN = 8

# the 19 core fields: short names from the frozen decoder lexicon (per-field pages: LEXICON_V1/V2,
# carried unchanged into LEXICON_V3 Section 1); verdict grades as certified there
FIELD_NAME = {
    0: "naval/warship", 1: "collegiate-sports", 2: "special-symbol<->temporal-connective",
    3: "L0 magnitude/anomalous-token(numeric)", 4: "place-name<->statistics",
    5: "clause-final/physical-process", 6: "epistemic-negative", 7: "formula/markup-symbol",
    8: "harm/casualty", 9: "sports-team", 10: "punctuation-boundary(struct)",
    11: "coastal-storm/geography", 12: "local-relation/admin", 13: "quotation/boundary",
    14: "comma-boundary(struct)", 15: "mixed-measurement", 16: "spatial-prep/@",
    17: "hyphen/@-format", 18: "@-format",
}
FIELD_STATUS = {i: ("NAMED" if i in (0, 2, 7, 8, 9, 10, 11, 12, 15, 17, 18) else
                    ("STILL-DARK" if i == 3 else "NAMED-CONDITIONED")) for i in range(19)}

# the two LEXICON_V4_ADDENDUM provisional dark entries (b6 only); glosses quoted from that record
DARK_META = {
    "dark_b6_svd4": {"col": 4, "verdict": "NAMED (provisional, dark)",
                     "gloss": "faint WATERCOURSE / TERRAIN-FEATURE tendency (River/Creek/cavern) "
                              "in the free-text regimes; NON-WU (no vocabulary gloss); provisional, "
                              "not in the certified dictionary (LEXICON_V4_ADDENDUM)"},
    "dark_b6_svd7": {"col": 7, "verdict": "NAMED (provisional, dark; INCOHERENT)",
                     "gloss": "SEMANTICALLY INCOHERENT across regimes (numerals/bapt-/container-"
                              "types); crosses the NAMED bar by rubric only; NON-WU; provisional "
                              "(LEXICON_V4_ADDENDUM)"}}

# frozen reference readout for the default sentence (from the original MINDREAD run; see
# demo/EXAMPLES.md). checked whenever the default sentence is used.
REFERENCE = {
    "next_top1": (" ship", 0.6284),
    "anchors": [  # (boundary, position-key, entry id, expected z)
        (0, "final", "field_18", 2.49),
        (6, "final", "field_18", 1.83),
        (6, "storm", "field_14", 3.01),
        (6, "storm", "fold_O_r48_code_b6_d19", 2.55),
        (11, "final", "fold_O_r48_b11_d39", -1.88),
        (11, "final", "field_3", -1.86),
    ],
    "z_tol": 0.25, "p_tol": 0.02,
}


def sha16(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def fail(msg):
    print(f"\nFATAL: {msg}", file=sys.stderr)
    sys.exit(2)


def unit(v):
    return v / v.norm().clamp(min=1e-9)


def main():
    ap = argparse.ArgumentParser(description="Read GPT-2's mind in its own certified vocabulary.")
    ap.add_argument("--sentence", default=DEFAULT_SENTENCE)
    ap.add_argument("--pos", type=int, default=None,
                    help="extra 0-based token position to probe at all three boundaries")
    args = ap.parse_args()

    # ---------- GATE-0: frozen artifact hashes ----------
    print("GATE-0: checking frozen artifact hashes ...")
    for path, locked in LOCKED.items():
        if not os.path.exists(path):
            fail(f"missing frozen artifact: {path}")
        got = sha16(path)
        if got != locked:
            fail(f"hash mismatch for {os.path.relpath(path, ROOT)}: got {got}, locked {locked} "
                 f"-- artifact modified; this demo only speaks for the frozen record")
        print(f"  ok  {got}  {os.path.relpath(path, ROOT)}")

    # ---------- load frozen reader; GATE-0b: encoder == decoder reader ----------
    D7 = torch.load(os.path.join(ART, "decoder_v7_tensors.pt"), map_location="cpu",
                    weights_only=False)
    ENC = torch.load(os.path.join(ART, "_l3_encoder.pt"), map_location="cpu", weights_only=False)
    xdiff = {nm: float((ENC[nm].float() - D7[nm].float()).abs().max()) for nm in ("C", "mu")}
    if any(v > 1e-6 for v in xdiff.values()):
        fail(f"encoder/decoder reader cross-check failed: max|diff| {xdiff}")
    print(f"GATE-0b: encoder == decoder reader (max|diff| {xdiff}) -- pass")
    C = D7["C"].float()                    # [768,19] core fields
    mu = D7["mu"].float()                  # [13,768] per-boundary means
    V35 = D7["V35"].float()                # [768,35] corridor directions
    L6B = torch.load(os.path.join(ART, "_l6_bases.pt"), map_location="cpu", weights_only=False)
    dark_dirs = L6B["armA_selected_dirs"].float()   # [768,8]

    # ---------- parse LEXICON_V3 (Sections 2+3: corridor + folded-read words) ----------
    lex_lines = open(os.path.join(ART, "LEXICON_V3.md"), encoding="utf-8").read().splitlines()
    corr_re = re.compile(r"^--- (b(\d+)_d(\d+)) \(j=(\d+)\) \[([^\]]+)\] -> \*\*([^*]+)\*\* ---")
    fold_re = re.compile(r"^--- (fold_(O_r48_\S+)_d(\d+)) share=([0-9.]+)"
                         r"((?:; aliases: .*?)?) -> \*\*([^*]+)\*\* ---")
    alias_re = re.compile(r"([A-Za-z]+_b\d+)#d(\d+)\(dot ([0-9.]+)\)")

    def grab_gloss(i):
        g = []
        j = i + 1
        while j < len(lex_lines):
            ln = lex_lines[j].strip()
            if ln.startswith("GLOSS:"):
                g.append(ln[6:].strip())
            elif g and not ln.startswith("evidence"):
                g.append(ln)
            if ln.startswith("evidence") or ln.startswith("---"):
                break
            j += 1
        return " ".join(g).strip() or None

    def cell_boundary(cell):               # "O_r48_b8" / "O_r48_code_b4" / "O_r48_prose_b12"
        m = re.match(r"O_r48_(?:(code|prose)_)?b(\d+)$", cell)
        return (m.group(1) or "repetition"), int(m.group(2))

    corr_words, fold_words = {}, {}
    for i, ln in enumerate(lex_lines):
        m = corr_re.match(ln)
        if m:
            wid, room = m.group(1), int(m.group(2))
            corr_words[wid] = {"j": int(m.group(4)), "boundary": room,
                               "verdict": m.group(6).strip(), "gloss": grab_gloss(i)}
            continue
        m = fold_re.match(ln)
        if m:
            wid, cell = m.group(1), m.group(2)
            _reg, b = cell_boundary(cell)
            bset = {b}
            for am in alias_re.finditer(m.group(5) or ""):
                bset.add(int(am.group(1).rsplit("_b", 1)[1]))
            fold_words[wid] = {"cell": cell, "dim": int(m.group(3)),
                               "verdict": m.group(6).strip(), "boundaries": sorted(bset),
                               "gloss": grab_gloss(i)}
    if len(corr_words) != 35:
        fail(f"expected 35 corridor entries in LEXICON_V3, parsed {len(corr_words)}")
    print(f"lexicon parsed: 19 fields, {len(corr_words)} corridor words, "
          f"{len(fold_words)} folded-read words, 2 provisional dark entries (b6)")

    # ---------- entry table per probe boundary ----------
    def entries_for(b):
        ents = []
        for i in range(19):
            ents.append({"id": f"field_{i}", "verdict": FIELD_STATUS[i],
                         "gloss": FIELD_NAME[i], "vec": unit(C[:, i])})
        for wid, w in corr_words.items():
            if w["boundary"] == b:
                ents.append({"id": wid, "verdict": w["verdict"], "gloss": w["gloss"],
                             "vec": unit(V35[:, w["j"]])})
        for wid, w in fold_words.items():
            if b in w["boundaries"]:
                ents.append({"id": wid, "verdict": w["verdict"], "gloss": w["gloss"],
                             "vec": unit(D7[w["cell"]].float()[:, w["dim"]])})
        if b == 6:
            for wid, meta in DARK_META.items():
                ents.append({"id": wid, "verdict": meta["verdict"], "gloss": meta["gloss"],
                             "vec": unit(dark_dirs[:, meta["col"]])})
        return ents

    ENTS = {b: entries_for(b) for b in BOUNDS}

    # ---------- frozen standing stds (z normalization) ----------
    import json
    stats = json.load(open(os.path.join(DEMO, "standing_stats.json"), encoding="utf-8"))
    STD = {}
    for b in BOUNDS:
        per_id = stats["std"][str(b)]
        missing = [e["id"] for e in ENTS[b] if e["id"] not in per_id]
        if missing:
            fail(f"standing_stats.json missing entries at BUS[{b}]: {missing[:5]} ...")
        STD[b] = torch.tensor([per_id[e["id"]] for e in ENTS[b]])

    # ---------- model: one fp32 CPU forward pass, read-only ----------
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print("loading gpt2 (fp32, eager, CPU) ...")
    tok = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2", torch_dtype=torch.float32,
                                                 attn_implementation="eager").eval()
    for p in model.parameters():
        p.requires_grad_(False)

    cap = {}

    def mk(key):
        def hook(_m, _i, out):
            cap[key] = (out[0] if isinstance(out, tuple) else out).detach()
        return hook
    blocks = list(model.transformer.h)
    hooks = [model.transformer.drop.register_forward_hook(mk(0)),
             blocks[5].register_forward_hook(mk(6)),
             blocks[10].register_forward_hook(mk(11))]

    ids = tok(args.sentence, return_tensors="pt")["input_ids"]
    toks = [tok.decode([int(t)]) for t in ids[0]]
    T = ids.shape[1]
    final_pos = T - 1
    with torch.no_grad():
        logits = model(ids, use_cache=False).logits[0]
    for h in hooks:
        h.remove()
    H = {b: cap[b][0].float() for b in BOUNDS}

    print(f"\nSENTENCE ({T} tokens): {args.sentence!r}")

    def top5_next(pos):
        pr = torch.softmax(logits[pos].float(), -1)
        tv, ti = torch.topk(pr, 5)
        return [(tok.decode([int(i)]), float(p)) for p, i in zip(tv, ti)]

    next5 = top5_next(final_pos)
    print(f"\nTOP-5 NEXT-TOKEN after {toks[final_pos]!r}:")
    for t, p in next5:
        print(f"  {t!r:<16} {100 * p:5.1f}%")

    # ---------- decode probes ----------
    checked_z = {}

    def decode(b, pos, poskey):
        r = H[b][pos] - mu[b]
        Vm = torch.stack([e["vec"] for e in ENTS[b]], 1)
        w = r @ Vm
        z = w / STD[b].clamp(min=1e-9)
        for k, e in enumerate(ENTS[b]):
            checked_z[(b, poskey, e["id"])] = float(z[k])
        order = torch.argsort(z.abs(), descending=True)[:TOPN]
        print(f"\nPROBE BUS[{b}] at token {toks[pos]!r} (pos {pos}) -- "
              f"{len(ENTS[b])} certified entries, residual norm {float(r.norm()):.1f}")
        print(f"  {'#':>2} {'z':>6}  {'entry':<26} {'verdict':<38} certified meaning")
        for rank, k in enumerate(order.tolist(), 1):
            e = ENTS[b][k]
            gloss = e["gloss"] if e["gloss"] else "(dark -- certified, unnamed)"
            if len(gloss) > 96:
                gloss = gloss[:93] + "..."
            print(f"  {rank:>2} {float(z[k]):+6.2f}  {e['id']:<26} {e['verdict']:<38} {gloss}")

    probes = [(b, final_pos, "final") for b in BOUNDS]
    storm_hits = [i for i, s in enumerate(toks) if s.strip() == "storm"]
    if args.sentence == DEFAULT_SENTENCE and len(storm_hits) == 1:
        probes.insert(2, (6, storm_hits[0], "storm"))
        print(f"\n(default sentence: adding the contrast probe BUS[6] at ' storm', "
              f"pos {storm_hits[0]}, plus next-token there)")
        n5s = top5_next(storm_hits[0])
        print(f"TOP-5 NEXT-TOKEN after {toks[storm_hits[0]]!r}: "
              + ", ".join(f"{t!r} {100 * p:.1f}%" for t, p in n5s))
    if args.pos is not None:
        if not (0 <= args.pos < T):
            fail(f"--pos {args.pos} outside sentence (0..{T - 1})")
        probes += [(b, args.pos, f"pos{args.pos}") for b in BOUNDS]
    for b, pos, poskey in probes:
        decode(b, pos, poskey)

    # ---------- self-check on the default sentence ----------
    if args.sentence == DEFAULT_SENTENCE:
        print("\nSELF-CHECK vs frozen reference readout:")
        ok = True
        t1, p1 = next5[0]
        cond = t1 == REFERENCE["next_top1"][0] and abs(p1 - REFERENCE["next_top1"][1]) <= REFERENCE["p_tol"]
        ok &= cond
        print(f"  {'ok' if cond else 'MISS':>4}  next-token top1 {t1!r} p={p1:.4f} "
              f"(expected {REFERENCE['next_top1'][0]!r} p={REFERENCE['next_top1'][1]})")
        for b, poskey, eid, zexp in REFERENCE["anchors"]:
            zgot = checked_z.get((b, poskey, eid))
            cond = zgot is not None and abs(zgot - zexp) <= REFERENCE["z_tol"]
            ok &= cond
            print(f"  {'ok' if cond else 'MISS':>4}  BUS[{b}]@{poskey} {eid}: z={zgot:+.2f} "
                  f"(expected {zexp:+.2f})")
        if not ok:
            print("SELF-CHECK FAILED", file=sys.stderr)
            sys.exit(1)
        print("SELF-CHECK PASS -- readout reproduces the frozen reference within tolerance")

    print("\nDone. Read-only demo: nothing was steered, nothing was written. Entries the record")
    print("certifies as word-less are shown dark -- when the dictionary has no word, the honest")
    print("read is 'dark'. Full narrated example: demo/EXAMPLES.md")


if __name__ == "__main__":
    main()

# make_paper_figs.py -- PAPER_DRAFT_V1 figures, reproducible from frozen artifacts ONLY (CPU, matplotlib).
# Run from CONSTRUCTIVE\paper_figs\:  python make_paper_figs.py
# Inputs (all frozen, hashes in the closeouts):
#   ..\_open6_result.json      OPEN-6 verdict + gap table          (OPEN_CAMPAIGN_CLOSEOUT.md)
#   ..\_v2_result.json         V2 S5 gap table                     (V2_CLOSEOUT.md)
#   ..\_v3_result.json         V3 S7 gap table + rank curves       (V3_CLOSEOUT.md)
#   ..\_v4_result.json         V4 verdict + rep_b12 rank extension (V4_CLOSEOUT.md)
#   ..\_v5_result.json         V5 both-meter verdict tables        (V5_CLOSEOUT.md)
#   ..\_v6_result.json         V6 surrogate ladder + both meters   (V6_CLOSEOUT.md, dcb767be66434df3)
#   ..\_v7_result.json         V7 final both-meter 39-cell tables  (V7_CLOSEOUT.md, e293979a6be37109)
#   ..\_l4_result.json         L4 speak-test T3 confusion rows     (BABEL_CLOSEOUT.md, d777297d1fae0e92)
#   ..\_l6_result.json         L6 dark-mass rank ladder + gaps     (L6_CLOSEOUT.md, fd71cd4f3bbfa3e3)
# Outputs: fig1..fig6 as .png (300 dpi) + .pdf in this directory.
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return json.load(f)

REGIMES = ["prose", "code", "repetition"]
BOUNDS = list(range(13))

def savefig(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(HERE, f"{stem}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("wrote", stem)

# ----------------------------------------------------------------------------------------------
# FIG 1 -- THE NAT COLLAPSE: unexplained behavioral mass (excess nats over per-cell floors) and
# open gap cells, per decoder round. Every point recomputed/read from that round's frozen verdict.
# ----------------------------------------------------------------------------------------------
def fig1():
    o6 = load("_open6_result.json"); v2 = load("_v2_result.json"); v3 = load("_v3_result.json")
    v4 = load("_v4_result.json");   v5 = load("_v5_result.json"); v6 = load("_v6_result.json")
    v7 = load("_v7_result.json")
    stages   = ["OPEN-6\n(S4)", "V2\n(S5)", "V3\n(S7)", "V4\n(S7)", "V5", "V6", "V7"]
    # legacy-meter series (the only meter until V5; permanent afterwards)
    legacy_m = [sum(r["excess_nats"] for r in o6["gap_table"]),
                sum(r["excess_nats"] for r in v2["gap_table"]),
                sum(r["excess_nats"] for r in v3["gap_table"]),
                v4["verdict"]["unexplained_nats"],
                v5["verdict"]["tables"]["legacy"]["unexplained_nats"],
                v6["verdict"]["tables"]["legacy"]["unexplained_nats"],
                v7["verdict"]["tables"]["legacy"]["unexplained_nats"]]
    legacy_c = [len(o6["gap_table"]), len(v2["gap_table"]), len(v3["gap_table"]),
                v4["verdict"]["gap_cells"],
                v5["verdict"]["tables"]["legacy"]["gap_cells"],
                v6["verdict"]["tables"]["legacy"]["gap_cells"],
                v7["verdict"]["tables"]["legacy"]["gap_cells"]]
    # recalibrated meter exists from V5 (Will-ratified primary)
    recal_x  = [4, 5, 6]
    recal_m  = [v5["verdict"]["tables"]["recal"]["unexplained_nats"],
                v6["verdict"]["tables"]["recal"]["unexplained_nats"],
                v7["verdict"]["tables"]["recal"]["unexplained_nats"]]
    recal_c  = [v5["verdict"]["tables"]["recal"]["gap_cells"],
                v6["verdict"]["tables"]["recal"]["gap_cells"],
                v7["verdict"]["tables"]["recal"]["gap_cells"]]
    x = np.arange(len(stages))
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax2 = ax.twinx()
    ax2.bar(x - 0.08, legacy_c, width=0.16, color="#cccccc", alpha=0.5, label="gap cells (legacy)")
    ax2.bar([xi + 0.08 for xi in recal_x], recal_c, width=0.16, color="#e8a49c", alpha=0.6,
            label="gap cells (recal)")
    ax2.set_ylabel("open gap cells (of 39)"); ax2.set_ylim(0, 30)
    ax.plot(x, legacy_m, "o-", color="#888888", lw=2, label="legacy meter (nats)", zorder=3)
    ax.plot(recal_x, recal_m, "s-", color="#c0392b", lw=2.5, label="recalibrated meter, primary (nats)",
            zorder=3)
    for xi, yi in zip(x, legacy_m):
        ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=8, color="#555555")
    for xi, yi in zip(recal_x, recal_m):
        ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points", xytext=(14, -13),
                    ha="center", fontsize=8, color="#c0392b")
    ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=9)
    ax.set_ylabel("unexplained mass (excess nats over floors)")
    ax.set_ylim(-0.6, 13.8); ax.set_xlim(-0.5, 6.9)
    ax.axhline(0, color="k", lw=0.6)
    ax.annotate("six NOT-YET verdicts →", (1.5, 12.6), fontsize=9, color="#444444", ha="center")
    ax.annotate("V7: OPEN-AT-GRAIN\n39/39, 0.000 nats", xy=(6, 0.0), xytext=(4.35, 1.5),
                fontsize=9, color="#c0392b", ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2))
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=8, framealpha=0.95)
    ax.set_title("The account closes: unexplained mass 11.2 → 0 nats\nacross seven pre-registered rounds",
                 fontsize=11, pad=10)
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    savefig(fig, "fig1_nat_collapse")

# ----------------------------------------------------------------------------------------------
# FIG 2 -- FINAL VERDICT HEATMAPS, BOTH METERS: per-cell substitution-KL / floor ratio at the
# decoder_v7 grain (V7 verdict tables verbatim). Ratio < 1 = inside the model's own noise floor.
# ----------------------------------------------------------------------------------------------
def fig2():
    v7 = load("_v7_result.json")
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.4), sharex=True)
    for ax, meter in zip(axes, ["recal", "legacy"]):
        cells = v7["verdict"]["tables"][meter]["cells"]
        M = np.zeros((3, 13)); P = np.zeros((3, 13), dtype=bool)
        for i, reg in enumerate(REGIMES):
            for b in BOUNDS:
                c = cells[f"{reg}_b{b}"]
                M[i, b] = c["KL"] / c["floor"]; P[i, b] = c["pass_grain"]
        im = ax.imshow(M, cmap="RdYlGn_r", vmin=0.0, vmax=2.0, aspect="auto")
        for i in range(3):
            for b in BOUNDS:
                ax.text(b, i, f"{M[i,b]:.2f}", ha="center", va="center", fontsize=7,
                        color="black" if M[i, b] < 1.35 else "white",
                        fontweight="bold" if not P[i, b] else "normal")
                if not P[i, b]:
                    ax.add_patch(plt.Rectangle((b - .5, i - .5), 1, 1, fill=False, ec="black", lw=1.8))
        n = v7["verdict"]["tables"][meter]
        ax.set_yticks(range(3)); ax.set_yticklabels(REGIMES, fontsize=9)
        tag = "recalibrated (primary)" if meter == "recal" else "legacy (permanent)"
        ax.set_title(f"{tag}: N_grain = {n['N_grain']}/39", fontsize=10, loc="left")
        fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01, label="KL / floor")
    axes[1].set_xticks(BOUNDS); axes[1].set_xticklabels([f"b{b}" for b in BOUNDS], fontsize=9)
    axes[1].set_xlabel("layer boundary (BUS[0..12])")
    fig.suptitle("Every cell priced: substitution-KL over its per-(boundary,regime) floor, decoder_v7 grain",
                 fontsize=11)
    savefig(fig, "fig2_verdict_heatmaps")

# ----------------------------------------------------------------------------------------------
# FIG 3 -- KL vs RANK: the late tail buys out gradually (V3 rank ladder, all 12 late cells) and
# asymptotes at rep_b12 (V4 extension) -- rank is the wrong axis for what remained late.
# ----------------------------------------------------------------------------------------------
def fig3():
    v3 = load("_v3_result.json"); v4 = load("_v4_result.json")
    rc = v3["rank_curve"]["cells"]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    ranks = [0, 5, 10, 15, 20]; keys = ["S4", "S_r5", "S_r10", "S_r15", "S_r20"]
    for cell, cur in sorted(rc.items()):
        ys = [cur[k] for k in keys]
        reg, b = cell.rsplit("_b", 1)
        color = {"prose": "#2c7fb8", "code": "#41ab5d", "repetition": "#c0392b"}[reg]
        axL.plot(ranks, ys, "o-", ms=3, lw=1.2, color=color, alpha=0.75)
        axL.annotate(f"{reg[:4]} b{b}", (ranks[-1], ys[-1]), textcoords="offset points",
                     xytext=(4, 0), fontsize=6.5, color=color)
    axL.set_xlabel("late-complement oracle read rank r (added dims)")
    axL.set_ylabel("substitution KL (nats)")
    axL.set_title("V3: the late tail sells out gradually (no cliff)", fontsize=10)
    axL.set_xticks(ranks); axL.set_xlim(-1, 26)
    curve = v4["armB"]["curve"]
    xs = sorted(int(k) for k in curve); ys = [curve[str(k)]["KL"] for k in xs]
    cap = [k for k in xs if curve[str(k)]["allowance_ok"]]
    axR.plot(xs, ys, "o-", color="#c0392b", lw=1.8, label="rep_b12 folded read KL")
    axR.axhline(v4["armB"]["rep_b12_vs_floor"]["floor"], color="k", ls="--", lw=1,
                label=f"legacy floor {v4['armB']['rep_b12_vs_floor']['floor']:.4f}")
    axR.axhline(0.1935, color="#c0392b", ls=":", lw=1, label="recal floor 0.1935 (V5)")
    if cap:
        axR.axvline(max(cap), color="#888888", ls="-.", lw=1,
                    label=f"unnamed-dims allowance cap (net {max(cap)})")
    axR.set_xlabel("net oracle dims (V4 Arm B extension)")
    axR.set_title("V4: rep_b12 plateaus above the legacy floor;\ncloses only under the honest recal meter (V5)",
                  fontsize=10)
    m = v4["armB"]["marginal_nat_per_dim"]
    axR.annotate(f"marginal price falls {m['m_20_32']:.4f} → {m['m_48_64']:.4f} nat/dim",
                 (0.35, 0.62), xycoords="axes fraction", fontsize=8)
    axL.legend(handles=[plt.Line2D([], [], color=c, label=r) for r, c in
                        [("prose", "#2c7fb8"), ("code", "#41ab5d"), ("repetition", "#c0392b")]],
               fontsize=8, loc="upper right")
    axR.legend(fontsize=7.5, loc="upper right")
    savefig(fig, "fig3_kl_vs_rank")

# ----------------------------------------------------------------------------------------------
# FIG 4 -- THE WALL'S STUDENT: V6 surrogate training curves (real vs shuffled-target twin) and the
# capacity-hurts falsifier (train fit vs held-out-period substitution KL, three rungs).
# ----------------------------------------------------------------------------------------------
def fig4():
    v6 = load("_v6_result.json")
    lad, cert = v6["ladder"], v6["cert"]["rungs"]
    floor = v6["config"]["floor_b5_recal"]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    colors = {"L0": "#c0392b", "L1": "#2c7fb8", "L2": "#41ab5d"}
    names = {"L0": "LINEAR 1.18M", "L1": "MLP 1.77M", "L2": "ATTN 1.78M"}
    for r in ["L0", "L1", "L2"]:
        steps = np.linspace(0, v6["config"]["steps"], len(lad[r]["loss_curve"]))
        axL.plot(steps, lad[r]["loss_curve"], "-", color=colors[r], lw=1.6, label=names[r])
        axL.plot(steps, lad[r]["twin_loss_curve"], "--", color=colors[r], lw=1.0, alpha=0.55)
    axL.set_yscale("log"); axL.set_xlabel("training step"); axL.set_ylabel("MSE loss (log)")
    axL.set_title("Training: real targets (solid) vs shuffled-target twin (dashed)", fontsize=10)
    axL.legend(fontsize=8)
    rungs = ["L0", "L1", "L2"]; xs = np.arange(3)
    sacred = [cert[r]["SACRED_kl_rep"] for r in rungs]
    within = [cert[r]["WITHIN_kl_rep"] for r in rungs]
    twin   = [cert[r]["twin_kl_rep"] for r in rungs]
    axR.bar(xs - 0.22, within, 0.2, color="#aaaaaa", label="within-seen KL (memorization)")
    axR.bar(xs, sacred, 0.2, color="#c0392b", label="held-out-period KL (SACRED)")
    axR.bar(xs + 0.22, twin, 0.2, color="#444444", label="shuffled-target twin KL")
    axR.axhline(floor, color="k", ls="--", lw=1, label=f"recal floor {floor}")
    axR.set_yscale("log")
    axR.set_xticks(xs)
    axR.set_xticklabels([f"{names[r]}\ntrain-R²={lad[r]['r2_train']:.2f}" for r in rungs], fontsize=8)
    axR.set_ylabel("substitution KL at BUS[5] (nats, log)")
    axR.set_title("The falsifier: only the student too small to memorize\ncertifies on never-seen periods",
                  fontsize=10)
    axR.legend(fontsize=7, loc="upper left")
    savefig(fig, "fig4_surrogate_falsifier")

# ----------------------------------------------------------------------------------------------
# FIG 5 -- THE SPEAK TEST CONFUSION MATRIX: antisymmetric CH-WU response of each readout (col)
# to a +/-3sigma human edit of each named axis (row), vs matched-random edit nulls (L4 T3).
# ----------------------------------------------------------------------------------------------
def fig5():
    l4 = load("_l4_result.json")
    fams = l4["T3"]["families"]; cols = l4["T3"]["readout_columns"]
    rows = ["naval", "clause", "operator", "rung"]  # display order; rung last (L5: certified read-only)
    M = np.array([[fams[r]["M_row"][c] for c in cols] for r in rows])
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    vmax = np.abs(M).max()
    im = ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            own = (c == fams[r]["own_readout"])
            ax.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=9,
                    fontweight="bold" if own else "normal")
            if own:
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False, ec="black", lw=2.0))
    labels = [f"{r}\n(null95 {fams[r]['null95']:.3g})" for r in rows]
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=9)
    ax.set_xlabel("readout (the axis's own W_U vocabulary image)")
    ax.set_ylabel("edited axis (+3σ on the English gloss, re-encoded)")
    ax.set_title("Human-edit steering: 3 of 4 named axes steer the model\nin their own vocabulary; "
                 "the executable rung is certified read-only at ±3σ and ±6σ (L5/L6)", fontsize=10)
    fig.colorbar(im, fraction=0.04, pad=0.02, label="antisymmetric CH-WU response")
    savefig(fig, "fig5_speak_confusion")

# ----------------------------------------------------------------------------------------------
# FIG 6 -- THE DARK MASS IS DIFFUSE (L6 Arm A): fraction of the 5.3% transplant gap closed by the
# top-k SVD subspace of the dark complement (prose b6), vs the greedy-8 selection and a RANDOM
# 256-dim dark slice; no k <= 256 reaches the pre-registered 0.80 localization bar. Right panel:
# the per-boundary dark gap (1 - sbar_readable) deepens with depth. All values from the frozen
# _l6_result.json (fd71cd4f3bbfa3e3) verbatim.
# ----------------------------------------------------------------------------------------------
def fig6():
    l6 = load("_l6_result.json")
    a = l6["armA"]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9),
                                   gridspec_kw={"width_ratios": [1.5, 1.0]})
    ks = sorted(int(k) for k in a["ladder"])
    closure = [a["ladder"][str(k)]["closure"] for k in ks]
    axL.plot(ks, closure, "o-", color="#c0392b", lw=1.8, label="top-k dark SVD subspace")
    gj = [s["j"] for s in a["greedy"]["steps"]]
    gc = [s["closure"] for s in a["greedy"]["steps"]]
    axL.plot(gj, gc, "s--", color="#2c7fb8", lw=1.2, ms=4,
             label=f"greedy best-{gj[-1]} directions ({gc[-1]:.3f})")
    sp = a["specificity"]
    axL.plot([sp["rank"]] * len(sp["closure_null_draws"]), sp["closure_null_draws"],
             "x", color="#888888", ms=7, mew=1.6,
             label=f"random {sp['rank']}-dim dark slice (mean {sp['closure_null_mean']:.3f})")
    axL.axhline(0.80, color="k", ls="--", lw=1,
                label="pre-registered localization bar (0.80)")
    axL.set_xscale("log", base=2)
    axL.set_xticks(ks); axL.set_xticklabels([str(k) for k in ks], fontsize=8)
    axL.set_ylim(-0.08, 1.0)
    axL.set_xlabel("dark-subspace rank k (of 329 dark dims)")
    axL.set_ylabel("fraction of transplant gap closed")
    axL.annotate("DIFFUSE: no k ≤ 256 reaches the bar;\nbest hand-picked 256 beats a random\n"
                 f"256-slice by only ~{a['ladder']['256']['closure'] - sp['closure_null_mean']:.2f}",
                 (0.04, 0.64), xycoords="axes fraction", fontsize=8.5, color="#c0392b")
    axL.set_title("L6: the 5.3% transplant remainder has no low-rank carrier", fontsize=10)
    axL.legend(fontsize=7.5, loc="center left")
    att = l6["armA"]["attribution"]
    order = ["b2", "b4", "b6_banked", "b8", "b10"]
    labels = ["b2", "b4", "b6", "b8", "b10"]
    gaps = [att[k]["dark_gap"] for k in order]
    axR.bar(np.arange(len(order)), gaps, 0.55, color="#555555")
    for i, g in enumerate(gaps):
        axR.annotate(f"{g:.3f}", (i, g), textcoords="offset points", xytext=(0, 3),
                     ha="center", fontsize=8)
    axR.set_xticks(np.arange(len(order))); axR.set_xticklabels(labels, fontsize=9)
    axR.set_xlabel("boundary")
    axR.set_ylabel("dark gap (1 − s̄, readable payload)")
    axR.set_title("The dark share deepens with depth", fontsize=10)
    fig.suptitle("The un-transplanted remainder is diffuse, high-dimensional dark signal (L6 Arm A)",
                 fontsize=11)
    savefig(fig, "fig6_dark_rank_ladder")

if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("all figures written to", HERE)

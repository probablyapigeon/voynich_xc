import math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

rng_gen = random.Random(101)

# 1. Symbolic Music Notation (from local data/music_nottingham.txt)
music_toks = Path("data/music_nottingham.txt").read_text(encoding="utf-8-sig").split()

# 2. Chemical / Apothecary Symbolic Formula Stream (compact reaction & dosage notation)
reagents = ["Herb.A", "Rad.B", "Flos.C", "Sem.D", "Gum.E", "Sal.F", "Ol.G", "Aq.H", "Vin.I", "Mel.J"]
states = ["(raw)", "(4o:prep)", "(dec)", "(inf)", "(pulv)", "(dist)"]
ops = ["+", "->", "::", "aa", "q.s.", "M.", "f.s.a."]
chem_toks = []
for _ in range(3200):
    chem_toks.extend([
        rng_gen.choice(reagents) + rng_gen.choice(states),
        rng_gen.choice(ops),
        rng_gen.choice(reagents) + rng_gen.choice(states),
        rng_gen.choice(["->"]),
        "Comp." + str(rng_gen.randint(1, 12)) + rng_gen.choice(["[II]", "[III]", "[IV]"]),
    ])

# 3. Medieval Abbreviated Sigla / Slot-Template Notation (prefix + root + suffix shorthand)
prefs = ["4o-", "o-", "1-", "2-", "8-", "y-"]
roots = ["ham", "han", "hae", "hC", "k1", "coe", "oh", "ok", "1c", "9k"]
suffs = ["-89", "-9", "-am", "-oe", "-ay", "-79"]
abbr_toks = []
for _ in range(3200):
    # Slot-locked template: [OPENER] [PREP-ROOT-SUFF] [PREP-ROOT-SUFF] [CLOSER]
    abbr_toks.extend([
        "4o-han-9",
        rng_gen.choice(["4o-", "o-"]) + rng_gen.choice(roots) + rng_gen.choice(suffs),
        rng_gen.choice(["4o-", "8-"]) + rng_gen.choice(roots) + rng_gen.choice(suffs),
        "1c-89",
    ])

voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()
cb_toks = voynich_toks[30000:36000]

CORPORA = {
    "1. Symbolic Music (ABC)": music_toks,
    "2. Apothecary Formula Not.": chem_toks,
    "3. Slot-Template Shorthand": abbr_toks,
    "4. Voynich Currier B (Target)": cb_toks,
}

def obs_vec(tokens: list[str]):
    pairs = Counter(zip(tokens, tokens[1:]))
    out = Counter(tokens[:-1])
    res = []
    for i, t in enumerate(tokens):
        c = 0.88 if t in tokens[max(0, i - 8):i] else 0.25
        s = min(0.15 + 0.85 * pairs[t, tokens[i + 1]] / out[t], 0.95) if i + 1 < len(tokens) else 0.5
        e = min(len(set(t)) / 10.0, 1.0)
        res.append((c, round(s, 3), round(e, 3)))
    return res

def run_sim(obs):
    r = PsiVector(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, T=0.5, E=0.5, d=0.5, a=0.5)
    for c_v, s_v, e_v in obs:
        tok = PsiVector(c=c_v, p=0.5, r=e_v, s=s_v, Φ=0.6, T=0.4, E=e_v, d=0.3, a=0.5)
        connect(r, tok, weight=0.25, type="sym_ctrl")
        r = Ouroboros(r, target=tok)
    return list(r.as_dict().values())

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

rng = random.Random(42)
win_z = {}
for name, toks in CORPORA.items():
    nw = min(10, len(toks) // 300)
    z_list = []
    for w in range(nw):
        chunk = toks[w * 300 : (w + 1) * 300]
        rv = run_sim(obs_vec(chunk))
        nv = [run_sim(obs_vec(rng.sample(chunk, len(chunk)))) for _ in range(30)]
        z = []
        for k in range(9):
            vals = [v[k] for v in nv]
            mu = sum(vals) / len(vals)
            sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / len(vals)) or 1e-9
            z.append((rv[k] - mu) / sd)
        z_list.append(z)
    win_z[name] = z_list

cb_mean = [sum(z[k] for z in win_z["4. Voynich Currier B (Target)"]) / len(win_z["4. Voynich Currier B (Target)"]) for k in range(9)]

md = [
    "# Step 3: Symbolic, Formulaic & Slot-Template Shorthand Control\n",
    "![Symbolic Notation Control](symbolic_notation_polarity.png)\n",
    "Tests **Hypothesis #2** (whether symbolic notation, apothecary formulas, or slot-locked morphological shorthand reproduce **Voynich Currier B's** positive $Z_\\Phi = +0.46$ procedural regime, unlike natural English recipes in Step 2 which stayed negative at $Z_\\Phi = -0.55$).\n",
    "| System | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Voynich Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== STEP 3: SYMBOLIC & FORMULA NOTATION CONTROL (Up to 10 x 300 Windows, Seed=42) ===")
print(f"{'System':30s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CB)':>8s}")
print("-" * 94)

labels, zp_m, zp_s, cb_c_list = [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    cb_c = float(np.mean([cos(z, cb_mean) for z in zl]))
    print(f"{name:30s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {cb_c:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{cb_c:+.4f}` |")
    labels.append(f"{name} (n={n})")
    zp_m.append(zpm); zp_s.append(zps); cb_c_list.append(cb_c)

Path("SYMBOLIC_NOTATION_CONTROL.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y, cb_c_list, height=0.5, color="#58a6ff", edgecolor="#79c0ff")
for i, v in enumerate(cb_c_list):
    ax1.text(v + (0.04 if v >= 0 else -0.04), i, f"{v:+.3f}", va="center",
             ha="left" if v >= 0 else "right", fontweight="bold", color="#e6edf3")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-1.05, 1.15)
ax1.set_xlabel("Mean Cosine Similarity to Voynich Currier B", color="#c9d1d9")
ax1.set_title("A. Alignment to Currier B Procedural Regime", fontweight="bold", color="#f0f6fc")

colors2 = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.5, color=colors2, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-3.2, 2.5)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Coherence Polarity Match (Positive Z_Φ)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Step 3: Symbolic, Formulaic & Slot-Template Notation vs. Currier B",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("symbolic_notation_polarity.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved SYMBOLIC_NOTATION_CONTROL.md and symbolic_notation_polarity.png")
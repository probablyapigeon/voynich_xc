import math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()
cb_toks = voynich_toks[30000:36000]

# Vocabulary pools for 4-slot apothecary ledgers
qtys = ["i", "ii", "iii", "iv", "vi", "ss", "ana", "qs", "p1", "p2"]
items = [f"herb.{chr(65+i)}{j}" for i in range(12) for j in range(1, 5)]  # 48 distinct botanical items
preps = ["raw", "contus", "coq", "infus", "dist", "calc", "lav", "subt", "clar", "misc", "filtr", "evap"]
units = ["dri", "uncii", "scriii", "lbss", "mi", "gttx", "cyath", "manip", "vas", "phial"]

# 1. Stateless Ledger (random item every 4-slot line)
rng1 = random.Random(303)
stateless_toks = []
for _ in range(1500):
    stateless_toks.extend([rng1.choice(qtys), rng1.choice(items), rng1.choice(preps), rng1.choice(units)])

# 2. Stateful Multi-Step Ledger (holds 1 active ingredient across 4-6 consecutive steps while changing prep/qty/unit)
rng2 = random.Random(606)
stateful_toks = []
while len(stateful_toks) < 6000:
    active_item = rng2.choice(items)
    n_steps = rng2.randint(4, 6)
    step_preps = rng2.sample(preps, n_steps)
    for sp in step_preps:
        stateful_toks.extend([rng2.choice(qtys), active_item, sp, rng2.choice(units)])

# 3. Stateful Rich Ledger (active ingredient + rotating co-ingredient & inflectional endings)
rng3 = random.Random(707)
endings = ["a", "ae", "am", "is", "o", "um", "us", "e"]
stateful_rich_toks = []
while len(stateful_rich_toks) < 6000:
    base_item = rng3.choice(items)
    co_item = rng3.choice(items)
    n_steps = rng3.randint(4, 6)
    step_preps = rng3.sample(preps, n_steps)
    for idx, sp in enumerate(step_preps):
        ing = base_item if idx % 2 == 0 else co_item
        inflected_ing = ing + "." + rng3.choice(endings)
        inflected_prep = sp + "." + rng3.choice(endings)
        stateful_rich_toks.extend([rng3.choice(qtys), inflected_ing, inflected_prep, rng3.choice(units)])

CANDIDATES = {
    "1. Stateless Ledger (Random)": stateless_toks[:6000],
    "2. Stateful Multi-Step Ledger": stateful_toks[:6000],
    "3. Stateful Rich + Inflected": stateful_rich_toks[:6000],
    "4. Voynich Currier B (Actual)": cb_toks,
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
        connect(r, tok, weight=0.25, type="stateful")
        r = Ouroboros(r, target=tok)
    return list(r.as_dict().values())

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

rng = random.Random(42)
win_z = {}
for name, toks in CANDIDATES.items():
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

cb_mean = [sum(z[k] for z in win_z["4. Voynich Currier B (Actual)"]) / 10.0 for k in range(9)]

md = [
    "# Stateful Multi-Step Apothecary Ledger Probe\n",
    "![Stateful Ledger vs Currier B](stateful_ledger_probe.png)\n",
    "Tests whether holding an active ingredient steady across 4–6 consecutive preparation steps (`Stateful Multi-Step Ledger`) drops bigram stiffness $Z_s$ toward **Voynich Currier B** (`10 x 300` windows, `seed=42`).\n",
    "| System | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== STATEFUL MULTI-STEP LEDGER PROBE (10 x 300 Windows, Seed=42) ===")
print(f"{'System':30s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CB)':>8s}")
print("-" * 94)

labels, zs_m, zs_s, zp_m, zp_s, cb_c_list = [], [], [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    cbc = float(np.mean([cos(z, cb_mean) for z in zl]))
    print(f"{name:30s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {cbc:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{cbc:+.4f}` |")
    labels.append(name); zs_m.append(zsm); zs_s.append(zss); zp_m.append(zpm); zp_s.append(zps); cb_c_list.append(cbc)

Path("STATEFUL_LEDGER_PROBE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 4.8), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2, ax3):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))

# Panel A: cos(Currier B)
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y, cb_c_list, height=0.5, color="#a371f7", edgecolor="#d2a8ff")
for i, v in enumerate(cb_c_list):
    ax1.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.3f}", va="center",
             ha="left" if v >= 0 else "right", fontweight="bold", color="#e6edf3")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-0.3, 0.75)
ax1.set_xlabel("cos(Currier B)", color="#c9d1d9")
ax1.set_title("A. Overall Alignment to Currier B", fontweight="bold", color="#f0f6fc")

# Panel B: Bigram Stiffness Z_s
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zs_m, xerr=zs_s, height=0.5, color="#f0883e", error_kw=dict(ecolor="#f0f6fc", elinewidth=1.1, capsize=3))
for i, (m, s) in enumerate(zip(zs_m, zs_s)):
    ax2.text(m + s + 0.15, i, f"{m:+.2f}", va="center", ha="left", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-0.5, 8.5)
ax2.set_xlabel("Transition Stiffness Z_s (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Does Stateful Memory Drop Z_s?", fontweight="bold", color="#f0f6fc")

# Panel C: Phase Coherence Z_Phi
cols3 = ["#ff7b72" if m < 0 else "#58a6ff" for m in zp_m]
ax3.axvline(0, color="#8b949e", linewidth=1.0)
ax3.barh(y, zp_m, xerr=zp_s, height=0.5, color=cols3, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.1, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax3.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax3.set_yticks(y); ax3.set_yticklabels([""] * len(labels))
ax3.invert_yaxis(); ax3.set_xlim(-2.2, 2.0)
ax3.set_xlabel("Phase Coherence Z_Φ (Mean ± SD)", color="#c9d1d9")
ax3.set_title("C. Coherence Polarity Flip (Z_Φ)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Stateful Multi-Step Apothecary Ledger vs. Voynich Currier B (10 x 300 Windows)",
             fontsize=13, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("stateful_ledger_probe.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved STATEFUL_LEDGER_PROBE.md and stateful_ledger_probe.png")
import math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()
cb_toks = voynich_toks[30000:36000]

# 1. Row 3 Baseline: Latin-Alphabet Stateful Rich + Inflected Ledger (26+ chars + dot separator)
qtys_lat = ["i", "ii", "iii", "iv", "vi", "ss", "ana", "qs", "p1", "p2"]
items_lat = [f"herb.{chr(65+i)}{j}" for i in range(12) for j in range(1, 5)]
preps_lat = ["raw", "contus", "coq", "infus", "dist", "calc", "lav", "subt", "clar", "misc", "filtr", "evap"]
units_lat = ["dri", "uncii", "scriii", "lbss", "mi", "gttx", "cyath", "manip", "vas", "phial"]
endings_lat = ["a", "ae", "am", "is", "o", "um", "us", "e"]

rng1 = random.Random(707)
latin_stateful = []
while len(latin_stateful) < 6000:
    base_item = rng1.choice(items_lat)
    co_item = rng1.choice(items_lat)
    n_steps = rng1.randint(4, 6)
    for idx, sp in enumerate(rng1.sample(preps_lat, n_steps)):
        ing = (base_item if idx % 2 == 0 else co_item) + "." + rng1.choice(endings_lat)
        prp = sp + "." + rng1.choice(endings_lat)
        latin_stateful.extend([rng1.choice(qtys_lat), ing, prp, rng1.choice(units_lat)])

# 2. Compact-Glyph Stateful Ledger (mapped onto Voynich's 14-glyph core inventory: o,e,8,9,y,a,m,c,h,k,1,4,s,n)
# Every token reuses the same small glyph set while rotating prefixes/stems/endings
qtys_cmp = ["1o", "2o", "8o", "9o", "1c", "2c", "8c", "9c", "oe", "oy"]
# 48 compact 2-3 glyph stems built strictly from {o,e,8,9,y,a,m,c,h,k,1,4,s,n}
cores = ["oh", "ok", "ch", "sh", "hc", "kc", "am", "an", "oe", "oy", "8o", "9o", "1c", "4o", "mc", "nc"]
mids = ["a", "e", "o", "8", "9", "c"]
items_cmp = [c + m for c in cores for m in mids[:3]]  # 48 distinct compact stems
preps_cmp = ["han", "ham", "hae", "hc8", "k1c", "coe", "1ch", "9kc", "oha", "oka", "8am", "9am"]
units_cmp = ["1c89", "4o89", "o89", "c89", "89", "am9", "oe9", "ay9", "an9", "99"]
prefs_cmp = ["4o", "o", "1", "2", "8", "y"]
suffs_cmp = ["89", "9", "am", "an", "oe", "ay", "y", "e"]

rng2 = random.Random(808)
compact_stateful = []
while len(compact_stateful) < 6000:
    base_item = rng2.choice(items_cmp)
    co_item = rng2.choice(items_cmp)
    n_steps = rng2.randint(4, 6)
    for idx, sp in enumerate(rng2.sample(preps_cmp, n_steps)):
        stem = base_item if idx % 2 == 0 else co_item
        ing = rng2.choice(["4o", "o", ""]) + stem + rng2.choice(suffs_cmp)
        prp = rng2.choice(["4o", "8", ""]) + sp + rng2.choice(["9", "am", "oe", ""])
        compact_stateful.extend([rng2.choice(qtys_cmp), ing, prp, rng2.choice(units_cmp)])

# 3. Ultra-Compact High-Reuse Variant (maximizes intra-word glyph repetition like 'oeeo', '8989', 'chch')
rng3 = random.Random(909)
ultracompact_stateful = []
while len(ultracompact_stateful) < 6000:
    base_item = rng3.choice(items_cmp)
    co_item = rng3.choice(items_cmp)
    n_steps = rng3.randint(4, 6)
    for idx, sp in enumerate(rng3.sample(preps_cmp, n_steps)):
        stem = base_item if idx % 2 == 0 else co_item
        # Mirror/echo a glyph from the stem inside the affix to keep unique-char count (E) low
        echo = stem[0]
        ing = echo + "o" + stem + echo + "9"
        prp = "4o" + sp + "o9"
        ultracompact_stateful.extend([rng3.choice(qtys_cmp), ing, prp, rng3.choice(units_cmp)])

CANDIDATES = {
    "1. Latin Stateful Ledger (Row 3)": latin_stateful[:6000],
    "2. Compact-Glyph Ledger (14-Char)": compact_stateful[:6000],
    "3. Echo-Compact Ledger (Low-E)": ultracompact_stateful[:6000],
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
        connect(r, tok, weight=0.25, type="cmp_led")
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
    "# Compact-Alphabet Stateful Ledger Probe\n",
    "![Compact Ledger Polarity Flip](compact_ledger_probe.png)\n",
    "Tests whether compressing the **Stateful Inflected Ledger** onto Voynich's 14-glyph core inventory (`{o, e, 8, 9, y, a, m, c, h, k, 1, 4, s, n}`) flips $Z_\\Phi$ positive (`10 x 300` windows, `seed=42`).\n",
    "| System | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== COMPACT-GLYPH STATEFUL LEDGER PROBE (10 x 300 Windows, Seed=42) ===")
print(f"{'System':33s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CB)':>8s}")
print("-" * 97)

labels, zp_m, zp_s, cb_c_list = [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    cbc = float(np.mean([cos(z, cb_mean) for z in zl]))
    print(f"{name:33s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {cbc:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{cbc:+.4f}` |")
    labels.append(name); zp_m.append(zpm); zp_s.append(zps); cb_c_list.append(cbc)

Path("COMPACT_LEDGER_PROBE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 4.8), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y, cb_c_list, height=0.5, color="#3fb950", edgecolor="#56d364")
for i, v in enumerate(cb_c_list):
    ax1.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.3f}", va="center",
             ha="left" if v >= 0 else "right", fontweight="bold", color="#e6edf3")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-0.3, 0.85)
ax1.set_xlabel("Mean Cosine Similarity to Actual Currier B", color="#c9d1d9")
ax1.set_title("A. Alignment to Currier B", fontweight="bold", color="#f0f6fc")

cols2 = ["#ff7b72" if m < 0 else "#58a6ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.5, color=cols2, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.1, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-2.2, 2.0)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Does Compact Glyph Inventory Flip Z_Φ Positive?", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Compact-Glyph Stateful Ledger vs. Voynich Currier B (10 x 300 Windows)",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("compact_ledger_probe.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved COMPACT_LEDGER_PROBE.md and compact_ledger_probe.png")
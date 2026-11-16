import re, math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

def load_clean_pg(path_str: str, marker: str, max_chars: int = 80000) -> list[str]:
    raw = Path(path_str).read_text(encoding="utf-8", errors="replace")
    idx = raw.find(marker)
    if idx != -1:
        raw = raw[idx:]
    end_idx = raw.find("*** END OF THE PROJECT GUTENBERG")
    if end_idx != -1:
        raw = raw[:end_idx]
    cleaned = re.sub(r"[^A-Za-z0-9\s]", " ", raw[:max_chars]).lower()
    return [w for w in cleaned.split() if len(w) >= 2]

herbal_prose = load_clean_pg("data/culpeper_herbal.txt", "AMARA DULCIS")
recipe_prose = load_clean_pg("data/forme_of_cury.txt", "FOR TO MAKE")

voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()
ca_toks = voynich_toks[:6000]
cb_toks = voynich_toks[30000:36000]

CORPORA = {
    "1. Historical Herbal (Desc.)": herbal_prose,
    "2. 14th-C. Recipes (Proc.)": recipe_prose,
    "3. Voynich Currier A (Herbal)": ca_toks,
    "4. Voynich Currier B (Recipe)": cb_toks,
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
        connect(r, tok, weight=0.25, type="dual_reg")
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

ca_mean = [sum(z[k] for z in win_z["3. Voynich Currier A (Herbal)"]) / len(win_z["3. Voynich Currier A (Herbal)"]) for k in range(9)]
cb_mean = [sum(z[k] for z in win_z["4. Voynich Currier B (Recipe)"]) / len(win_z["4. Voynich Currier B (Recipe)"]) for k in range(9)]

md = [
    "# Step 2: Single-Source Dual-Register Control (Historical Herbal vs. 14th-Century Recipes)\n",
    "![Dual-Register Polarity Control](dual_register_polarity.png)\n",
    "Tests whether authentic historical **descriptive herbal entries** (*Culpeper's Complete Herbal*, PG #49513) vs. **procedural compounding recipes** (*The Forme of Cury*, c. 1390, PG #8102) reproduce the same $Z_\\Phi$ polarity flip seen between **Voynich Currier A** and **Voynich Currier B** across **10 non-overlapping 300-token windows** (`30` Monte Carlo shuffles/window, `seed=42`).\n",
    "| Corpus | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== STEP 2: HISTORICAL DUAL-REGISTER CONTROL (10 x 300 Windows, Seed=42) ===")
print(f"{'Corpus':30s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CA)':>8s} | {'cos(CB)':>8s}")
print("-" * 104)

labels, zp_m, zp_s, ca_c_list, cb_c_list = [], [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    ca_c = float(np.mean([cos(z, ca_mean) for z in zl]))
    cb_c = float(np.mean([cos(z, cb_mean) for z in zl]))
    print(f"{name:30s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {ca_c:+8.4f} | {cb_c:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{ca_c:+.4f}` | `{cb_c:+.4f}` |")
    labels.append(f"{name} (n={n})")
    zp_m.append(zpm); zp_s.append(zps)
    ca_c_list.append(ca_c); cb_c_list.append(cb_c)

Path("DUAL_REGISTER_CONTROL.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 4.8), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
h = 0.35
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y - h/2, ca_c_list, height=h, color="#3fb950", label="cos(Voynich Currier A)")
ax1.barh(y + h/2, cb_c_list, height=h, color="#58a6ff", label="cos(Voynich Currier B)")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-0.85, 0.85)
ax1.set_xlabel("Mean Cosine Similarity to Voynich Dialect Centroid", color="#c9d1d9")
ax1.set_title("A. Register Alignment vs. Voynich Dialects", fontweight="bold", color="#f0f6fc")
ax1.legend(loc="lower left", frameon=True, facecolor="#0d1117", edgecolor="#30363d", fontsize=9)

colors2 = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.5, color=colors2, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-3.2, 2.5)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Coherence Polarity Flip (Descriptive vs. Recipe)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Step 2: Historical Herbal Description vs. 14th-Century Recipes (10 x 300 Windows)",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("dual_register_polarity.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved DUAL_REGISTER_CONTROL.md and dual_register_polarity.png")
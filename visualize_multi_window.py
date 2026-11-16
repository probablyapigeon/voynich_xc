import math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

SOURCES = {
    "DNA (Human HBB)": ("dna_hbb.txt", 0),
    "Music (Norbeck ABC)": ("music_nottingham.txt", 0),
    "Runtime Opcodes": ("malware_api.txt", 0),
    "AI Prose (Live LLM)": ("ai_ollama.txt", 0),
    "Human Prose (1818)": ("human_frankenstein.txt", 0),
    "Voynich Currier A": ("voynich_clean.txt", 0),
    "Voynich Currier B": ("voynich_clean.txt", 30000),
    "Bengalese Finch": ("birds.npz", 0),
}

def load_tokens(path: Path) -> list[str]:
    if path.suffix != ".npz":
        return path.read_text(encoding="utf-8-sig").split()
    with np.load(path, allow_pickle=False) as archive:
        labels = archive["syllable_types"]
        return [str(int(v)) if float(v).is_integer() else str(float(v)) for v in labels]

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
        connect(r, tok, weight=0.25, type="mw")
        r = Ouroboros(r, target=tok)
    return list(r.as_dict().values())

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

rng = random.Random(42)
win_z = {}
for dom, (fn, offset) in SOURCES.items():
    toks = load_tokens(Path("data") / fn)[offset:]
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
    win_z[dom] = z_list

ca_mean = [sum(z[k] for z in win_z["Voynich Currier A"]) / len(win_z["Voynich Currier A"]) for k in range(9)]
cb_mean = [sum(z[k] for z in win_z["Voynich Currier B"]) / len(win_z["Voynich Currier B"]) for k in range(9)]

domains = list(win_z.keys())
y_pos = np.arange(len(domains))

ca_means, ca_sds, cb_means, cb_sds = [], [], [], []
zp_means, zp_sds, counts = [], [], []

for dom in domains:
    zl = win_z[dom]
    n = len(zl)
    counts.append(n)
    ca_vals = [cos(z, ca_mean) for z in zl]
    cb_vals = [cos(z, cb_mean) for z in zl]
    zp_vals = [z[4] for z in zl]
    ca_means.append(np.mean(ca_vals)); ca_sds.append(np.std(ca_vals))
    cb_means.append(np.mean(cb_vals)); cb_sds.append(np.std(cb_vals))
    zp_means.append(np.mean(zp_vals)); zp_sds.append(np.std(zp_vals))

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=220, gridspec_kw={"width_ratios": [1.35, 1.0]})
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#484f58")
    ax.spines["bottom"].set_color("#484f58")

# Panel A: Cosine Similarity to Currier A vs. Currier B (Mean +/- SD)
h = 0.36
ax1.axvline(0, color="#8b949e", linewidth=1.0, alpha=0.8)
ax1.barh(y_pos - h/2, ca_means, xerr=ca_sds, height=h, color="#3fb950", edgecolor="#56d364",
         error_kw=dict(ecolor="#aff5b4", elinewidth=1.2, capsize=3), label="cos(Currier A)  [Expressive / Herbal]")
ax1.barh(y_pos + h/2, cb_means, xerr=cb_sds, height=h, color="#58a6ff", edgecolor="#79c0ff",
         error_kw=dict(ecolor="#cae8ff", elinewidth=1.2, capsize=3), label="cos(Currier B)  [Procedural / Recipes]")

labels_with_n = [f"{d} (n={n})" for d, n in zip(domains, counts)]
ax1.set_yticks(y_pos)
ax1.set_yticklabels(labels_with_n, fontsize=10, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis()
ax1.set_xlim(-1.05, 1.15)
ax1.set_xlabel("Cosine Similarity to Voynich Dialect Centroid (Mean ± SD)", fontsize=10.5, color="#c9d1d9")
ax1.set_title("A. Multi-Window Dialect Alignment (cos θ)", fontsize=12, fontweight="bold", color="#f0f6fc", pad=12)
ax1.legend(loc="lower left", frameon=True, facecolor="#0d1117", edgecolor="#30363d", fontsize=9)

# Panel B: Phase Coherence Polarity (Z_Phi Mean +/- SD)
bar_colors = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_means]
ax2.axvline(0, color="#8b949e", linewidth=1.0, alpha=0.8)
ax2.barh(y_pos, zp_means, xerr=zp_sds, height=0.55, color=bar_colors,
         error_kw=dict(ecolor="#e6edf3", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_means, zp_sds)):
    offset_x = 0.12 if m >= 0 else -0.12
    ha = "left" if m >= 0 else "right"
    ax2.text(m + (s if m >= 0 else -s) + offset_x, i, f"{m:+.2f}", va="center", ha=ha, fontsize=9, color="#e6edf3", fontweight="bold")

ax2.set_yticks(y_pos)
ax2.set_yticklabels([""] * len(domains))
ax2.invert_yaxis()
ax2.set_xlim(-3.2, 2.8)
ax2.set_xlabel("Phase Coherence Z-Score  Z_Φ (Mean ± SD)", fontsize=10.5, color="#c9d1d9")
ax2.set_title("B. Coherence Polarity Split (Z_Φ)", fontsize=12, fontweight="bold", color="#f0f6fc", pad=12)

fig.suptitle("XEMBRA (.xc) Multi-Window Cross-Domain Stability & Currier A/B Split (300-Token Windows, Seed=42)",
             fontsize=13.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("multi_window_isomorphism.png", dpi=220, facecolor=fig.get_facecolor())
print("Saved multi_window_isomorphism.png")
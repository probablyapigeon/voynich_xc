import re, math, random, hashlib
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

def window_rng(base_seed: int, domain: str, win_idx: int) -> random.Random:
    digest = hashlib.sha256(f"{base_seed}:{domain}:{win_idx}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))

def extract_words(path_str: str, marker: str, length: int = 120000) -> list[str]:
    raw = Path(path_str).read_text(encoding="utf-8", errors="replace")
    pos = raw.lower().find(marker.lower())
    start = pos if pos != -1 else min(5000, len(raw) // 4)
    chunk = raw[start : start + length]
    return [w for w in re.sub(r"[^A-Za-z0-9\s]", " ", chunk).lower().split() if len(w) >= 2]

# Read-only corpus loading (zero writes to data/)
frank_toks = Path("data/human_frankenstein.txt").read_text(encoding="utf-8-sig").split()
herbal_toks = extract_words("data/culpeper_herbal.txt", "amara dulcis")
ai_seed_toks = Path("data/ai_ollama.txt").read_text(encoding="utf-8-sig").split()
voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()

# Build deterministic trigram autoregressive continuation from pure Frankenstein prose
trans = defaultdict(list)
for a, b, c in zip(frank_toks[:6000], frank_toks[1:6001], frank_toks[2:6002]):
    trans[(a, b)].append(c)

rng_ar = random.Random(77)
ar_toks = list(ai_seed_toks)
w0, w1 = frank_toks[10], frank_toks[11]
while len(ar_toks) < 6200:
    cands = trans.get((w0, w1))
    nxt = rng_ar.choice(cands) if cands else rng_ar.choice(frank_toks[:500])
    ar_toks.append(nxt)
    w0, w1 = w1, nxt

CORPORA = {
    "1. Human Literary Prose (n=20)": frank_toks[:6000],
    "2. Human Herbal Prose (n=20)": herbal_toks[:6000],
    "3. Live AI + Autoreg. (n=20)": ar_toks[:6000],
    "4. Voynich Currier A (n=20)": voynich_toks[:6000],
    "5. Voynich Currier B (n=20)": voynich_toks[30000:36000],
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
        connect(r, tok, weight=0.25, type="step4")
        r = Ouroboros(r, target=tok)
    return list(r.as_dict().values())

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

win_z = {}
for name, toks in CORPORA.items():
    nw = min(20, len(toks) // 300)
    z_list = []
    for w in range(nw):
        rng = window_rng(42, name, w)
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

hum_mean = [sum(z[k] for z in win_z["1. Human Literary Prose (n=20)"]) / 20.0 for k in range(9)]

md = [
    "# Step 4: 20-Window Human Prose vs. Autoregressive AI & Voynich Polarity Benchmark\n",
    "![Human vs AI 20-Window Polarity](human_vs_llm_polarity.png)\n",
    "Evaluates **20 independent non-overlapping 300-token windows per corpus** (`100` real windows + `3,000` Monte Carlo shuffle controls = `3,100` `Ouroboros` runs, per-window isolated SHA-256 seeds from `seed=42`).\n",
    "| Corpus | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Human Prose)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== STEP 4: 20-WINDOW HUMAN VS AUTOREGRESSIVE & VOYNICH BENCHMARK (3,100 Runs) ===")
print(f"{'Corpus':30s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(Hum)':>8s}")
print("-" * 94)

labels, zp_m, zp_s, hum_c_list = [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    hc = float(np.mean([cos(z, hum_mean) for z in zl]))
    print(f"{name:30s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {hc:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{hc:+.4f}` |")
    labels.append(name)
    zp_m.append(zpm); zp_s.append(zps); hum_c_list.append(hc)

Path("HUMAN_VS_LLM_BENCHMARK.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.8, 5.2), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y, hum_c_list, height=0.5, color="#3fb950", edgecolor="#56d364")
for i, v in enumerate(hum_c_list):
    ax1.text(v + (0.04 if v >= 0 else -0.04), i, f"{v:+.3f}", va="center",
             ha="left" if v >= 0 else "right", fontweight="bold", color="#e6edf3")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-0.85, 1.15)
ax1.set_xlabel("Mean Cosine Similarity to Human Prose", color="#c9d1d9")
ax1.set_title("A. Structural Proximity to Authentic Human Prose", fontweight="bold", color="#f0f6fc")

colors2 = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.5, color=colors2, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-3.5, 2.5)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD across 20 Windows)", color="#c9d1d9")
ax2.set_title("B. 20-Window Coherence Polarity (Z_Φ)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Step 4: 20-Window Human Prose vs. Autoregressive AI & Voynich Polarity (3,100 Runs)",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("human_vs_llm_polarity.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved HUMAN_VS_LLM_BENCHMARK.md and human_vs_llm_polarity.png")
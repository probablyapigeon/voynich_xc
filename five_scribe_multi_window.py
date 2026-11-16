import re, math, random
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros
import scribe_map

def get_scribe(folio_str: str) -> str:
    for fn_name in ("get_scribe", "folio_to_scribe", "assign_scribe", "scribe_for_folio"):
        fn = getattr(scribe_map, fn_name, None)
        if callable(fn):
            res = fn(folio_str)
            if res:
                return str(res)
    for attr in ("SCRIBE_MAP", "FOLIO_SCRIBES", "SCRIBES"):
        mp = getattr(scribe_map, attr, None)
        if isinstance(mp, dict) and folio_str in mp:
            return str(mp[folio_str])
    return "Unassigned"

raw_lines = Path("data/voynich_raw.txt").read_text(encoding="utf-8", errors="replace").splitlines()
TAG_RE = re.compile(r"<[^>]+>|\[[^\]]+\]|\{[^\}]+\}|[!*,=\-\.\+\?()]")

scribe_tokens = defaultdict(list)
for ln in raw_lines:
    s = ln.strip()
    if not s or s.startswith("#"):
        continue
    m = re.match(r"<(\d+[rv])", s)
    if not m:
        continue
    folio = m.group(1)
    sc = get_scribe(folio)
    if not sc or sc == "Unassigned":
        continue
    if not sc.lower().startswith("scribe"):
        sc = f"Scribe {sc}"
    cleaned = TAG_RE.sub(" ", s)
    toks = [t for t in cleaned.split() if not re.match(r"^\d+[rv]", t)]
    scribe_tokens[sc].extend(toks)

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
        connect(r, tok, weight=0.25, type="scribe_mw")
        r = Ouroboros(r, target=tok)
    return list(r.as_dict().values())

def cos(a, b):
    d = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0

rng = random.Random(42)
scribes_sorted = sorted(scribe_tokens.keys())
scribe_win_z = {}

for sc in scribes_sorted:
    toks = scribe_tokens[sc]
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
    if z_list:
        scribe_win_z[sc] = z_list

s1_mean = [sum(z[k] for z in scribe_win_z.get("Scribe 1", [])) / max(1, len(scribe_win_z.get("Scribe 1", []))) for k in range(9)]
s2_mean = [sum(z[k] for z in scribe_win_z.get("Scribe 2", [])) / max(1, len(scribe_win_z.get("Scribe 2", []))) for k in range(9)]

md = [
    "# Five-Scribe Multi-Window Variance & Polarity Benchmark\n",
    "![Five-Scribe Multi-Window Stability](five_scribe_stability.png)\n",
    "Evaluates up to **10 non-overlapping 300-token windows per paleographic scribe** (`30` Monte Carlo shuffles per window, `seed=42`) to test whether within-scribe variance tightens relative to mixed byte-offset slicing (`±0.50`–`±0.60`).\n",
    "| Scribe | Total Toks | Wins | Self-Cosine (`Mean ± SD`) | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Scribe 1)` | `cos(Scribe 2)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== FIVE-SCRIBE MULTI-WINDOW VARIANCE TEST (Up to 10 x 300 Windows, Seed=42) ===")
print(f"{'Scribe':10s} | {'Toks':>6s} | {'W':>2s} | {'Self-Cos(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(S1)':>8s} | {'cos(S2)':>8s}")
print("-" * 82)

labels, self_m, self_s, zp_m, zp_s = [], [], [], [], []
for sc, zl in scribe_win_z.items():
    n = len(zl)
    sc_mean = [sum(z[k] for z in zl) / n for k in range(9)]
    sc_cos = [cos(z, sc_mean) for z in zl]
    cm, cs = float(np.mean(sc_cos)), float(np.std(sc_cos))
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0)
    zsm, zss = st(3)
    zpm, zps = st(4)
    c1 = float(np.mean([cos(z, s1_mean) for z in zl]))
    c2 = float(np.mean([cos(z, s2_mean) for z in zl]))
    tot_t = len(scribe_tokens[sc])
    print(f"{sc:10s} | {tot_t:6d} | {n:2d} | {cm:+6.3f}({cs:.3f}) | {zpm:+6.2f}({zps:5.2f}) | {c1:+8.4f} | {c2:+8.4f}")
    md.append(f"| **{sc}** | `{tot_t}` | `{n}` | `{cm:+.3f} ± {cs:.3f}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{c1:+.4f}` | `{c2:+.4f}` |")
    labels.append(f"{sc} (n={n})")
    self_m.append(cm); self_s.append(cs)
    zp_m.append(zpm); zp_s.append(zps)

Path("FIVE_SCRIBE_MULTI_WINDOW.md").write_text("\n".join(md) + "\n", encoding="utf-8")

# Render dual-panel figure
plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
ax1.axvline(0.50, color="#f85149", linestyle=":", linewidth=1.2, label="Unpartitioned Mixed Baseline (~0.18–0.48)")
ax1.barh(y, self_m, xerr=self_s, height=0.5, color="#a371f7", edgecolor="#d2a8ff",
         error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(0, 1.15)
ax1.set_xlabel("Within-Scribe Centroid Cosine (Mean ± SD)", color="#c9d1d9")
ax1.set_title("A. Within-Scribe Consistency (Error Bar Tightening)", fontweight="bold", color="#f0f6fc")

colors2 = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.5, color=colors2,
         error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-3.0, 2.5)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Coherence Polarity by Paleographic Hand (Z_Φ)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Five-Scribe Multi-Window Variance & Coherence Polarity (300-Token Windows, Seed=42)",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("five_scribe_stability.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved FIVE_SCRIBE_MULTI_WINDOW.md and five_scribe_stability.png")
import math, random
from collections import Counter
from pathlib import Path
import numpy as np
from xembra_core import PsiVector, connect, Ouroboros

SOURCES = {
    "1_DNA_Human_HBB": ("dna_hbb.txt", 0),
    "2_Music_Norbeck_ABC": ("music_nottingham.txt", 0),
    "3_Runtime_Opcodes": ("malware_api.txt", 0),
    "4_AI_Prose_Live_LLM": ("ai_ollama.txt", 0),
    "5_Human_Frankenstein": ("human_frankenstein.txt", 0),
    "6A_Voynich_Currier_A": ("voynich_clean.txt", 0),
    "6B_Voynich_Currier_B": ("voynich_clean.txt", 30000),
    "7_Bengalese_Finch": ("birds.npz", 0),
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

ca_mean = [sum(z[k] for z in win_z["6A_Voynich_Currier_A"]) / len(win_z["6A_Voynich_Currier_A"]) for k in range(9)]
cb_mean = [sum(z[k] for z in win_z["6B_Voynich_Currier_B"]) / len(win_z["6B_Voynich_Currier_B"]) for k in range(9)]

md = [
    "# Multi-Window Cross-Domain Stability Benchmark (Split Currier A & Currier B)\n",
    "Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`), separating **Currier A (`offset=0`)** from **Currier B (`offset=30000`)**.\n",
    "| Domain | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
]

print(f"{'Domain':22s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CA)':>8s} | {'cos(CB)':>8s}")
print("-" * 96)
for dom, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (sum(z[idx] for z in zl)/n, math.sqrt(sum((z[idx] - sum(z[idx] for z in zl)/n)**2 for z in zl)/n))
    zc_m, zc_s = st(0)
    zs_m, zs_s = st(3)
    zp_m, zp_s = st(4)
    ca_c = sum(cos(z, ca_mean) for z in zl) / n
    cb_c = sum(cos(z, cb_mean) for z in zl) / n
    print(f"{dom:22s} | {n:2d} | {zc_m:+6.2f}({zc_s:4.2f}) | {zs_m:+6.2f}({zs_s:4.2f}) | {zp_m:+6.2f}({zp_s:5.2f}) | {ca_c:+8.4f} | {cb_c:+8.4f}")
    md.append(f"| **{dom}** | `{n}` | `{zc_m:+.2f} ± {zc_s:.2f}` | `{zs_m:+.2f} ± {zs_s:.2f}` | `{zp_m:+.2f} ± {zp_s:.2f}` | `{ca_c:+.4f}` | `{cb_c:+.4f}` |")

Path("MULTI_WINDOW_ISOMORPHISM.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("\nSaved MULTI_WINDOW_ISOMORPHISM.md")
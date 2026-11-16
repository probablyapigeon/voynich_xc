import math, random
from collections import Counter
from pathlib import Path
import numpy as np
from xembra_core import PsiVector, connect, Ouroboros

SOURCES = {
    "1_DNA_Human_HBB": "dna_hbb.txt",
    "2_Music_Norbeck_ABC": "music_nottingham.txt",
    "3_Runtime_Opcodes": "malware_api.txt",
    "4_AI_Prose_Live_LLM": "ai_ollama.txt",
    "5_Human_Frankenstein": "human_frankenstein.txt",
    "6_Voynich_MS408": "voynich_clean.txt",
    "7_Bengalese_Finch": "birds.npz",
}

def load_tokens(path: Path) -> list[str]:
    if path.suffix != ".npz":
        return path.read_text(encoding="utf-8-sig").split()
    with np.load(path, allow_pickle=False) as archive:
        labels = archive["syllable_types"]
        return [str(int(v)) if float(v).is_integer() else str(float(v)) for v in labels]

def observations(tokens: list[str]) -> list[tuple[float, float, float]]:
    pairs = Counter(zip(tokens, tokens[1:]))
    outgoing = Counter(tokens[:-1])
    res = []
    for i, tok in enumerate(tokens):
        c = 0.88 if tok in tokens[max(0, i - 8):i] else 0.25
        s = min(0.15 + 0.85 * pairs[tok, tokens[i + 1]] / outgoing[tok], 0.95) if i + 1 < len(tokens) else 0.5
        e = min(len(set(tok)) / 10.0, 1.0)
        res.append((c, round(s, 3), round(e, 3)))
    return res

def run_ouroboros(obs):
    reader = PsiVector(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, T=0.5, E=0.5, d=0.5, a=0.5)
    for c_val, s_val, e_val in obs:
        tok = PsiVector(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, T=0.4, E=e_val, d=0.3, a=0.5)
        connect(reader, tok, weight=0.25, type="multi_window")
        reader = Ouroboros(reader, target=tok)
    return list(reader.as_dict().values())

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

data_dir = Path("data")
W_LEN = 300
N_NULLS = 30
rng = random.Random(42)

domain_win_z = {}
domain_counts = {}

for domain, fname in SOURCES.items():
    toks = load_tokens(data_dir / fname)
    n_win = min(10, len(toks) // W_LEN)
    domain_counts[domain] = n_win
    z_list = []
    for w_idx in range(n_win):
        win = toks[w_idx * W_LEN : (w_idx + 1) * W_LEN]
        rvec = run_ouroboros(observations(win))
        nvecs = []
        for _ in range(N_NULLS):
            shuf = win.copy()
            rng.shuffle(shuf)
            nvecs.append(run_ouroboros(observations(shuf)))
        z = []
        for k in range(9):
            vals = [v[k] for v in nvecs]
            mu = sum(vals) / len(vals)
            sd = math.sqrt(sum((x - mu) ** 2 for x in vals) / len(vals)) or 1e-9
            z.append((rvec[k] - mu) / sd)
        z_list.append(z)
    domain_win_z[domain] = z_list

v_z_list = domain_win_z["6_Voynich_MS408"]
v_mean_z = [sum(z[k] for z in v_z_list) / len(v_z_list) for k in range(9)]

print(f"\n=== MULTI-WINDOW STABILITY BENCHMARK (Up to 10 x 300-Token Windows/Domain, Seed=42) ===")
print(f"{'Domain':24s} | {'Wins':>4s} | {'Mean Zc (SD)':>15s} | {'Mean Zs (SD)':>15s} | {'Mean ZPhi (SD)':>15s} | {'cos(Voynich) Mean (SD)'}")
print("-" * 105)

md = [
    "# Multi-Window Cross-Domain Structural Stability Benchmark\n",
    "Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`) to measure across-corpus variance and confidence intervals.\n",
    "| Domain | Windows | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | Cosine to Voynich (`Mean ± SD`) |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

for domain, z_list in domain_win_z.items():
    n = len(z_list)
    def ms(idx):
        arr = [z[idx] for z in z_list]
        mu = sum(arr) / n
        sd = math.sqrt(sum((x - mu) ** 2 for x in arr) / n)
        return mu, sd
    zc_m, zc_s = ms(0)
    zs_m, zs_s = ms(3)
    zp_m, zp_s = ms(4)
    cos_vals = [cosine(z, v_mean_z) for z in z_list]
    cm = sum(cos_vals) / n
    cs = math.sqrt(sum((x - cm) ** 2 for x in cos_vals) / n)
    print(f"{domain:24s} | {n:4d} | {zc_m:+6.2f} ({zc_s:4.2f}) | {zs_m:+6.2f} ({zs_s:4.2f}) | {zp_m:+6.2f} ({zp_s:4.2f}) | {cm:+7.4f} ({cs:.4f})")
    md.append(f"| **{domain}** | `{n}` | `{zc_m:+.2f} ± {zc_s:.2f}` | `{zs_m:+.2f} ± {zs_s:.2f}` | `{zp_m:+.2f} ± {zp_s:.2f}` | `{cm:+.4f} ± {cs:.4f}` |")

with open("MULTI_WINDOW_ISOMORPHISM.md", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(md) + "\n")
print("\nSaved MULTI_WINDOW_ISOMORPHISM.md")
import re, math, random
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, Ouroboros

voynich_toks = Path("data/voynich_clean.txt").read_text(encoding="utf-8-sig").split()
cb_toks = voynich_toks[30000:36000]

cury_raw = Path("data/forme_of_cury.txt").read_text(encoding="utf-8", errors="replace")
pos = max(0, cury_raw.lower().find("for to make"))
base_words = [w for w in re.sub(r"[^a-z\s]", " ", cury_raw[pos:pos+120000].lower()).split() if len(w) >= 2]

def to_abjad(word: str) -> str:
    cons = re.sub(r"[aeiouy]", "", word.lower())
    return cons if len(cons) >= 2 else word.lower()[:2]

# 1. Vowel-Dropped Abjad Shorthand
abjad_toks = [to_abjad(w) for w in base_words[:6000]]

# 2. Apothecary Ledger (4-Slot: Qty + Item + Prep + Unit)
rng_l = random.Random(303)
qtys = ["i", "ii", "iii", "iv", "vi", "ss", "ana", "qs"]
items = ["radgent", "folsalv", "flosros", "semaneth", "gumarab", "ololiv", "aqros", "meldisp", "pulvcin", "cortgran", "herbrut", "semfen"]
preps = ["coq", "inf", "pulv", "dist", "calc", "lav", "subt", "clar", "ter", "misc"]
units = ["dri", "uncii", "scriii", "lbss", "mi", "gttx", "cyath", "manip"]
ledger_toks = []
for _ in range(1500):
    ledger_toks.extend([rng_l.choice(qtys), rng_l.choice(items), rng_l.choice(preps), rng_l.choice(units)])

# 3. Combined: Apothecary Ledger + Vowel-Dropped Abjad
rng_c1 = random.Random(404)
ledger_abjad_toks = []
for _ in range(1500):
    ledger_abjad_toks.extend([
        to_abjad(rng_c1.choice(qtys)),
        to_abjad(rng_c1.choice(items)),
        to_abjad(rng_c1.choice(preps)),
        to_abjad(rng_c1.choice(units)),
    ])

# 4. Combined + Affix State Tags (4o- / o- / -89 / -am on Abjad Ledger)
rng_c2 = random.Random(505)
ledger_abjad_affix_toks = []
for _ in range(1500):
    q = rng_c2.choice(["1", "2", "8", "o"]) + to_abjad(rng_c2.choice(qtys))
    it = rng_c2.choice(["4o", "o"]) + to_abjad(rng_c2.choice(items)) + rng_c2.choice(["9", "am", "oe"])
    pr = "4o" + to_abjad(rng_c2.choice(preps)) + rng_c2.choice(["9", "an"])
    un = to_abjad(rng_c2.choice(units)) + "89"
    ledger_abjad_affix_toks.extend([q, it, pr, un])

# 5. Currier B Affix-Stripped Stems
PREFS = ("4o", "o", "y", "1", "2", "8", "9")
SUFFS = ("89", "79", "am", "an", "oe", "ay", "9", "y")
cb_stems = []
for w in cb_toks:
    s = w
    for p in PREFS:
        if s.startswith(p) and len(s) > len(p) + 1:
            s = s[len(p):]
            break
    for sf in SUFFS:
        if s.endswith(sf) and len(s) > len(sf) + 1:
            s = s[:-len(sf)]
            break
    cb_stems.append(s)

CANDIDATES = {
    "1. Vowel-Dropped Abjad": abjad_toks,
    "2. Apothecary Ledger (4-Slot)": ledger_toks,
    "3. Ledger + Abjad Combined": ledger_abjad_toks,
    "4. Ledger + Abjad + Affixes": ledger_abjad_affix_toks,
    "5. Currier B Affix-Stripped": cb_stems,
    "6. Voynich Currier B (Actual)": cb_toks,
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
        connect(r, tok, weight=0.25, type="cb_anat")
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

cb_mean = [sum(z[k] for z in win_z["6. Voynich Currier B (Actual)"]) / 10.0 for k in range(9)]

md = [
    "# Currier B Anatomy Probe: Combined Apothecary Ledger + Abjad Shorthand\n",
    "![Currier B Anatomy Comparison](currier_b_anatomy_v2.png)\n",
    "Tests **Apothecary Ledger + Vowel-Dropped Abjad Shorthand** (with and without morphological affix tags) against actual **Voynich Currier B** across **10 independent 300-token windows** (`30` Monte Carlo shuffles/window, `seed=42`).\n",
    "| Mechanism | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\\Phi$ (`Mean ± SD`) | `cos(Currier B)` |",
    "| :--- | :---: | :---: | :---: | :---: | :---: |",
]

print(f"\n=== CURRIER B ANATOMY: LEDGER + ABJAD COMBINED (10 x 300 Windows, Seed=42) ===")
print(f"{'Mechanism':31s} | {'W':>2s} | {'Zc Mean(SD)':>13s} | {'Zs Mean(SD)':>13s} | {'ZPhi Mean(SD)':>14s} | {'cos(CB)':>8s}")
print("-" * 96)

labels, zp_m, zp_s, cb_c_list = [], [], [], []
for name, zl in win_z.items():
    n = len(zl)
    st = lambda idx: (float(np.mean([z[idx] for z in zl])), float(np.std([z[idx] for z in zl])))
    zcm, zcs = st(0); zsm, zss = st(3); zpm, zps = st(4)
    cbc = float(np.mean([cos(z, cb_mean) for z in zl]))
    print(f"{name:31s} | {n:2d} | {zcm:+6.2f}({zcs:4.2f}) | {zsm:+6.2f}({zss:4.2f}) | {zpm:+6.2f}({zps:5.2f}) | {cbc:+8.4f}")
    md.append(f"| **{name}** | `{n}` | `{zcm:+.2f} ± {zcs:.2f}` | `{zsm:+.2f} ± {zss:.2f}` | `{zpm:+.2f} ± {zps:.2f}` | `{cbc:+.4f}` |")
    labels.append(name); zp_m.append(zpm); zp_s.append(zps); cb_c_list.append(cbc)

Path("CURRIER_B_ANATOMY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6), dpi=220)
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

y = np.arange(len(labels))
bar_cols1 = ["#a371f7" if "Combined" in l or "Affixes" in l else "#58a6ff" for l in labels]
ax1.axvline(0, color="#8b949e", linewidth=1.0)
ax1.barh(y, cb_c_list, height=0.52, color=bar_cols1)
for i, v in enumerate(cb_c_list):
    ax1.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.3f}", va="center",
             ha="left" if v >= 0 else "right", fontweight="bold", color="#e6edf3")
ax1.set_yticks(y); ax1.set_yticklabels(labels, fontweight="bold", color="#e6edf3")
ax1.invert_yaxis(); ax1.set_xlim(-0.35, 0.85)
ax1.set_xlabel("Mean Cosine Similarity to Actual Currier B", color="#c9d1d9")
ax1.set_title("A. Structural Match to Voynich Currier B", fontweight="bold", color="#f0f6fc")

colors2 = ["#ff7b72" if m < 0 else "#79c0ff" for m in zp_m]
ax2.axvline(0, color="#8b949e", linewidth=1.0)
ax2.barh(y, zp_m, xerr=zp_s, height=0.52, color=colors2, error_kw=dict(ecolor="#f0f6fc", elinewidth=1.2, capsize=3))
for i, (m, s) in enumerate(zip(zp_m, zp_s)):
    ax2.text(m + (s + 0.14 if m >= 0 else -(s + 0.14)), i, f"{m:+.2f}",
             va="center", ha="left" if m >= 0 else "right", fontweight="bold", color="#e6edf3")
ax2.set_yticks(y); ax2.set_yticklabels([""] * len(labels))
ax2.invert_yaxis(); ax2.set_xlim(-3.2, 2.5)
ax2.set_xlabel("Phase Coherence Z-Score Z_Φ (Mean ± SD)", color="#c9d1d9")
ax2.set_title("B. Coherence Polarity (Z_Φ)", fontweight="bold", color="#f0f6fc")

fig.suptitle("XEMBRA (.xc) Currier B Anatomy: Combined Apothecary Ledger + Abjad Shorthand (10 x 300 Windows)",
             fontsize=12.5, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("currier_b_anatomy_v2.png", dpi=220, facecolor=fig.get_facecolor())
print("\nSaved CURRIER_B_ANATOMY.md and currier_b_anatomy_v2.png")
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")
fig, axes = plt.subplots(2, 2, figsize=(15.5, 9.2), dpi=220)
fig.patch.set_facecolor("#0d1117")

for ax in axes.flat:
    ax.set_facecolor("#161b22")
    ax.grid(axis="x", color="#30363d", linestyle="--", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#484f58")
    ax.spines["bottom"].set_color("#484f58")

# Panel 1: Step 1 - Five Scribes (cos to Scribe 1)
ax = axes[0, 0]
s_names = ["Scribe 1 (n=10)", "Scribe 2 (n=10)", "Scribe 3 (n=10)", "Scribe 4 (n=10)", "Scribe 5 (n=3)"]
s_cos = [0.3327, 0.2542, -0.3484, -0.3627, 0.0671]
s_cols = ["#3fb950" if v > 0.1 else ("#ff7b72" if v < -0.1 else "#8b949e") for v in s_cos]
y1 = np.arange(len(s_names))
ax.axvline(0, color="#8b949e", linewidth=1.0)
ax.barh(y1, s_cos, height=0.55, color=s_cols)
for i, v in enumerate(s_cos):
    ax.text(v + (0.03 if v >= 0 else -0.03), i, f"{v:+.3f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=9.5, fontweight="bold", color="#e6edf3")
ax.set_yticks(y1); ax.set_yticklabels(s_names, fontweight="bold", fontsize=10, color="#e6edf3")
ax.invert_yaxis(); ax.set_xlim(-0.55, 0.55)
ax.set_xlabel("Alignment to Scribe 1 Centroid (cos θ)", fontsize=9.5, color="#c9d1d9")
ax.set_title("1. Five Scribes Split Into Two Opposite Teams", fontsize=11.5, fontweight="bold", color="#f0f6fc", pad=10)

# Panel 2: Step 2 - Historical Herbal vs 14th-C Recipes (Z_Phi)
ax = axes[0, 1]
r_names = ["Historical Herbal (Desc.)", "14th-C. Recipes (Proc.)", "Voynich Currier A (Herbal)", "Voynich Currier B (Recipe)"]
r_zp = [-0.57, -0.55, -0.46, 0.46]
r_sd = [1.75, 1.73, 1.93, 0.57]
r_cols = ["#ff7b72" if v < 0 else "#58a6ff" for v in r_zp]
y2 = np.arange(len(r_names))
ax.axvline(0, color="#8b949e", linewidth=1.0)
ax.barh(y2, r_zp, xerr=r_sd, height=0.52, color=r_cols, error_kw=dict(ecolor="#e6edf3", elinewidth=1.1, capsize=3))
for i, (m, s) in enumerate(zip(r_zp, r_sd)):
    ax.text(m + (s + 0.12 if m >= 0 else -(s + 0.12)), i, f"{m:+.2f}", va="center",
            ha="left" if m >= 0 else "right", fontsize=9.5, fontweight="bold", color="#e6edf3")
ax.set_yticks(y2); ax.set_yticklabels(r_names, fontweight="bold", fontsize=10, color="#e6edf3")
ax.invert_yaxis(); ax.set_xlim(-3.2, 2.2)
ax.set_xlabel("Coherence Polarity Z_Φ (Mean ± SD)", fontsize=9.5, color="#c9d1d9")
ax.set_title("2. Medieval Cookbooks Stay Negative; Currier B Flips", fontsize=11.5, fontweight="bold", color="#f0f6fc", pad=10)

# Panel 3: Step 3 - Symbolic & Slot Shorthand (cos to Currier B)
ax = axes[1, 0]
sym_names = ["Symbolic Music (ABC)", "Apothecary Formulas", "Slot-Template Shorthand", "Voynich Currier B (Target)"]
sym_cos = [-0.8205, -0.1917, 0.3103, 0.4694]
sym_cols = ["#ff7b72" if v < 0 else ("#a371f7" if v < 0.4 else "#58a6ff") for v in sym_cos]
y3 = np.arange(len(sym_names))
ax.axvline(0, color="#8b949e", linewidth=1.0)
ax.barh(y3, sym_cos, height=0.52, color=sym_cols)
for i, v in enumerate(sym_cos):
    ax.text(v + (0.04 if v >= 0 else -0.04), i, f"{v:+.3f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=9.5, fontweight="bold", color="#e6edf3")
ax.set_yticks(y3); ax.set_yticklabels(sym_names, fontweight="bold", fontsize=10, color="#e6edf3")
ax.invert_yaxis(); ax.set_xlim(-1.05, 0.75)
ax.set_xlabel("Alignment to Currier B Procedural Regime (cos θ)", fontsize=9.5, color="#c9d1d9")
ax.set_title("3. Prefix/Suffix Slot Shorthand Moves Toward Currier B", fontsize=11.5, fontweight="bold", color="#f0f6fc", pad=10)

# Panel 4: Step 4 - 20-Window Human vs AI & Voynich (Z_Phi)
ax = axes[1, 1]
h_names = ["Human Literary Prose (n=9)", "Human Herbal Prose (n=9)", "Live AI + Autoreg. (n=20)", "Voynich Currier A (n=20)", "Voynich Currier B (n=20)"]
h_zp = [-0.27, -0.36, -1.38, -0.79, 0.26]
h_sd = [0.61, 0.63, 2.89, 2.09, 0.95]
h_cols = ["#ff7b72" if v < 0 else "#58a6ff" for v in h_zp]
y4 = np.arange(len(h_names))
ax.axvline(0, color="#8b949e", linewidth=1.0)
ax.barh(y4, h_zp, xerr=h_sd, height=0.55, color=h_cols, error_kw=dict(ecolor="#e6edf3", elinewidth=1.1, capsize=3))
for i, (m, s) in enumerate(zip(h_zp, h_sd)):
    ax.text(m + (s + 0.14 if m >= 0 else -(s + 0.14)), i, f"{m:+.2f}", va="center",
            ha="left" if m >= 0 else "right", fontsize=9.5, fontweight="bold", color="#e6edf3")
ax.set_yticks(y4); ax.set_yticklabels(h_names, fontweight="bold", fontsize=10, color="#e6edf3")
ax.invert_yaxis(); ax.set_xlim(-4.8, 2.2)
ax.set_xlabel("20-Window Coherence Polarity Z_Φ (Mean ± SD)", fontsize=9.5, color="#c9d1d9")
ax.set_title("4. Multi-Window Stress Test: Currier B Stands Alone", fontsize=11.5, fontweight="bold", color="#f0f6fc", pad=10)

fig.suptitle("XEMBRA (.xc) Four-Step Multi-Window Synthesis: Scribes, Registers, Shorthand & Polarity",
             fontsize=14, fontweight="bold", color="#ffffff", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("four_step_synthesis.png", dpi=220, facecolor=fig.get_facecolor())
print("Saved four_step_synthesis.png")
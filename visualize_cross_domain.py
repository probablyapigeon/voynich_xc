import matplotlib.pyplot as plt
from xembra_core import PsiVector, connect, tau_ij

# Exact converged state vectors from your 450-token & 200-cycle XEMBRA experiments
v_base  = PsiVector(c=0.898, p=0.179, r=0.121, s=0.184, Φ=0.214, T=0.143, E=0.055, d=0.107, a=0.179)
f_attr  = PsiVector(c=0.841, p=0.228, r=0.176, s=0.149, Φ=0.274, T=0.182, E=0.096, d=0.137, a=0.228)
h_attr  = PsiVector(c=0.851, p=0.217, r=0.202, s=0.116, Φ=0.261, T=0.174, E=0.111, d=0.130, a=0.217)
v_finch = PsiVector(c=0.981, p=0.083, r=0.064, s=0.054, Φ=0.099, T=0.066, E=0.021, d=0.050, a=0.083)
v_human = PsiVector(c=0.982, p=0.078, r=0.073, s=0.042, Φ=0.094, T=0.063, E=0.024, d=0.047, a=0.078)

# Register directed τᵢⱼ structural resonance bridges in xembra_core
connect(v_base, f_attr,  weight=0.50, type="isolated_avian_baseline")
connect(v_base, h_attr,  weight=0.50, type="isolated_human_baseline")
connect(v_base, v_finch, weight=0.90, type="voynich_finch_200cycle_pull")
connect(v_base, v_human, weight=0.90, type="voynich_human_200cycle_pull")

nodes = [
    ("1. Voynich Manuscript (Isolated)", v_base,  "#8b5cf6", "o"),
    ("2. Bengalese Finch (Isolated)",    f_attr,  "#10b981", "^"),
    ("3. Human Prose (Isolated)",        h_attr,  "#3b82f6", "s"),
    ("4. Voynich <-> Finch (200-cyc)",   v_finch, "#f59e0b", "D"),
    ("5. Voynich <-> Human (200-cyc)",   v_human, "#ef4444", "X"),
]

fig = plt.figure(figsize=(11, 8.5))
ax = fig.add_subplot(111, projection="3d")

# Plot each trajectory attractor node with distinct color, marker, and 3D offset label
for label, psi, color, marker in nodes:
    ax.scatter(psi.c, psi.p, psi.r, s=160, c=color, marker=marker, edgecolors="black", linewidths=1.0, label=label, zorder=5)
    ax.text(psi.c + 0.003, psi.p + 0.003, psi.r + 0.003, label.split(" (")[0], fontsize=9, fontweight="bold", color=color)

# Draw τᵢⱼ coupling trajectories from xembra_core
styles = {
    "isolated_avian_baseline":   ("#10b981", "--", 1.5, "Baseline Span (Voynich - Finch)"),
    "isolated_human_baseline":   ("#3b82f6", "--", 1.5, "Baseline Span (Voynich - Human)"),
    "voynich_finch_200cycle_pull": ("#f59e0b", "-",  2.8, "200-Cycle Avian Field Pull"),
    "voynich_human_200cycle_pull": ("#ef4444", "-",  2.8, "200-Cycle Human Field Pull"),
}

for (p1, p2), props in tau_ij.items():
    edge_type = props.get("type", "")
    if edge_type in styles:
        col, ls, lw, edge_lbl = styles[edge_type]
        ax.plot([p1.c, p2.c], [p1.p, p2.p], [p1.r, p2.r], color=col, linestyle=ls, linewidth=lw, alpha=0.85, label=edge_lbl)

ax.set_title("XEMBRA 3D Cross-Domain Attractor Geometry:\nVoynich Manuscript vs. Bengalese Finch vs. Human Prose", fontsize=12, fontweight="bold")
ax.set_xlabel("c (Onset / Prefix Coupling)")
ax.set_ylabel("p (Positional Drift)")
ax.set_zlabel("r (Durational / Length Resonance)")
ax.legend(loc="upper left", fontsize=8.5, framealpha=0.92)
plt.tight_layout()
plt.savefig("voynich_avian_human_3d.png", dpi=200)
print("Saved 3D trajectory plot to: voynich_avian_human_3d.png")
plt.show()

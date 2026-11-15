import matplotlib.pyplot as plt
from xembra_core import PsiVector, Ouroboros, connect

# Converged 450-token domain attractors
v_base = PsiVector(c=0.898, p=0.179, r=0.121, s=0.184, Φ=0.214, T=0.143, E=0.055, d=0.107, a=0.179)
f_attr = PsiVector(c=0.841, p=0.228, r=0.176, s=0.149, Φ=0.274, T=0.182, E=0.096, d=0.137, a=0.228)
h_attr = PsiVector(c=0.851, p=0.217, r=0.202, s=0.116, Φ=0.261, T=0.174, E=0.111, d=0.130, a=0.217)

# Active states for 200-step continuous integration
cur_finch = PsiVector(c=0.898, p=0.179, r=0.121, s=0.184, Φ=0.214, T=0.143, E=0.055, d=0.107, a=0.179)
cur_human = PsiVector(c=0.898, p=0.179, r=0.121, s=0.184, Φ=0.214, T=0.143, E=0.055, d=0.107, a=0.179)

finch_curve = [cur_finch]
human_curve = [cur_human]

for step in range(200):
    connect(cur_finch, f_attr, weight=0.40, type="avian_step")
    cur_finch = Ouroboros(cur_finch, target=f_attr)
    finch_curve.append(cur_finch)

    connect(cur_human, h_attr, weight=0.40, type="human_step")
    cur_human = Ouroboros(cur_human, target=h_attr)
    human_curve.append(cur_human)

fig = plt.figure(figsize=(11.5, 8.5))
ax = fig.add_subplot(111, projection="3d")

# Plot the 200-step continuous curves
ax.plot(
    [n.c for n in finch_curve],
    [n.p for n in finch_curve],
    [n.r for n in finch_curve],
    color="#f59e0b", linewidth=2.6, alpha=0.95, label="Voynich <-> Bengalese Finch (200-Step Curve)"
)
ax.plot(
    [n.c for n in human_curve],
    [n.p for n in human_curve],
    [n.r for n in human_curve],
    color="#ef4444", linewidth=2.6, alpha=0.95, label="Voynich <-> Human Prose (200-Step Curve)"
)

# Plot milestone tick nodes every 25 steps along both curves
milestones = list(range(25, 200, 25))
ax.scatter(
    [finch_curve[i].c for i in milestones],
    [finch_curve[i].p for i in milestones],
    [finch_curve[i].r for i in milestones],
    c="#f59e0b", s=38, alpha=0.85, edgecolors="black", linewidths=0.5, label="25-Cycle Interval Ticks"
)
ax.scatter(
    [human_curve[i].c for i in milestones],
    [human_curve[i].p for i in milestones],
    [human_curve[i].r for i in milestones],
    c="#ef4444", s=38, alpha=0.85, edgecolors="black", linewidths=0.5
)

# Plot the 5 anchor endpoints
anchors = [
    ("Voynich Start (t=0)",        v_base,          "#8b5cf6", "o", 170),
    ("Bengalese Finch Field",      f_attr,          "#10b981", "^", 160),
    ("Human Prose Field",          h_attr,          "#3b82f6", "s", 160),
    ("Voynich <-> Finch (t=200)",  finch_curve[-1], "#d97706", "D", 170),
    ("Voynich <-> Human (t=200)",  human_curve[-1], "#b91c1c", "X", 180),
]

for lbl, psi, col, mk, sz in anchors:
    ax.scatter(psi.c, psi.p, psi.r, s=sz, c=col, marker=mk, edgecolors="black", linewidths=1.1, label=lbl, zorder=10)
    ax.text(psi.c + 0.0025, psi.p + 0.0025, psi.r + 0.0025, lbl, fontsize=8.5, fontweight="bold", color=col)

ax.set_title("XEMBRA 200-Step Continuous State Migration in 3D (c, p, r)\nVoynich Manuscript Coupled to Bengalese Finch vs. Human Prose", fontsize=12, fontweight="bold")
ax.set_xlabel("c (Onset / Prefix Coupling)")
ax.set_ylabel("p (Positional Drift)")
ax.set_zlabel("r (Durational / Length Resonance)")
ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
plt.tight_layout()
plt.savefig("voynich_200step_curves_3d.png", dpi=220)
print("Saved 200-step 3D continuous trajectory plot to: voynich_200step_curves_3d.png")
plt.show()

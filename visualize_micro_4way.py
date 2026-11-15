import random
import matplotlib.pyplot as plt
from xembra_core import PsiVector, Ouroboros, connect

voynich_words = open("data/voynich_clean.txt", encoding="utf-8", errors="ignore").read().split()[:450]
rng = random.Random(1404)
cipher_words = list(voynich_words)
rng.shuffle(cipher_words)
alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
shuffled_alpha = list(alpha)
rng.shuffle(shuffled_alpha)
cipher_words = [w.lower().translate(str.maketrans(alpha, "".join(shuffled_alpha))) for w in cipher_words]

psi_cipher = PsiVector(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, T=0.5, E=0.5, d=0.5, a=0.5)
for w in cipher_words:
    c_val = 0.9 if w.startswith(("8", "4o", "2", "o")) else 0.2
    s_val = 0.9 if w.endswith(("9", "am", "ay", "89")) else 0.2
    e_val = round(min(len(w) / 10.0, 1.0), 3)
    tok = PsiVector(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, T=0.4, E=e_val, d=0.3, a=0.5)
    connect(psi_cipher, tok, weight=0.25, type="cipher_stream")
    psi_cipher = Ouroboros(psi_cipher, target=tok)

v_base = PsiVector(c=0.898, p=0.179, r=0.121, s=0.184, Φ=0.214, T=0.143, E=0.055, d=0.107, a=0.179)
f_attr = PsiVector(c=0.841, p=0.228, r=0.176, s=0.149, Φ=0.274, T=0.182, E=0.096, d=0.137, a=0.228)
h_attr = PsiVector(c=0.851, p=0.217, r=0.202, s=0.116, Φ=0.261, T=0.174, E=0.111, d=0.130, a=0.217)

def trace_steps(start_vec, target_vec, steps=10):
    cur = PsiVector(
        c=start_vec.c, p=start_vec.p, r=start_vec.r, s=start_vec.s,
        Φ=start_vec.Φ, T=start_vec.T, E=start_vec.E, d=start_vec.d, a=start_vec.a
    )
    traj = list()
    traj.append(cur)
    for _ in range(steps):
        cur = Ouroboros(cur, target=target_vec)
        traj.append(cur)
    return traj

finch_micro  = trace_steps(v_base, f_attr, steps=10)
human_micro  = trace_steps(v_base, h_attr, steps=10)
cipher_micro = trace_steps(v_base, psi_cipher, steps=10)

# FIGURE 1: Zoomed t = 0 -> 10 Micro-Trajectory Arcs
fig1 = plt.figure(figsize=(11.5, 8.5))
ax1 = fig1.add_subplot(111, projection="3d")

curves = (
    ("Voynich -> Bengalese Finch (t=0..10)", finch_micro,  "#f59e0b", "D"),
    ("Voynich -> Human Prose (t=0..10)",     human_micro,  "#ef4444", "X"),
    ("Voynich -> Cipher/Null (t=0..10)",     cipher_micro, "#06b6d4", "P"),
)

for lbl, traj, col, mk in curves:
    ax1.plot([n.c for n in traj], [n.p for n in traj], [n.r for n in traj], color=col, linewidth=2.5, label=lbl)
    ax1.scatter([n.c for n in traj[1:]], [n.p for n in traj[1:]], [n.r for n in traj[1:]], c=col, s=55, marker=mk, edgecolors="black", linewidths=0.6)

ax1.scatter(v_base.c, v_base.p, v_base.r, s=190, c="#8b5cf6", marker="o", edgecolors="black", linewidths=1.2, label="Voynich Start (t=0)", zorder=12)
ax1.text(v_base.c - 0.004, v_base.p + 0.004, v_base.r + 0.004, "t=0 (Start)", fontsize=9, fontweight="bold", color="#8b5cf6")

for step_idx in (1, 2, 3, 5, 10):
    pt_f = finch_micro[step_idx]
    ax1.text(pt_f.c + 0.0015, pt_f.p + 0.002, pt_f.r - 0.003, f"F:t={step_idx}", fontsize=8, fontweight="bold", color="#b45309")
    pt_c = cipher_micro[step_idx]
    ax1.text(pt_c.c + 0.0015, pt_c.p - 0.004, pt_c.r + 0.002, f"C:t={step_idx}", fontsize=8, fontweight="bold", color="#0e7490")

ax1.set_title("XEMBRA Zoomed Micro-Trajectory (t = 0 to t = 10)\nCurved Capture Arcs: Voynich -> Finch vs. Human vs. Deterministic Cipher", fontsize=11.5, fontweight="bold")
ax1.set_xlabel("c (Onset / Prefix Coupling)")
ax1.set_ylabel("p (Positional Drift)")
ax1.set_zlabel("r (Durational / Length Resonance)")
ax1.legend(loc="upper left", fontsize=8.5, framealpha=0.92)
plt.tight_layout()
plt.savefig("voynich_t0_to_t10_micro_3d.png", dpi=220)

# FIGURE 2: Macroscopic 4-Way Attractor Map
fig2 = plt.figure(figsize=(11.5, 8.5))
ax2 = fig2.add_subplot(111, projection="3d")

macro_nodes = (
    ("1. Voynich Manuscript",     v_base,           "#8b5cf6", "o"),
    ("2. Bengalese Finch",        f_attr,           "#10b981", "^"),
    ("3. Human Prose",            h_attr,           "#3b82f6", "s"),
    ("4. Deterministic Cipher",   psi_cipher,       "#06b6d4", "P"),
    ("5. Voynich <-> Finch",      finch_micro[-1],  "#f59e0b", "D"),
    ("6. Voynich <-> Human",      human_micro[-1],  "#ef4444", "X"),
    ("7. Voynich <-> Cipher",     cipher_micro[-1], "#0891b2", "*"),
)

for lbl, psi, col, mk in macro_nodes:
    ax2.scatter(psi.c, psi.p, psi.r, s=170, c=col, marker=mk, edgecolors="black", linewidths=1.0, label=lbl, zorder=10)
    ax2.text(psi.c + 0.003, psi.p + 0.003, psi.r + 0.003, lbl, fontsize=8.5, fontweight="bold", color=col)

for traj, col in ((finch_micro, "#f59e0b"), (human_micro, "#ef4444"), (cipher_micro, "#06b6d4")):
    ax2.plot([n.c for n in traj], [n.p for n in traj], [n.r for n in traj], color=col, linewidth=2.2, alpha=0.85)

ax2.set_title("XEMBRA 4-Way Cross-Domain Attractor Geometry\nVoynich vs. Bengalese Finch vs. Human Prose vs. Deterministic Cipher", fontsize=11.5, fontweight="bold")
ax2.set_xlabel("c (Onset / Prefix Coupling)")
ax2.set_ylabel("p (Positional Drift)")
ax2.set_zlabel("r (Durational / Length Resonance)")
ax2.legend(loc="upper left", fontsize=8.5, framealpha=0.92)
plt.tight_layout()
plt.savefig("voynich_4way_attractors_3d.png", dpi=220)

print("Saved: voynich_t0_to_t10_micro_3d.png & voynich_4way_attractors_3d.png")
print("Deterministic Cipher Isolated State:", psi_cipher)
plt.show()

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

data = json.load(open("voynich_five_scribe_synthesis.json", encoding="utf-8"))
matrix = data["five_scribe_matrix"]

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), dpi=180, gridspec_kw={"width_ratios": [1.05, 1.25]})
fig.patch.set_facecolor("#0b0f19")

# --- PANEL 1: FIVE-SCRIBE TWO-CLASS GRAMMAR MATRIX ---
ax1.set_facecolor("#111827")
scribes = [f"Scribe {r['scribe_id']}\n({r['dialect']})" for r in matrix]
c1_vals = [r["class_1_pct"] for r in matrix]
c2_vals = [r["class_2_pct"] for r in matrix]
y_pos = range(len(scribes))[::-1]

bars1 = ax1.barh(y_pos, c1_vals, color="#38bdf8", height=0.55, label="Class 1: Upstream Bridge Nouns")
bars2 = ax1.barh(y_pos, c2_vals, left=c1_vals, color="#f59e0b", height=0.55, label="Class 2: Cross-Scribe Procedural Ops")

for y, c1, c2 in zip(y_pos, c1_vals, c2_vals):
    ax1.text(c1 / 2, y, f"{c1:.1f}%", va="center", ha="center", color="#0b0f19", fontweight="bold", fontsize=9.5)
    ax1.text(c1 + c2 / 2, y, f"{c2:.1f}%", va="center", ha="center", color="#0b0f19", fontweight="bold", fontsize=9.5)
    ax1.text(c1 + c2 + 1.2, y, f"Total: {c1 + c2:.1f}%", va="center", ha="left", color="#e5e7eb", fontweight="bold", fontsize=9.5)

ax1.set_yticks(list(y_pos))
ax1.set_yticklabels(scribes, color="#f3f4f6", fontsize=10, fontweight="bold")
ax1.set_xlim(0, 72)
ax1.set_xlabel("% of Total Scribe Tokens Covered", color="#9ca3af", fontsize=10)
ax1.set_title("1. FIVE-SCRIBE VOCABULARY & GRAMMAR SPLIT\n(40,240 Normalized Tokens Across 201 Folio Sides)", color="#f9fafb", fontsize=11.5, fontweight="bold", pad=14)
ax1.tick_params(axis="x", colors="#9ca3af")
for spine in ("top", "right"):
    ax1.spines[spine].set_visible(False)
for spine in ("bottom", "left"):
    ax1.spines[spine].set_color("#374151")
ax1.grid(axis="x", linestyle="--", alpha=0.2, color="#6b7280")
ax1.legend(loc="lower right", frameon=True, facecolor="#1f2937", edgecolor="#374151", labelcolor="#f3f4f6", fontsize=8.5)

# --- PANEL 2: DUAL-SUPPLY-CHAIN CROSS-SCRIBE TOPOLOGY ---
ax2.set_facecolor("#111827")
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis("off")
ax2.set_title("2. DUAL CROSS-SCRIBE SUPPLY CHAINS\n(o- Static Labels -> 4o- Activated Prose)", color="#f9fafb", fontsize=11.5, fontweight="bold", pad=14)

def draw_node(ax, x, y, w, h, title, subtitle, edge_color):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.2",
                                 facecolor="#1f2937", edgecolor=edge_color, linewidth=1.8)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", color="#f9fafb", fontweight="bold", fontsize=9.5)
    ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center", color="#9ca3af", fontsize=8)

# Supply Chain A (Top)
ax2.text(5.0, 9.35, "SUPPLY CHAIN A: BOTANICAL & APOTHECARY -> STARRED RECIPES", ha="center", color="#38bdf8", fontweight="bold", fontsize=9)
draw_node(ax2, 0.4, 7.1, 3.6, 1.7, "SCRIBE 1 (Currier A)", "Herbal A & Jar Labels (87r-102v)\n38.6% Class 1 Nouns | o- Prefix", "#38bdf8")
draw_node(ax2, 6.0, 7.6, 3.6, 1.35, "SCRIBE 3 (Currier B)", "Starred Recipes (103r-116r)\n34.3% Nouns + 21.4% Proc. Ops", "#f59e0b")
draw_node(ax2, 6.0, 5.75, 3.6, 1.35, "SCRIBE 5 (Currier B)", "Folio 115v (75.2% Covered)\n24.0% Nouns + 51.2% Proc. Ops", "#a855f7")

ax2.annotate("", xy=(5.85, 8.25), xytext=(4.15, 8.05), arrowprops=dict(arrowstyle="->", color="#38bdf8", lw=2))
ax2.annotate("", xy=(5.85, 6.45), xytext=(4.15, 7.65), arrowprops=dict(arrowstyle="->", color="#a855f7", lw=2))
ax2.text(5.0, 8.55, "135 Master\nBridges", ha="center", color="#e5e7eb", fontsize=7.8, fontweight="bold")
ax2.text(4.85, 6.45, "+146 Class 2\nOperators", ha="center", color="#fcd34d", fontsize=7.8, fontweight="bold")

# Divider
ax2.plot([0.3, 9.7], [4.95, 4.95], color="#374151", linestyle="--", lw=1)

# Supply Chain B (Bottom)
ax2.text(5.0, 4.4, "SUPPLY CHAIN B: ZODIAC NYMPH ROUNDELS -> BALNEOLOGICAL POOLS", ha="center", color="#34d399", fontweight="bold", fontsize=9)
draw_node(ax2, 0.4, 1.4, 3.6, 2.2, "SCRIBE 4 (Currier B)", "Zodiac Roundels (70r-73v)\nStar-Holding Nymph Labels\nStatic o- (oh989, ok1s9)", "#34d399")
draw_node(ax2, 6.0, 1.4, 3.6, 2.2, "SCRIBE 2 (Currier B)", "Bathing Pools (75r-84v) & Rosettes\n38.6% Nouns + 18.7% Proc. Ops\nActive 4o- (4oh989, 4ok1s79)", "#ec4899")

ax2.annotate("", xy=(5.85, 2.5), xytext=(4.15, 2.5), arrowprops=dict(arrowstyle="->", color="#34d399", lw=2.2))
ax2.text(5.0, 2.95, "220 Nymph\nBridges", ha="center", color="#e5e7eb", fontsize=8, fontweight="bold")
ax2.text(5.0, 1.85, "o- -> 4o-\nActivation", ha="center", color="#6ee7b7", fontsize=7.8, fontweight="bold")

fig.suptitle("VOYNICH CODEX FIVE-SCRIBE & DUAL-SUPPLY-CHAIN ARCHITECTURE (voynich_xc)", color="#f9fafb", fontsize=13.5, fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("voynich_five_scribe_network.png", facecolor=fig.get_facecolor())
print("Saved high-res chart -> voynich_five_scribe_network.png")

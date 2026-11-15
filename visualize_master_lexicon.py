import json
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def map_provenance_label(raw_cls):
    if "4-Way" in raw_cls:
        return "4-Way Bridge\n(69 tokens)"
    if "3-Way" in raw_cls:
        return "3-Way Bridge\n(47 tokens)"
    if "Apothecary" in raw_cls:
        return "Pure Apothecary\n(9 tokens)"
    if "Zodiac" in raw_cls or "Balneo" in raw_cls:
        return "Zodiac / Balneo\n(8 tokens)"
    return "Rosettes Bridge\n(2 tokens)"

def load_network_weights():
    lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
    rec = json.load(open("voynich_reconstructed_codex.json", encoding="utf-8"))

    ordered_classes = [
        "4-Way Bridge\n(69 tokens)",
        "3-Way Bridge\n(47 tokens)",
        "Pure Apothecary\n(9 tokens)",
        "Zodiac / Balneo\n(8 tokens)",
        "Rosettes Bridge\n(2 tokens)",
    ]
    target_jars = ["93r", "88v", "96v", "99r", "100v"]
    target_folios = ["104r", "106v", "113v", "115r"]

    tok_to_jars = {}
    class_to_jar = Counter()

    for entry in lex["entries"]:
        tok = entry["token"]
        cls_label = map_provenance_label(entry["provenance_class"])

        jars_found = set()
        for j in entry["source_pharma_jars"]:
            j_page = j.split(".")[0]
            if j_page in target_jars:
                jars_found.add(j_page)
        tok_to_jars[tok] = jars_found

        for jp in jars_found:
            class_to_jar[(cls_label, jp)] += 1

    jar_to_folio = Counter()
    folio_totals = Counter()

    for card in rec["cards"]:
        fp = card["folio_page"]
        if fp not in target_folios:
            continue
        for ing in card["ingredients"]:
            tok = ing["token"]
            folio_totals[fp] += 1
            for jp in tok_to_jars.get(tok, set()):
                jar_to_folio[(jp, fp)] += 1

    return ordered_classes, target_jars, target_folios, class_to_jar, jar_to_folio, folio_totals

def render_network():
    classes, jars, folios, class_to_jar, jar_to_folio, folio_totals = load_network_weights()

    fig, ax = plt.subplots(figsize=(15, 9), dpi=150)
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    x_cols = {"class": 1.5, "jar": 5.5, "folio": 9.5}
    y_classes = [8.2, 6.5, 4.8, 3.1, 1.4]
    y_jars = [8.0, 6.4, 4.8, 3.2, 1.6]
    y_folios = [7.6, 5.7, 3.8, 1.9]

    pos = {}
    for c, y in zip(classes, y_classes):
        pos[("class", c)] = (x_cols["class"], y)
    for j, y in zip(jars, y_jars):
        pos[("jar", j)] = (x_cols["jar"], y)
    for f, y in zip(folios, y_folios):
        pos[("folio", f)] = (x_cols["folio"], y)

    max_cj = max(class_to_jar.values()) if class_to_jar else 1
    for (c, j), w in class_to_jar.items():
        x1, y1 = pos[("class", c)]
        x2, y2 = pos[("jar", j)]
        lw = 0.8 + 4.8 * (w / max_cj)
        alpha = 0.25 + 0.55 * (w / max_cj)
        ax.plot([x1, x2], [y1, y2], color="#38bdf8", linewidth=lw, alpha=alpha, zorder=1)

    max_jf = max(jar_to_folio.values()) if jar_to_folio else 1
    for (j, f), w in jar_to_folio.items():
        x1, y1 = pos[("jar", j)]
        x2, y2 = pos[("folio", f)]
        lw = 0.8 + 5.2 * (w / max_jf)
        alpha = 0.25 + 0.60 * (w / max_jf)
        ax.plot([x1, x2], [y1, y2], color="#f59e0b", linewidth=lw, alpha=alpha, zorder=1)

    class_colors = ["#38bdf8", "#818cf8", "#34d399", "#f472b6", "#fbbf24"]
    for (c, y), col in zip(zip(classes, y_classes), class_colors):
        x = x_cols["class"]
        box = patches.FancyBboxPatch(
            (x - 1.15, y - 0.45), 2.3, 0.9,
            boxstyle="round,pad=0.12", facecolor="#1e293b", edgecolor=col, linewidth=2.2, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y, c, color="#f8fafc", fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=4)

    jar_notes = {
        "93r": "Jar Folio 93r\n(Central Dispensary)",
        "88v": "Jar Folio 88v\n(Early Apothecary)",
        "96v": "Jar Folio 96v\n(Rosettes & Bases)",
        "99r": "Jar Folio 99r\n(Multi-Label Hub)",
        "100v": "Jar Folio 100v\n(Closing Jars)",
    }
    for j, y in zip(jars, y_jars):
        x = x_cols["jar"]
        box = patches.FancyBboxPatch(
            (x - 1.05, y - 0.42), 2.1, 0.84,
            boxstyle="round,pad=0.12", facecolor="#1e293b", edgecolor="#fb923c", linewidth=2.2, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y, jar_notes[j], color="#ffedd5", fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=4)

    folio_notes = {
        "104r": f"Folio 104r (30.19% Dens.)\n{folio_totals['104r']} Recipe Bridge Hits",
        "106v": f"Folio 106v (50 Unique)\n{folio_totals['106v']} Recipe Bridge Hits",
        "113v": f"Folio 113v (29.03% Dens.)\n{folio_totals['113v']} Recipe Bridge Hits",
        "115r": f"Folio 115r (49 Unique)\n{folio_totals['115r']} Recipe Bridge Hits",
    }
    for f, y in zip(folios, y_folios):
        x = x_cols["folio"]
        box = patches.FancyBboxPatch(
            (x - 1.18, y - 0.45), 2.36, 0.9,
            boxstyle="round,pad=0.12", facecolor="#1e293b", edgecolor="#4ade80", linewidth=2.2, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y, folio_notes[f], color="#dcfce7", fontsize=9.5, fontweight="bold", ha="center", va="center", zorder=4)

    ax.text(x_cols["class"], 9.3, "1. UPSTREAM PROVENANCE\n(135 Master Lexicon Tokens)", color="#7dd3fc", fontsize=11, fontweight="bold", ha="center")
    ax.text(x_cols["jar"], 9.3, "2. PHARMACEUTICAL JARS\n(Top Dispensary Folios 88r-102v)", color="#fdba74", fontsize=11, fontweight="bold", ha="center")
    ax.text(x_cols["folio"], 9.3, "3. STARRED RECIPES\n(Top Density Folios 103r-116v)", color="#86efac", fontsize=11, fontweight="bold", ha="center")

    ax.set_title(
        "Voynich Codex Apothecary Supply-Chain Network (35 Probes | 135 Master Bridges | 359 Reconstructed Recipes)",
        color="#f8fafc", fontsize=13, fontweight="bold", pad=16
    )
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0.5, 10.0)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("voynich_master_network.png", dpi=300, facecolor=fig.get_facecolor())
    print("Saved publication network figure: voynich_master_network.png")
    plt.show()

if __name__ == "__main__":
    render_network()

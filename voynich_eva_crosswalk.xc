# Probe #36: FSG/Numeric-to-EVA Transliteration Crosswalk for the 135-Entry Master Lexicon
# Generates voynich_master_lexicon_eva.json and voynich_master_lexicon_eva.csv

import json
import csv

LIGATURE_RULES = [
    ("4o", "qo"),
    ("89", "dy"),
    ("1c", "ch"),
    ("am", "aiin"),
    ("an", "ain"),
    ("ae", "al"),
    ("oe", "ol"),
    ("ay", "ai"),
    ("oy", "oi"),
    ("K", "k"),
    ("T", "t"),
    ("P", "p"),
    ("F", "f"),
    ("H", "ckh"),
    ("C", "kh"),
    ("J", "cth"),
    ("A", "a"),
    ("N", "n"),
    ("8", "d"),
    ("9", "y"),
    ("1", "sh"),
    ("2", "s"),
    ("3", "i"),
    ("7", "g"),
    ("g", "q"),
    ("z", "s"),
]

def to_eva(token):
    out = []
    i = 0
    unmapped = set()
    while i < len(token):
        matched = False
        for src, dst in LIGATURE_RULES:
            if token.startswith(src, i):
                out.append(dst)
                i += len(src)
                matched = True
                break
        if not matched:
            ch = token[i]
            out.append(ch)
            if ch not in "oaeiykthpfslrncqg":
                unmapped.add(ch)
            i += 1
    return "".join(out), sorted(unmapped)

def extract_hits(entry):
    # Locate nested dict of section counts regardless of exact key name
    for k in ("section_hits", "hits", "counts", "sections", "section_counts"):
        if isinstance(entry.get(k), dict):
            return entry[k]
    for v in entry.values():
        if isinstance(v, dict) and any(sec in v for sec in ("herbal", "pharma", "recipes")):
            return v
    return {}

def run_crosswalk():
    lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
    eva_entries = []
    all_unmapped = set()

    for entry in lex["entries"]:
        raw_tok = entry["token"]
        eva_tok, unmapped = to_eva(raw_tok)
        all_unmapped.update(unmapped)

        sh = extract_hits(entry)
        total_hits = sum(v for v in sh.values() if isinstance(v, (int, float)))
        if total_hits == 0:
            for k in ("total_codex_hits", "total_hits", "total", "freq", "count"):
                if isinstance(entry.get(k), (int, float)) and entry[k] > 0:
                    total_hits = int(entry[k])
                    break

        jars = entry.get("source_pharma_jars", entry.get("pharma_jars", entry.get("jars", [])))
        cards = entry.get("sample_recipe_cards", entry.get("recipe_cards", entry.get("cards", [])))
        state = entry.get("xembra_state", entry.get("psi_state", entry.get("state", {})))

        enriched = {
            "xc_token": raw_tok,
            "eva_token": eva_tok,
            "provenance_class": entry.get("provenance_class", entry.get("class", "")),
            "total_codex_hits": int(total_hits),
            "section_hits": sh,
            "source_pharma_jars": jars,
            "sample_recipe_cards": cards,
            "xembra_state": state,
        }
        eva_entries.append(enriched)

    eva_entries.sort(key=lambda x: x["total_codex_hits"], reverse=True)

    out_json = {
        "metadata": {
            "probe": "voynich_eva_crosswalk.xc (Probe #36)",
            "total_entries": len(eva_entries),
            "transliteration_target": "Standard EVA (Extensible Voynich Alphabet)",
            "unmapped_characters": sorted(all_unmapped),
        },
        "entries": eva_entries,
    }
    open("voynich_master_lexicon_eva.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(out_json, indent=2)
    )

    with open("voynich_master_lexicon_eva.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "xc_token", "eva_token", "provenance_class", "total_codex_hits",
            "herbal_hits", "zodiac_hits", "balneo_hits", "rosettes_hits",
            "pharma_hits", "recipe_hits", "source_pharma_jars"
        ])
        for e in eva_entries:
            sh = e["section_hits"]
            writer.writerow([
                e["xc_token"],
                e["eva_token"],
                e["provenance_class"],
                e["total_codex_hits"],
                sh.get("herbal", 0),
                sh.get("zodiac", 0),
                sh.get("balneo", 0),
                sh.get("rosettes", 0),
                sh.get("pharma", 0),
                sh.get("recipes", 0),
                "; ".join(str(j) for j in e["source_pharma_jars"]),
            ])

    print(f"Exported {len(eva_entries)} EVA-crosswalked entries to voynich_master_lexicon_eva.json & .csv")
    print(f"Unmapped characters: {sorted(all_unmapped) if all_unmapped else 'None (100% mapped)'}")
    print("\nTop 15 Master Bridge Tokens (XC Numeric -> Standard EVA):")
    for e in eva_entries[:15]:
        print(f"  {e['xc_token']:10s} -> {e['eva_token']:12s} | Hits: {e['total_codex_hits']:4d} | {e['provenance_class']}")

if __name__ == "__main__":
    run_crosswalk()

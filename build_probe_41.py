import json, re
from pathlib import Path
from collections import Counter

def normalize_voynich(tok: str) -> str:
    t = re.sub(r"(6|7|8)?9$", "89", tok)
    t = re.sub(r"ap$", "ay", t)
    return re.sub(r"^(4o|o)(?=[a-zA-Z0-9]{2,})", "", t)

# Load Layer 1 & Layer 2 sets
synth = json.load(open("voynich_five_scribe_synthesis.json", encoding="utf-8"))
layer2_proc = {r["stem"] for r in synth["class_2_procedural_operators"]}
chain_b_nouns = {r["stem"] for r in synth["zodiac_to_bathing_bridges"]}

lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
lex_recs = lex if isinstance(lex, list) else next(v for v in lex.values() if isinstance(v, list))
chain_a_nouns = {normalize_voynich(r["token"]) for r in lex_recs if isinstance(r, dict) and "token" in r}
layer1_nouns = (chain_a_nouns | chain_b_nouns) - layer2_proc

# Scan full corpus for global stem counts & exact lines of 17r and 24v
corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(\d{1,3}[rv])([^>]*)>\s*(.+)$")

global_stem_hits = Counter()
global_stem_folios = {}
target_lines = {"17r": [], "24v": []}

for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    fid, meta, raw_text = m.group(1), m.group(2), m.group(3)
    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", raw_text)
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]

    for tok in toks:
        st = normalize_voynich(tok)
        global_stem_hits[st] += 1
        global_stem_folios.setdefault(st, set()).add(fid)

    if fid in target_lines and toks:
        target_lines[fid].append((meta.lstrip("."), toks))

def analyze_outlier(fid: str):
    annotated_lines = []
    obs_list = []
    l3_details = []
    hapax_count = 0

    for locus, toks in target_lines[fid]:
        tagged = []
        for tok in toks:
            st = normalize_voynich(tok)
            s_val = 0.9 if tok.startswith("4o") else (0.5 if tok.startswith("o") else 0.2)
            e_val = min(1.0, round(len(tok) / 10.0, 2))

            if st in layer1_nouns:
                tagged.append(f"[{tok}|L1]")
                obs_list.append((0.9, s_val, e_val))
            elif st in layer2_proc:
                tagged.append(f"[{tok}|L2]")
                obs_list.append((0.6, s_val, e_val))
            else:
                g_hits = global_stem_hits[st]
                other_folios = sorted(global_stem_folios[st] - {fid})
                if g_hits == 1:
                    hapax_count += 1
                tagged.append(f"{{{tok}|L3:{g_hits}}}")
                obs_list.append((0.2, s_val, e_val))
                l3_details.append({
                    "raw": tok,
                    "stem": st,
                    "global_hits": g_hits,
                    "other_folios": other_folios[:6],
                })
        annotated_lines.append((locus, " ".join(tagged)))

    # Deduplicate L3 isolates sorted by global frequency (cross-section orphans first, then hapax)
    seen = set()
    unique_l3 = []
    for item in sorted(l3_details, key=lambda x: x["global_hits"], reverse=True):
        if item["raw"] not in seen:
            seen.add(item["raw"])
            unique_l3.append(item)

    return annotated_lines, obs_list, unique_l3, hapax_count, len(l3_details)

lines_17r, obs_17r, l3_17r, hapax_17r, tot_l3_17r = analyze_outlier("17r")
lines_24v, obs_24v, l3_24v, hapax_24v, tot_l3_24v = analyze_outlier("24v")

xc_code = [
    "# XC Probe #41: Scribe 1 Herbal A Structural Anomaly Inspector (Folios 17r & 24v)",
    f"summary_17r = {{'total_l3': {tot_l3_17r}, 'true_hapax': {hapax_17r}, 'cross_section_orphans': {tot_l3_17r - hapax_17r}}}",
    f"summary_24v = {{'total_l3': {tot_l3_24v}, 'true_hapax': {hapax_24v}, 'cross_section_orphans': {tot_l3_24v - hapax_24v}}}",
    f"lines_17r = {repr(lines_17r)}",
    f"lines_24v = {repr(lines_24v)}",
    f"orphans_17r = {repr([x for x in l3_17r if x['global_hits'] > 1])}",
    f"orphans_24v = {repr([x for x in l3_24v if x['global_hits'] > 1])}",
    f"obs_17r = {repr(obs_17r)}",
    f"obs_24v = {repr(obs_24v)}",
    "",
    "def evolve_folio(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. XEMBRA STATE VECTORS: TOP HERBAL A ANOMALY FOLIOS (17r & 24v) ===')",
    "print('Folio 17r (65.0% Anomaly) :', evolve_folio(obs_17r, 'folio_17r_anomaly'))",
    "print('Folio 24v (61.2% Anomaly) :', evolve_folio(obs_24v, 'folio_24v_anomaly'))",
    "print('17r L3 Breakdown          :', summary_17r)",
    "print('24v L3 Breakdown          :', summary_24v)",
    "",
    "print('\\n=== 2. FOLIO 17r LINE-BY-LINE THREE-LAYER DISSECTION ===')",
    "for loc, txt in lines_17r:",
    "    print(f'  17r.{loc:<6}: {txt}')",
    "",
    "print('\\n=== 3. FOLIO 24v LINE-BY-LINE THREE-LAYER DISSECTION ===')",
    "for loc, txt in lines_24v:",
    "    print(f'  24v.{loc:<6}: {txt}')",
    "",
    "print('\\n=== 4. CROSS-SECTION ORPHANS ON 17r & 24v (NON-HAPAX LAYER-3 STEMS) ===')",
    "print('  [17r Orphans]:')",
    "for item in orphans_17r[:10]:",
    "    print(f\"    {item['raw']:<12} (stem: {item['stem']:<10}) | Global Hits: {item['global_hits']:<3} | Other Folios: {item['other_folios']}\")",
    "print('  [24v Orphans]:')",
    "for item in orphans_24v[:10]:",
    "    print(f\"    {item['raw']:<12} (stem: {item['stem']:<10}) | Global Hits: {item['global_hits']:<3} | Other Folios: {item['other_folios']}\")",
]

Path("voynich_17r_24v_anomaly_inspector.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_17r_24v_anomaly_inspector.xc successfully.")

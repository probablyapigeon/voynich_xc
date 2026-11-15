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

corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(84v|115v)([^>]*)>\s*(.+)$")

pages = {"84v": [], "115v": []}
for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    fid, meta, raw_text = m.group(1), m.group(2), m.group(3)
    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", raw_text)
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]
    if toks:
        pages[fid].append((meta.lstrip("."), toks))

def analyze_peak_page(fid: str):
    annotated_lines = []
    obs_list = []
    transitions = Counter()
    top_l1, top_l2 = Counter(), Counter()
    line_locks = []

    for locus, toks in pages[fid]:
        tagged = []
        seq = []
        locked_in_line = 0
        for tok in toks:
            st = normalize_voynich(tok)
            s_val = 0.9 if tok.startswith("4o") else (0.5 if tok.startswith("o") else 0.2)
            e_val = min(1.0, round(len(tok) / 10.0, 2))

            if st in layer1_nouns:
                tagged.append(f"[{tok}|L1]")
                seq.append("L1")
                top_l1[st] += 1
                locked_in_line += 1
                obs_list.append((0.9, s_val, e_val))
            elif st in layer2_proc:
                tagged.append(f"[{tok}|L2]")
                seq.append("L2")
                top_l2[st] += 1
                locked_in_line += 1
                obs_list.append((0.6, s_val, e_val))
            else:
                tagged.append(f"{{{tok}|L3}}")
                seq.append("L3")
                obs_list.append((0.2, s_val, e_val))

        for a, b in zip(seq, seq[1:]):
            transitions[f"{a}->{b}"] += 1

        pct = round(locked_in_line / len(toks) * 100, 1)
        line_locks.append((pct, locus, len(toks)))
        annotated_lines.append((locus, pct, " ".join(tagged)))

    line_locks.sort(reverse=True)
    return annotated_lines, obs_list, dict(transitions.most_common()), top_l1.most_common(8), top_l2.most_common(8), line_locks[:5]

lines_84v, obs_84v, trans_84v, l1_84v, l2_84v, best_lines_84v = analyze_peak_page("84v")
_, obs_115v, trans_115v, l1_115v, l2_115v, _ = analyze_peak_page("115v")

xc_code = [
    "# XC Probe #42: Peak Grammar-Lock Inspector (Folio 84v at 74.7% Lock vs. Folio 115v at 73.6%)",
    f"transitions_84v = {repr(trans_84v)}",
    f"transitions_115v = {repr(trans_115v)}",
    f"top_l1_84v = {repr(l1_84v)}",
    f"top_l2_84v = {repr(l2_84v)}",
    f"best_lines_84v = {repr(best_lines_84v)}",
    f"lines_84v = {repr(lines_84v)}",
    f"obs_84v = {repr(obs_84v)}",
    f"obs_115v = {repr(obs_115v)}",
    "",
    "def evolve_lock(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. XEMBRA PEAK-LOCK STATE VECTORS: FOLIO 84v (S2) VS. FOLIO 115v (S5) ===')",
    "print('Folio 84v (74.7% Lock | Balneo End) :', evolve_lock(obs_84v, 'folio_84v_peak_lock'))",
    "print('Folio 115v (73.6% Lock | Recipe S5) :', evolve_lock(obs_115v, 'folio_115v_peak_lock'))",
    "print('84v Bigram Transitions              :', transitions_84v)",
    "print('115v Bigram Transitions             :', transitions_115v)",
    "",
    "print('\\n=== 2. FOLIO 84v TOP LAYER-1 NOUNS & LAYER-2 PROCEDURAL OPERATORS ===')",
    "print('  Top L1 Reference Nouns   :', top_l1_84v)",
    "print('  Top L2 Procedural Ops    :', top_l2_84v)",
    "print('  Highest-Lock Lines (84v) :', best_lines_84v)",
    "",
    "print('\\n=== 3. FOLIO 84v LINE-BY-LINE THREE-LAYER GRAMMAR STREAM ===')",
    "for loc, pct, txt in lines_84v:",
    "    print(f'  84v.{loc:<6} [{pct:>5.1f}%]: {txt}')",
]

Path("voynich_84v_peak_lock_inspector.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_84v_peak_lock_inspector.xc successfully.")

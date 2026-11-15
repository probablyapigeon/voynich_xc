import json, re
from pathlib import Path
from collections import Counter, defaultdict

def normalize_voynich(tok: str) -> str:
    t = re.sub(r"(6|7|8)?9$", "89", tok)
    t = re.sub(r"ap$", "ay", t)
    return re.sub(r"^(4o|o)(?=[a-zA-Z0-9]{2,})", "", t)

# Load v1.0.5 datasets
synth = json.load(open("voynich_five_scribe_synthesis.json", encoding="utf-8"))
proc_set = {r["stem"] for r in synth["class_2_procedural_operators"]}
chain_b_set = {r["stem"] for r in synth["zodiac_to_bathing_bridges"]}

lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
lex_recs = lex if isinstance(lex, list) else next(v for v in lex.values() if isinstance(v, list))
chain_a_set = {normalize_voynich(r["token"]) for r in lex_recs if isinstance(r, dict) and "token" in r}

# Parse Rosettes foldout (folios 85 and 86) from raw corpus
corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(85|86)([rv]\d*)[^>]*>\s*(.+)$")

panel_stats = defaultdict(lambda: {"total": 0, "chain_a": 0, "chain_b": 0, "nexus": 0, "proc": 0})
nexus_stems = Counter()
nexus_examples = defaultdict(list)

obs_nexus, obs_chain_a, obs_chain_b, obs_proc = [], [], [], []

for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    panel = f"{m.group(1)}{m.group(2)}"
    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", m.group(3))
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]

    for tok in toks:
        stem = normalize_voynich(tok)
        if len(stem) < 2:
            continue
        in_a = stem in chain_a_set
        in_b = stem in chain_b_set
        in_p = stem in proc_set

        panel_stats[panel]["total"] += 1
        s_val = 0.9 if tok.startswith("4o") else (0.5 if tok.startswith("o") else 0.2)
        e_val = min(1.0, round(len(tok) / 10.0, 2))

        if in_a and in_b:
            panel_stats[panel]["nexus"] += 1
            nexus_stems[stem] += 1
            nexus_examples[stem].append(f"{panel}:{tok}")
            obs_nexus.append((0.95, s_val, e_val))
        elif in_a:
            panel_stats[panel]["chain_a"] += 1
            obs_chain_a.append((0.80, s_val, e_val))
        elif in_b:
            panel_stats[panel]["chain_b"] += 1
            obs_chain_b.append((0.75, s_val, e_val))
        elif in_p:
            panel_stats[panel]["proc"] += 1
            obs_proc.append((0.60, s_val, e_val))

top_nexus = [
    {"stem": st, "rosettes_hits": cnt, "samples": list(dict.fromkeys(nexus_examples[st]))[:6]}
    for st, cnt in nexus_stems.most_common(20)
]

panel_ranking = []
for p, st in sorted(panel_stats.items(), key=lambda x: x[1]["nexus"], reverse=True):
    tot = max(1, st["total"])
    panel_ranking.append({
        "panel": p,
        "total_tokens": st["total"],
        "dual_nexus_hits": st["nexus"],
        "nexus_pct": round(st["nexus"] / tot * 100, 1),
        "chain_a_only": st["chain_a"],
        "chain_b_only": st["chain_b"],
        "class_2_proc": st["proc"],
    })

xc_code = [
    "# XC Probe #37: Scribe 2 Rosettes Foldout (85r-86v) Dual-Supply-Chain Nexus Inspector",
    "# Tests convergence of Supply Chain A (S1 -> S3/S5) & Supply Chain B (S4 Zodiac -> S2 Bathing)",
    "",
    f"rosettes_panel_ranking = {repr(panel_ranking)}",
    f"top_dual_nexus_stems = {repr(top_nexus)}",
    f"obs_dual_nexus = {repr(obs_nexus[:250])}",
    f"obs_chain_a_only = {repr(obs_chain_a[:250])}",
    f"obs_chain_b_only = {repr(obs_chain_b[:250])}",
    f"obs_class2_proc = {repr(obs_proc[:250])}",
    "",
    "def evolve_nexus(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. XEMBRA ROSETTES (85r-86v) FOUR-WAY ROUTING STATE VECTORS ===')",
    "print('Dual-Chain Nexus (Chain A & B) :', evolve_nexus(obs_dual_nexus, 'rosettes_dual_nexus'))",
    "print('Supply Chain A Only (Herbal/Jar):', evolve_nexus(obs_chain_a_only, 'rosettes_chain_a'))",
    "print('Supply Chain B Only (Zodiac/Bath):', evolve_nexus(obs_chain_b_only, 'rosettes_chain_b'))",
    "print('Class 2 Procedural Ops (Currier B):', evolve_nexus(obs_class2_proc, 'rosettes_proc_ops'))",
    "",
    "print('\\n=== 2. ROSETTES FOLDOUT PANEL NEXUS RANKING (85r-86v) ===')",
    "for r in rosettes_panel_ranking:",
    "    print(f\"  Panel {r['panel']:<6} | Tokens: {r['total_tokens']:<4} | Dual Nexus: {r['dual_nexus_hits']:<3} ({r['nexus_pct']:>4.1f}%) | Chain A: {r['chain_a_only']:<3} | Chain B: {r['chain_b_only']:<3} | Proc: {r['class_2_proc']}\")",
    "",
    "print('\\n=== 3. TOP DUAL-SUPPLY-CHAIN NEXUS STEMS INSIDE ROSETTES ===')",
    "for item in top_dual_nexus_stems[:15]:",
    "    print(f\"  {item['stem']:<10} | Rosettes Hits: {item['rosettes_hits']:<3} | Samples: {item['samples']}\")",
]

Path("voynich_rosettes_nexus_probe.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_rosettes_nexus_probe.xc successfully.")


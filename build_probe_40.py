import json, re
from pathlib import Path
from collections import Counter, defaultdict
from scribe_map import get_scribe_id

def normalize_voynich(tok: str) -> str:
    t = re.sub(r"(6|7|8)?9$", "89", tok)
    t = re.sub(r"ap$", "ay", t)
    return re.sub(r"^(4o|o)(?=[a-zA-Z0-9]{2,})", "", t)

# Load Layer 1 (Supply Chain A + Supply Chain B Nouns) & Layer 2 (Class 2 Procedural Operators)
synth = json.load(open("voynich_five_scribe_synthesis.json", encoding="utf-8"))
layer2_proc = {r["stem"] for r in synth["class_2_procedural_operators"]}
chain_b_nouns = {r["stem"] for r in synth["zodiac_to_bathing_bridges"]}

lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
lex_recs = lex if isinstance(lex, list) else next(v for v in lex.values() if isinstance(v, list))
chain_a_nouns = {normalize_voynich(r["token"]) for r in lex_recs if isinstance(r, dict) and "token" in r}

layer1_nouns = (chain_a_nouns | chain_b_nouns) - layer2_proc

def get_section(fnum: int) -> str:
    if 1 <= fnum <= 66:
        return "Herbal (1r-66v)"
    if 67 <= fnum <= 73:
        return "Astro/Zodiac (67r-73v)"
    if 75 <= fnum <= 84:
        return "Balneological (75r-84v)"
    if fnum in (85, 86):
        return "Rosettes Foldout (85r-86v)"
    if 87 <= fnum <= 102:
        return "Pharma Jars (87r-102v)"
    if 103 <= fnum <= 116:
        return "Starred Recipes (103r-116v)"
    return "Other"

corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(\d{1,3})([rv])\d*[^>]*>\s*(.+)$")

sec_stats = defaultdict(lambda: {"tot": 0, "l1": 0, "l2": 0, "l3": 0})
folio_stats = defaultdict(lambda: {"tot": 0, "l1": 0, "l2": 0, "l3": 0, "scribe": 0})
sec_obs = defaultdict(list)

tot_all, l1_all, l2_all, l3_all = 0, 0, 0, 0

for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    fnum, side = int(m.group(1)), m.group(2)
    fid = f"{fnum}{side}"
    sid = get_scribe_id(fid)
    if sid is None:
        continue
    sec = get_section(fnum)

    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", m.group(3))
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]

    folio_stats[fid]["scribe"] = sid
    for tok in toks:
        st = normalize_voynich(tok)
        tot_all += 1
        sec_stats[sec]["tot"] += 1
        folio_stats[fid]["tot"] += 1

        s_val = 0.9 if tok.startswith("4o") else (0.5 if tok.startswith("o") else 0.2)
        e_val = min(1.0, round(len(tok) / 10.0, 2))

        if st in layer1_nouns:
            l1_all += 1
            sec_stats[sec]["l1"] += 1
            folio_stats[fid]["l1"] += 1
            c_val = 0.9
        elif st in layer2_proc:
            l2_all += 1
            sec_stats[sec]["l2"] += 1
            folio_stats[fid]["l2"] += 1
            c_val = 0.6
        else:
            l3_all += 1
            sec_stats[sec]["l3"] += 1
            folio_stats[fid]["l3"] += 1
            c_val = 0.2

        if len(sec_obs[sec]) < 250:
            sec_obs[sec].append((c_val, s_val, e_val))

# Rank folios (min 80 tokens) by highest structural lock vs. highest residual anomaly
eligible = []
for fid, st in folio_stats.items():
    if st["tot"] >= 80:
        lock_pct = round((st["l1"] + st["l2"]) / st["tot"] * 100, 1)
        anom_pct = round(st["l3"] / st["tot"] * 100, 1)
        eligible.append({
            "folio": fid,
            "scribe": st["scribe"],
            "tokens": st["tot"],
            "lock_pct": lock_pct,
            "l1_pct": round(st["l1"] / st["tot"] * 100, 1),
            "l2_pct": round(st["l2"] / st["tot"] * 100, 1),
            "anomaly_pct": anom_pct,
        })

most_locked = sorted(eligible, key=lambda x: x["lock_pct"], reverse=True)[:10]
most_anomalous = sorted(eligible, key=lambda x: x["anomaly_pct"], reverse=True)[:10]

sec_summary = []
for sec, st in sec_stats.items():
    tot = max(1, st["tot"])
    sec_summary.append({
        "section": sec,
        "tokens": tot,
        "l1_pct": round(st["l1"] / tot * 100, 1),
        "l2_pct": round(st["l2"] / tot * 100, 1),
        "l3_pct": round(st["l3"] / tot * 100, 1),
        "total_lock_pct": round((st["l1"] + st["l2"]) / tot * 100, 1),
    })

xc_code = [
    "# XC Milestone Probe #40: Master Three-Layer Codex Architecture & Anomaly Detector",
    "# Unifies Layer 1 Reference Nouns, Layer 2 Procedural Operators & Layer 3 Residual Isolates",
    "",
    f"global_totals = {{'tokens': {tot_all}, 'l1_nouns': {l1_all}, 'l2_proc': {l2_all}, 'l3_residual': {l3_all}, 'total_lock_pct': {round((l1_all + l2_all) / tot_all * 100, 2)}}}",
    f"section_summary = {repr(sec_summary)}",
    f"most_locked_folios = {repr(most_locked)}",
    f"most_anomalous_folios = {repr(most_anomalous)}",
    f"sec_obs_map = {repr(dict(sec_obs))}",
    "",
    "def evolve_section(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. MILESTONE #40 GLOBAL THREE-LAYER CODEX COVERAGE ===')",
    "print(f\"Total Extant Tokens : {global_totals['tokens']:,}\")",
    "print(f\"Layer 1 (Ref Nouns) : {global_totals['l1_nouns']:,} ({global_totals['l1_nouns']/global_totals['tokens']*100:.1f}%)\")",
    "print(f\"Layer 2 (Proc Ops)  : {global_totals['l2_proc']:,} ({global_totals['l2_proc']/global_totals['tokens']*100:.1f}%)\")",
    "print(f\"Layer 3 (Residual)  : {global_totals['l3_residual']:,} ({global_totals['l3_residual']/global_totals['tokens']*100:.1f}%)\")",
    "print(f\"COMBINED CODEX LOCK : {global_totals['total_lock_pct']}%\")",
    "",
    "print('\\n=== 2. SECTION-BY-SECTION THREE-LAYER BREAKDOWN & Ψ ATTRACTORS ===')",
    "for s in section_summary:",
    "    vec = evolve_section(sec_obs_map[s['section']], s['section'])",
    "    print(f\"  {s['section']:<28} | Lock: {s['total_lock_pct']:>5.1f}% (L1:{s['l1_pct']:>4.1f}% L2:{s['l2_pct']:>4.1f}% L3:{s['l3_pct']:>4.1f}%) | {vec}\")",
    "",
    "print('\\n=== 3. TOP 10 MOST STRUCTURALLY LOCKED FOLIOS (HIGHEST GRAMMAR DENSITY) ===')",
    "for f in most_locked_folios:",
    "    print(f\"  Folio {f['folio']:<5} [S{f['scribe']}] | Lock: {f['lock_pct']:>5.1f}% (L1:{f['l1_pct']:>4.1f}%, L2:{f['l2_pct']:>4.1f}%) | Tokens: {f['tokens']}\")",
    "",
    "print('\\n=== 4. TOP 10 STRUCTURAL ANOMALY FOLIOS (HIGHEST LAYER-3 ISOLATE DENSITY) ===')",
    "for f in most_anomalous_folios:",
    "    print(f\"  Folio {f['folio']:<5} [S{f['scribe']}] | Residual Anomaly: {f['anomaly_pct']:>5.1f}% (Lock: {f['lock_pct']:>4.1f}%) | Tokens: {f['tokens']}\")",
]

Path("voynich_master_codex_synthesis_40.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_master_codex_synthesis_40.xc successfully.")

import re
from pathlib import Path
from collections import Counter, defaultdict
from scribe_map import get_scribe_id

corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(\d{1,3})([rv])\d*[^>]*>\s*(.+)$")

# Match canonical hc89 / hC89 / hcc89 / hCC89 family (including 6/7/8 plume variants before 9)
HC89_RE = re.compile(r"^(4oe|oe|4o|o|9|8|1|2|e|k|g|s|y)?(h[cC]{1,2}(?:6|7|8)?9)$")

def classify_prefix(pref: str) -> str:
    if not pref:
        return "bare"
    if pref == "o":
        return "o-"
    if pref == "4o":
        return "4o-"
    if pref in ("oe", "4oe"):
        return "oe-/4oe-"
    return f"other({pref})"

def get_section(fnum: int) -> str:
    if 1 <= fnum <= 66:
        return "Herbal (1r-66v)"
    if 67 <= fnum <= 73:
        return "Astro/Zodiac (67r-73v)"
    if 75 <= fnum <= 84:
        return "Balneological (75r-84v)"
    if fnum in (85, 86):
        return "Rosettes (85r-86v)"
    if 87 <= fnum <= 102:
        return "Pharma Jars (87r-102v)"
    if 103 <= fnum <= 116:
        return "Starred Recipes (103r-116v)"
    return "Other"

scribe_prefixes = defaultdict(Counter)
section_prefixes = defaultdict(Counter)
prefix_raw_forms = defaultdict(Counter)
prefix_prev = defaultdict(Counter)
prefix_next = defaultdict(Counter)
prefix_obs = defaultdict(list)

total_hits = 0

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

    for idx, tok in enumerate(toks):
        hm = HC89_RE.match(tok)
        if not hm:
            continue
        pref_raw, root = hm.group(1) or "", hm.group(2)
        p_state = classify_prefix(pref_raw)

        total_hits += 1
        scribe_prefixes[sid][p_state] += 1
        section_prefixes[sec][p_state] += 1
        prefix_raw_forms[p_state][tok] += 1

        prev_tok = toks[idx - 1] if idx > 0 else "<LINE_START>"
        next_tok = toks[idx + 1] if idx + 1 < len(toks) else "<LINE_END>"
        prefix_prev[p_state][prev_tok] += 1
        prefix_next[p_state][next_tok] += 1

        if len(prefix_obs[p_state]) < 250:
            s_val = {"bare": 0.2, "o-": 0.5, "4o-": 0.9, "oe-/4oe-": 0.8}.get(p_state, 0.4)
            c_val = 0.85 if "C" in root else 0.65
            e_val = min(1.0, round(len(tok) / 10.0, 2))
            prefix_obs[p_state].append((c_val, s_val, e_val))

states_order = ["bare", "o-", "4o-", "oe-/4oe-"]

scribe_table = []
for sid in sorted(scribe_prefixes):
    c = scribe_prefixes[sid]
    tot = sum(c.values())
    scribe_table.append({
        "scribe": sid,
        "total": tot,
        "bare": c["bare"],
        "o": c["o-"],
        "qo": c["4o-"],
        "oe": c["oe-/4oe-"],
        "other": tot - sum(c[k] for k in states_order),
    })

section_table = []
for sec, c in section_prefixes.items():
    tot = sum(c.values())
    section_table.append({
        "section": sec,
        "total": tot,
        "bare": c["bare"],
        "o": c["o-"],
        "qo": c["4o-"],
        "oe": c["oe-/4oe-"],
        "other": tot - sum(c[k] for k in states_order),
    })

context_summary = {}
for st in states_order:
    context_summary[st] = {
        "total": sum(prefix_raw_forms[st].values()),
        "top_forms": prefix_raw_forms[st].most_common(5),
        "top_prev": prefix_prev[st].most_common(4),
        "top_next": prefix_next[st].most_common(4),
    }

xc_code = [
    "# XC Probe #43: Complete hc89 / hC89 / hcc89 Inflectional Paradigm Across Scribes 1-5",
    f"total_hc89_hits = {total_hits}",
    f"scribe_table = {repr(scribe_table)}",
    f"section_table = {repr(section_table)}",
    f"context_summary = {repr(context_summary)}",
    f"obs_bare = {repr(prefix_obs['bare'])}",
    f"obs_o = {repr(prefix_obs['o-'])}",
    f"obs_4o = {repr(prefix_obs['4o-'])}",
    f"obs_oe = {repr(prefix_obs['oe-/4oe-'])}",
    "",
    "def evolve_paradigm(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print(f'=== 1. XEMBRA STATE VECTORS BY PREFIX STATE (TOTAL hc89 FAMILY HITS: {total_hc89_hits}) ===')",
    "print('State 1: Bare Root (hc89/hC89)      :', evolve_paradigm(obs_bare, 'hc89_bare'))",
    "print('State 2: o- Prefix (ohc89/ohC89)   :', evolve_paradigm(obs_o, 'hc89_o_prefix'))",
    "print('State 3: 4o- Prefix (4ohc89/4ohC89):', evolve_paradigm(obs_4o, 'hc89_4o_prefix'))",
    "print('State 4: oe-/4oe- Prefix (oehc89)  :', evolve_paradigm(obs_oe, 'hc89_oe_prefix'))",
    "",
    "print('\\n=== 2. SCRIBE-BY-SCRIBE hc89 INFLECTION MATRIX (SCRIBES 1-5) ===')",
    "for r in scribe_table:",
    "    print(f\"  Scribe {r['scribe']} | Total: {r['total']:<4} | Bare: {r['bare']:<4} | o-: {r['o']:<4} | 4o-: {r['qo']:<4} | oe-/4oe-: {r['oe']:<4} | Other: {r['other']}\")",
    "",
    "print('\\n=== 3. SECTION-BY-SECTION hc89 INFLECTION MATRIX ===')",
    "for r in section_table:",
    "    print(f\"  {r['section']:<28} | Total: {r['total']:<4} | Bare: {r['bare']:<4} | o-: {r['o']:<4} | 4o-: {r['qo']:<4} | oe-/4oe-: {r['oe']:<4} | Other: {r['other']}\")",
    "",
    "print('\\n=== 4. SYNTACTIC SLOT CONTEXT ([PREV] -> [FORM] -> [NEXT]) BY PREFIX ===')",
    "for st, info in context_summary.items():",
    "    print(f\"  [{st:<8}] (n={info['total']}): Forms={info['top_forms']} | Prev={info['top_prev']} | Next={info['top_next']}\")",
]

Path("voynich_hc89_paradigm_probe.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_hc89_paradigm_probe.xc successfully.")

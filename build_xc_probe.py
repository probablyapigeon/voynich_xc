import json, re
from pathlib import Path
from scribe_map import get_scribe_id
def normalize_voynich_v2(tok: str) -> str:
    t = re.sub(r"(6|7|8)?9$", "89", tok)
    t = re.sub(r"ap$", "ay", t)
    return re.sub(r"^(4o|o)(?=[a-zA-Z0-9]{2,})", "", t)

_lex = json.load(open("voynich_master_lexicon.json", encoding="utf-8"))
_recs = _lex if isinstance(_lex, list) else next(v for v in _lex.values() if isinstance(v, list))
norm_master = {normalize_voynich_v2(r["token"]) for r in _recs if isinstance(r, dict) and "token" in r}

synth = json.load(open("voynich_five_scribe_synthesis.json", encoding="utf-8"))
proc_set = {r["stem"] for r in synth["class_2_procedural_operators"]}
corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(\d{1,3})([rv]\d*)[^>]*>\s*(.+)$")

scribe_obs = {1: [], 2: [], 3: [], 4: [], 5: []}

for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    ftag = f"{m.group(1)}{m.group(2)}"
    sid = get_scribe_id(ftag)
    if sid is None:
        continue
    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", m.group(3))
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]

    for tok in toks:
        if len(scribe_obs[sid]) >= 250:
            break
        stem = normalize_voynich_v2(tok)
        c_val = 0.9 if stem in norm_master else (0.5 if stem in proc_set else 0.2)
        s_val = 0.9 if tok.startswith("4o") else (0.5 if tok.startswith("o") else 0.2)
        e_val = min(1.0, round(len(tok) / 10.0, 2))
        scribe_obs[sid].append((c_val, s_val, e_val))

top_zb = synth["zodiac_to_bathing_bridges"][:15]
zodiac_b_obs = [(0.8, 0.5, min(1.0, round(len(b["stem"]) / 8.0, 2))) for b in top_zb]
bathing_b_obs = [(0.8, 0.9 if b["o_to_4o_activation_observed"] else 0.5, min(1.0, round(len(b["stem"]) / 8.0, 2))) for b in top_zb]

xc_lines = [
    "# XC Five-Scribe Partition & Dual-Supply-Chain Convergence Probe",
    f"five_scribe_matrix = {repr(synth['five_scribe_matrix'])}",
    f"top_procedural_ops = {repr(synth['class_2_procedural_operators'][:15])}",
    f"zodiac_bathing_bridges = {repr(top_zb)}",
    f"scribe_1_obs = {repr(scribe_obs[1])}",
    f"scribe_2_obs = {repr(scribe_obs[2])}",
    f"scribe_3_obs = {repr(scribe_obs[3])}",
    f"scribe_4_obs = {repr(scribe_obs[4])}",
    f"scribe_5_obs = {repr(scribe_obs[5])}",
    f"supply_chain_b_zodiac_obs = {repr(zodiac_b_obs)}",
    f"supply_chain_b_bathing_obs = {repr(bathing_b_obs)}",
    "",
    "def evolve_scribe_state(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. XEMBRA FIVE-SCRIBE STATE VECTOR EVOLUTION (SCRIBES 1-5) ===')",
    "print('Scribe 1 (Currier A | Herbal/Jars)     :', evolve_scribe_state(scribe_1_obs, 'scribe_1_currier_a'))",
    "print('Scribe 2 (Currier B | Bathing/Rosettes):', evolve_scribe_state(scribe_2_obs, 'scribe_2_balneo'))",
    "print('Scribe 3 (Currier B | Starred Recipes) :', evolve_scribe_state(scribe_3_obs, 'scribe_3_recipes'))",
    "print('Scribe 4 (Currier B | Zodiac Roundels) :', evolve_scribe_state(scribe_4_obs, 'scribe_4_zodiac'))",
    "print('Scribe 5 (Currier B | Folio 115v High) :', evolve_scribe_state(scribe_5_obs, 'scribe_5_procedural'))",
    "",
    "print('\\n=== 2. SUPPLY CHAIN B: ZODIAC NYMPHS (S4) -> BATHING POOLS (S2) ===')",
    "print('Zodiac Roundels (70r-73v | o- Static)  :', evolve_scribe_state(supply_chain_b_zodiac_obs, 'zodiac_nymph_source'))",
    "print('Bathing Pools   (75r-84v | 4o- Active) :', evolve_scribe_state(supply_chain_b_bathing_obs, 'bathing_nymph_target'))",
    "",
    "print('\\n=== 3. TOP CROSS-SCRIBE PROCEDURAL OPERATORS (CLASS 2) ===')",
    "for op in top_procedural_ops[:10]:",
    "    print(' ', op['stem'], '| S3:', op['scribe_3_hits'], '| S5:', op['scribe_5_hits'], '| Total:', op['total_recipe_hits'])",
    "",
    "print('\\n=== 4. EXCLUSIVE ZODIAC <-> BATHING NYMPH BRIDGES ===')",
    "for b in zodiac_bathing_bridges[:10]:",
    "    act = '[o- -> 4o- ACTIVATED]' if b['o_to_4o_activation_observed'] else '[Direct Bridge]'",
    "    print(' ', b['stem'], '| Excl:', b['nymph_pair_exclusivity_pct'], '% |', act, '|', b['zodiac_samples'], '<->', b['bathing_samples'])",
]

Path("voynich_five_scribe_probe.xc").write_text("\n".join(xc_lines), encoding="utf-8")
print("Rebuilt voynich_five_scribe_probe.xc cleanly with per-scribe obs lists.")


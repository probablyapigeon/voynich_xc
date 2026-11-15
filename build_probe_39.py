import json, math, random, re
from pathlib import Path
from collections import Counter, defaultdict
from scribe_map import get_scribe_id

random.seed(42)

def normalize_voynich(tok: str) -> str:
    t = re.sub(r"(6|7|8)?9$", "89", tok)
    t = re.sub(r"ap$", "ay", t)
    return re.sub(r"^(4o|o)(?=[a-zA-Z0-9]{2,})", "", t)

corpus_path = Path("data/voynich_raw.txt")
FOLIO_LINE_RE = re.compile(r"^<f?(\d{1,3})([rv])\d*[^>]*>\s*(.+)$")

# Collect rare normalized stems (len >= 4) per folio side (e.g., '1r', '1v', '56v')
folio_stems = defaultdict(Counter)
folio_order = []

for line in corpus_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    m = FOLIO_LINE_RE.match(line.strip())
    if not m:
        continue
    fnum, side = int(m.group(1)), m.group(2)
    fid = f"{fnum}{side}"
    if get_scribe_id(fid) is None:
        continue
    if fid not in folio_stems:
        folio_order.append(fid)

    text = re.sub(r"<[^>]+>|\[[^\]]+\]|\{[^}]+\}|[!%*?$,]", " ", m.group(3))
    toks = [t for t in re.split(r"[.\s=+-]+", text) if t and not t.startswith("@")]
    for tok in toks:
        st = normalize_voynich(tok)
        if len(st) >= 4:
            folio_stems[fid][st] += 1

# Compute Document Frequency (DF) & filter to rare/specific stems (2 <= DF <= 15)
doc_freq = Counter()
for fid, counts in folio_stems.items():
    for st in counts:
        doc_freq[st] += 1

N_DOCS = len(folio_order)
idf = {st: math.log(N_DOCS / df) for st, df in doc_freq.items() if 2 <= df <= 15}

# Build L2-normalized TF-IDF vectors per folio side
tfidf_vecs = {}
for fid in folio_order:
    vec = {st: cnt * idf[st] for st, cnt in folio_stems[fid].items() if st in idf}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    tfidf_vecs[fid] = {st: v / norm for st, v in vec.items()}

def cosine_sim(f1: str, f2: str) -> tuple[float, list[str]]:
    v1, v2 = tfidf_vecs[f1], tfidf_vecs[f2]
    shared = [st for st in v1 if st in v2]
    score = sum(v1[st] * v2[st] for st in shared)
    shared.sort(key=lambda st: v1[st] * v2[st], reverse=True)
    return score, shared

# 1. Measure current physical adjacent-folio continuity vs. 1,000 random permutations
adj_scores = [cosine_sim(folio_order[i], folio_order[i + 1])[0] for i in range(len(folio_order) - 1)]
obs_adj_mean = sum(adj_scores) / len(adj_scores)

null_adj_means = []
shuffled = folio_order[:]
for _ in range(1000):
    random.shuffle(shuffled)
    s_scores = [cosine_sim(shuffled[i], shuffled[i + 1])[0] for i in range(len(shuffled) - 1)]
    null_adj_means.append(sum(s_scores) / len(s_scores))

null_mean = sum(null_adj_means) / len(null_adj_means)
null_std = math.sqrt(sum((x - null_mean) ** 2 for x in null_adj_means) / len(null_adj_means)) or 1e-6
adj_z = (obs_adj_mean - null_mean) / null_std

# 2. Find Top Non-Adjacent Reordering Candidates (gap >= 4 folio sides)
same_scribe_pairs = []
cross_scribe_pairs = []

for i in range(len(folio_order)):
    for j in range(i + 4, len(folio_order)):
        f1, f2 = folio_order[i], folio_order[j]
        score, shared = cosine_sim(f1, f2)
        if score <= 0.05 or len(shared) < 2:
            continue
        s1, s2 = get_scribe_id(f1), get_scribe_id(f2)
        entry = {
            "folio_a": f1,
            "folio_b": f2,
            "scribe_a": s1,
            "scribe_b": s2,
            "tfidf_sim": round(score, 4),
            "shared_rare_stems": shared[:6],
        }
        if s1 == s2:
            same_scribe_pairs.append(entry)
        else:
            cross_scribe_pairs.append(entry)

same_scribe_pairs.sort(key=lambda x: x["tfidf_sim"], reverse=True)
cross_scribe_pairs.sort(key=lambda x: x["tfidf_sim"], reverse=True)

# Build XC observation tuples for top rebinding candidates vs. current adjacent baseline
rebind_obs = [(0.92, 0.75, min(1.0, round(p["tfidf_sim"] * 2.5, 2))) for p in same_scribe_pairs[:25]]
current_obs = [(0.45, 0.35, min(1.0, round(s * 2.5, 2))) for s in adj_scores[:25]]

xc_code = [
    "# XC Probe #39: Quire-Level Bifolio Reordering & Rare-Stem TF-IDF Topology",
    "# Identifies non-adjacent folio pairs sharing rare stems (len >= 4, 2 <= DF <= 15)",
    "",
    f"continuity_stats = {{'obs_adj_mean': {round(obs_adj_mean, 5)}, 'null_mean': {round(null_mean, 5)}, 'null_std': {round(null_std, 5)}, 'z_score': {round(adj_z, 2)}}}",
    f"top_same_scribe_rebind = {repr(same_scribe_pairs[:20])}",
    f"top_cross_scribe_links = {repr(cross_scribe_pairs[:20])}",
    f"rebind_candidate_obs = {repr(rebind_obs)}",
    f"current_adjacent_obs = {repr(current_obs)}",
    "",
    "def evolve_topology(obs_list, label):",
    "    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)",
    "    for c_val, s_val, e_val in obs_list:",
    "        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)",
    "        τᵢⱼ(agent, tok, weight=0.3, type=label)",
    "        agent = Ouroboros(agent, target=tok)",
    "    return agent",
    "",
    "print('=== 1. CURRENT BINDING CONTINUITY VS. 1,000-TRIAL RANDOM SHUFFLE ===')",
    "print(f\"Adjacent Folio Mean Sim: {continuity_stats['obs_adj_mean']} vs. Shuffled Null: {continuity_stats['null_mean']} ± {continuity_stats['null_std']} | Z = {continuity_stats['z_score']:+.2f}\")",
    "",
    "print('\\n=== 2. XEMBRA TOPOLOGY STATE: REBINDING CANDIDATES VS. CURRENT ADJACENCY ===')",
    "print('Proposed Rebinding Pairs :', evolve_topology(rebind_candidate_obs, 'proposed_bifolio_rebind'))",
    "print('Current Adjacent Sequence:', evolve_topology(current_adjacent_obs, 'current_binding_order'))",
    "",
    "print('\\n=== 3. TOP SAME-SCRIBE BIFOLIO REORDERING CANDIDATES (DISPLACED LEAVES) ===')",
    "for p in top_same_scribe_rebind[:12]:",
    "    print(f\"  [S{p['scribe_a']}] {p['folio_a']:<5} <-> {p['folio_b']:<5} | TF-IDF Sim: {p['tfidf_sim']:.4f} | Shared Rare Stems: {p['shared_rare_stems']}\")",
    "",
    "print('\\n=== 4. TOP CROSS-SCRIBE NON-ADJACENT REFERENCE PAIRS (INDEX -> RECIPE) ===')",
    "for p in top_cross_scribe_links[:12]:",
    "    print(f\"  [S{p['scribe_a']}->{p['scribe_b']}] {p['folio_a']:<5} <-> {p['folio_b']:<5} | TF-IDF Sim: {p['tfidf_sim']:.4f} | Shared Rare Stems: {p['shared_rare_stems']}\")",
]

Path("voynich_bifolio_reordering_probe.xc").write_text("\n".join(xc_code), encoding="utf-8")
print("Built voynich_bifolio_reordering_probe.xc successfully.")

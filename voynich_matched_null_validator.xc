raw = read_text("data/voynich_raw.txt").splitlines()
herbal, jars_explicit, jars_broad, recipes, freq = set(), set(), set(), set(), {}

for ln in raw:
    s = ln.strip()
    if not s.startswith("<"):
        continue
    hdr, _, body = s.partition(">")
    digits = ""
    for ch in hdr[1:]:
        if ch.isdigit():
            digits += ch
        else:
            break
    if not digits:
        continue
    fo = int(digits)
    clean = "".join(" " if c in ".,!=*-+?()[]{}" else c for c in body)
    toks = clean.split()
    for t in toks:
        freq[t] = freq.get(t, 0) + 1
    if 1 <= fo <= 66:
        herbal.update(toks)
    elif 87 <= fo <= 102:
        if "[LABEL" in s or ".labels" in s or ".L" in hdr:
            jars_explicit.update(toks)
        if "[LABEL" in s or ".labels" in s or ".L" in hdr or len(toks) <= 6:
            jars_broad.update(toks)
    elif 103 <= fo <= 116:
        recipes.update(toks)

strata = {}
for w, c in freq.items():
    t = 0 if c == 1 else (1 if c <= 3 else (2 if c <= 10 else 3))
    strata.setdefault((len(w), t), []).append(w)

def run_perm(vocab_set, seed=42):
    vocab = sorted(vocab_set)
    obs_rec = sum(1 for w in vocab if w in recipes)
    obs_tri = sum(1 for w in vocab if w in recipes and w in herbal)
    rng = Random(seed)
    n_rec, n_tri = [], []
    for _ in range(1000):
        samp = [rng.choice(strata[(len(w), 0 if freq[w]==1 else (1 if freq[w]<=3 else (2 if freq[w]<=10 else 3)))]) for w in vocab]
        n_rec.append(sum(1 for w in samp if w in recipes))
        n_tri.append(sum(1 for w in samp if w in recipes and w in herbal))
    def st(obs, arr):
        mu = sum(arr) / len(arr)
        sd = sqrt(sum((x - mu) ** 2 for x in arr) / len(arr)) or 1e-9
        return (round(mu, 2), round(sd, 2), round((obs - mu) / sd, 2), round(sum(1 for x in arr if x >= obs) / len(arr), 4))
    return len(vocab), obs_rec, st(obs_rec, n_rec), obs_tri, st(obs_tri, n_tri)

print("=== LIVE RAW-DATA STRATIFIED PERMUTATION VALIDATOR (1,000 TRIALS, SEED=42) ===")
for label, vset in [("Explicit Jar Labels Only", jars_explicit), ("Broad Short Pharma Lines (<=6 toks)", jars_broad)]:
    n, o_r, s_r, o_t, s_t = run_perm(vset)
    print(f"[{label}] N={n} | Jar->Rec={o_r} Null={s_r} | 3-Way={o_t} Null={s_t}")
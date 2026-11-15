import json
import sys

lex = json.load(open("voynich_lexicon.json", encoding="utf-8"))["entries"]
codex = json.load(open("voynich_recipe_codex.json", encoding="utf-8"))["cards"]

def normalize_stem(w):
    s = w
    for p in ("4ok", "4oh", "4o", "og1", "g1", "8", "9", "2", "1", "o", "e", "g"):
        if s.startswith(p) and len(s) - len(p) >= 2:
            s = s[len(p):]
            break
    for suf in ("89", "am", "ay", "an", "oe", "ae", "9", "8", "7"):
        if s.endswith(suf) and len(s) - len(suf) >= 2:
            s = s[:-len(suf)]
            break
    return s.lower().replace("k", "h")

stem_index = {}
for w, info in sorted(lex.items(), key=lambda kv: -kv[1].get("recipe_count", 0)):
    st = normalize_stem(w)
    if len(st) >= 2 and st not in stem_index:
        stem_index[st] = (w, info["pos"], info["gloss"])

PREFIX_GLOSS = {"4o": "active/prepared", "o": "raw/item", "1": "measure-1", "2": "measure-2", "8": "and/next", "9": "variant"}
SUFFIX_GLOSS = {"89": "state/mixture", "9": "form", "am": "of/with", "an": "in/agent", "ay": "to/toward", "oe": "in/place", "ae": "essence"}

def resolve_token(w):
    if w in lex:
        return "EXACT", lex[w]["pos"], lex[w]["gloss"]
    st = normalize_stem(w)
    if st in stem_index:
        base_w, pos, gloss = stem_index[st]
        prep = "[prepared] " if w.startswith("4o") and "[prepared]" not in gloss else ""
        return "MORPH", f"{pos}*", f"{prep}{gloss} (via '{base_w}')"
    p_tag = next((PREFIX_GLOSS[p] for p in ("4o", "8", "9", "2", "1", "o") if w.startswith(p) and len(w) > len(p)+1), "bare")
    s_tag = next((SUFFIX_GLOSS[s] for s in ("89", "am", "ay", "an", "oe", "ae", "9") if w.endswith(s) and len(w) > len(s)+1), "stem")
    return "AFFIX", "GRAM", f"[{p_tag} + '{st}' + {s_tag}]"

def decode_tokens(tokens):
    semantic_hits = 0
    lines = []
    for w in tokens:
        tier, pos, gloss = resolve_token(w)
        if tier in ("EXACT", "MORPH"):
            semantic_hits += 1
        lines.append(f"  {w:<11} | {tier:<5} | {pos:<10} | {gloss}")
    cov = round(100.0 * semantic_hits / max(len(tokens), 1), 1)
    return cov, "\n".join(lines)

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "9"
    if arg.isdigit():
        cid = int(arg)
        card = next((c for c in codex if c["card_id"] == cid), codex[0])
        cov, body = decode_tokens(card["raw_text"].split())
        print(f"=== SEMANTIC DECODE: CARD #{card['card_id']} (Folio {card['folio']}) | Semantic Coverage: {cov}% ===")
        print(body)
    else:
        cov, body = decode_tokens(arg.split())
        print(f"=== SEMANTIC DECODE | Semantic Coverage: {cov}% ===")
        print(body)

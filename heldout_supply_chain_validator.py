"""Odd-folio train/freeze/even-folio test supply-chain validator.

Candidate rules use train only. Requested null strata use whole-corpus counts
and dominant hands (transductive matching, not a wholly blind holdout design).
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics

from scribe_map import get_scribe_id

PREFIXES = ('4o', 'o', 'y', '1', '2', '8', '9')
SUFFIXES = ('89', '79', 'am', 'an', 'oe', 'ay', '9', 'y')
RAW_PREFIXES = {'', 'o', '1', '2', '8'}
SECTIONS = ('Herbal', 'Jars', 'Recipes')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stem_token(token):
    stem, prefix = token, ''
    for p in PREFIXES:
        if stem.startswith(p) and len(stem)-len(p) >= 2:
            stem, prefix = stem[len(p):], p
            break
    for s in SUFFIXES:
        if stem.endswith(s) and len(stem)-len(s) >= 2:
            stem = stem[:-len(s)]
            break
    return stem, prefix


def parse(path):
    rows = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        m = re.match(r'^<f?(\d+)([rv]\d*)([^>]*)>(.*)$', line.strip())
        if not m:
            continue
        n = int(m[1])
        sec = 'Herbal' if 1 <= n <= 66 else 'Jars' if 87 <= n <= 102 else 'Recipes' if 103 <= n <= 116 else None
        if not sec:
            continue
        folio = str(n)+m[2]
        text = re.sub(r'\[[^\]]*\]|\{[^}]*\}|<[^>]*>', ' ', m[4])
        tokens = [t for t in re.split(r'[.,!=*+?()\[\]{}\s\-]+', text) if re.fullmatch(r'[A-Za-z0-9]+', t)]
        label = bool(re.search(r'\[LABEL\b', line, re.I) or re.search(r'\.labels?|\.L(?:[_.\d]|$)', m[3]) or len(tokens) <= 6)
        items = [(t, *stem_token(t)) for t in tokens if len(stem_token(t)[0]) >= 2]
        rows.append(dict(number=n, folio=folio, section=sec, label=label,
                         hand=str(get_scribe_id(folio) or 'unknown'), items=items))
    if not rows:
        raise ValueError('No corpus rows found')
    return rows


def vocab(rows):
    v = {s:set() for s in SECTIONS}
    for r in rows:
        if r['section'] != 'Jars' or r['label']:
            v[r['section']].update(s for _,s,_ in r['items'])
    return v


def develop(train):
    frequency = Counter(s for r in train for _,s,_ in r['items'])
    raw_labels = {s for r in train if r['section'] in ('Herbal','Jars') and r['label'] for _,s,p in r['items'] if p in RAW_PREFIXES}
    activated = {s for r in train if r['section']=='Recipes' for _,s,p in r['items'] if p=='4o'}
    v = vocab(train)
    eligible = {s for s,n in frequency.items() if n <= 150}
    a = raw_labels & activated & eligible
    b = v['Herbal'] & v['Jars'] & v['Recipes'] & eligible
    return {'A':sorted(a), 'B':sorted(b), 'C':sorted(a&b)}


def tier(n):
    return 0 if n==1 else 1 if n<=5 else 2 if n<=20 else 3 if n<=150 else 4


def hits(words, v):
    jr = sum(s in v['Jars'] and s in v['Recipes'] for s in words)
    full = sum(s in v['Herbal'] and s in v['Jars'] and s in v['Recipes'] for s in words)
    return jr, full


def main():
    root = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--corpus', type=Path, default=root/'data/voynich_raw.txt')
    p.add_argument('--output-dir', type=Path, default=root)
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = parse(args.corpus)
    train = [r for r in rows if r['number']%2==1]
    # STEP 1: all candidate development uses odd folios only.
    rules = develop(train)
    # STEP 2: serialize and hash frozen rules before forming test vocabularies.
    frozen = dict(protocol='odd train / even test; exact user-specified Rules A/B/C',
                  prefixes=PREFIXES, suffixes=SUFFIXES, min_stem_length=2,
                  max_train_frequency=150, rules=rules, seed=42, trials=1000,
                  corpus_sha256=sha(args.corpus), script_sha256=sha(__file__),
                  scribe_map_sha256=sha(root/'scribe_map.py'))
    frozen_bytes = json.dumps(frozen,sort_keys=True,separators=(',',':')).encode()
    frozen_hash = hashlib.sha256(frozen_bytes).hexdigest()
    rules = json.loads(frozen_bytes)['rules']
    # STEP 3: evaluate fixed candidates on even folios.
    test = [r for r in rows if r['number']%2==0]
    test_v = vocab(test)
    if any(not s for s in test_v.values()):
        raise ValueError('Test split missing a required section')
    # STEP 4: requested whole-corpus matched background; tie hands lexically.
    counts = Counter(); hands = defaultdict(Counter)
    for r in rows:
        for _,s,_ in r['items']:
            counts[s]+=1; hands[s][r['hand']]+=1
    dominant = {s:sorted(hands[s],key=lambda h:(-hands[s][h],h))[0] for s in counts}
    exact, fallback = defaultdict(list), defaultdict(list)
    for s in sorted(counts):
        k = (len(s),tier(counts[s]))
        exact[k+(dominant[s],)].append(s); fallback[k].append(s)
    rng = random.Random(42)
    results = {}; fallback_counts = {}
    for name, candidates in rules.items():
        pools = []
        fallback_counts[name] = 0
        for s in candidates:
            k = (len(s),tier(counts[s]))
            pool = exact[k+(dominant[s],)]
            if len(pool)<2:
                pool = fallback[k]; fallback_counts[name]+=1
            pools.append(pool)
        nulls = [[],[]]
        for _ in range(1000):
            # Independent replacement per candidate, as requested; duplicates
            # count as sampled candidate slots, not deduplicated vocabulary.
            sample = [rng.choice(pool) for pool in pools]
            for i,x in enumerate(hits(sample,test_v)):
                nulls[i].append(x)
        observed = hits(candidates,test_v)
        metrics = []
        for obs, ns in zip(observed,nulls):
            mu,sd = statistics.mean(ns),statistics.pstdev(ns)
            metrics.append(dict(observed=obs,mean=mu,sd=sd,z=(obs-mu)/sd if sd else None,
                                p=(1+sum(x>=obs for x in ns))/1001,null=ns))
        results[name] = dict(n=len(candidates),metrics=metrics,
                            bridges=sorted(s for s in candidates if hits([s],test_v)[1]))
    # Verify training rules are insensitive to arbitrary held-out contents.
    assert develop(train)==rules
    assert not {r['number'] for r in train}&{r['number'] for r in test}
    summary = []
    for label,rs in [('Train (odd)',train),('Test (even)',test)]:
        for sec in SECTIONS:
            subset = [r for r in rs if r['section']==sec and (sec!='Jars' or r['label'])]
            hand_counts = Counter()
            for r in subset:
                hand_counts[r['hand']]+=len(r['items'])
            summary.append((label,sec,len({r['number'] for r in subset}),sum(hand_counts.values()),dict(sorted(hand_counts.items()))))
    md = ['# Held-out Plant -> Jar -> Recipe Validator','',
          'Retrospective holdout on a previously explored manuscript. Candidate rules use odd folios only; even folios are evaluated after rules are frozen.','',
          '## Frozen protocol','',
          '- Train: odd physical folio numbers; test: even. Recto/verso and subpanels remain together.',
          '- Case-sensitive stems: remove at most one eligible prefix and one suffix, retaining at least two characters. ASCII alphanumeric tokens only; annotation text is removed.',
          '- Labels: explicit [LABEL], .labels/.label/.L annotations or lines of at most six cleaned tokens.',
          '- Rule A: raw/bare herbal-or-jar label stem plus 4o- recipe form in training; total train stem frequency <=150.',
          '- Rule B: training Herbal / Jar Labels / Recipes intersection; total train stem frequency <=150.',
          '- Rule C: A intersect B. No threshold tuning or best-rule selection after test scoring.',
          '- Null: 1,000 trials, Random(42), exact stem length / whole-corpus frequency tier / whole-corpus dominant hand. Frequency tiers: 1, 2-5, 6-20, 21-150, >150. Hand ties break lexically.',
          '- If an exact stratum has fewer than two stems, fall back to length/frequency only. Sample independently with replacement per candidate; sampled duplicate slots are counted. Candidates themselves remain eligible controls.',
          '- Held-out pages and section sizes remain fixed across null trials. Parity does not guarantee equal section sizes or hands.',
          '- Whole-corpus null matching uses held-out marginal information (transductive control); this is not fully blind training-only matching.',
          '- Six correlated rule/metric tests are exploratory; p-values below are unadjusted. No claim of translated ingredients, plant identities or causal supply-chain direction follows from overlap alone.',
          f'- Frozen protocol/candidate SHA-256: `{frozen_hash}`',
          f'- Corpus SHA-256: `{sha(args.corpus)}`',
          f'- Script SHA-256: `{sha(__file__)}`','',
          '## Held-out results','',
          '| Rule | Metric | Predicted | Observed | Hit rate | Null mean +/- SD | Z | Upper-tail p | Hand fallback |',
          '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for name,r in results.items():
        for metric,m in zip(('Jar -> Recipe','Full 3-way'),r['metrics']):
            z = f"{m['z']:+.3f}" if m['z'] is not None else 'undefined (zero SD)'
            rate = f"{100*m['observed']/r['n']:.2f}%" if r['n'] else 'N/A'
            md.append(f"| {name} | {metric} | {r['n']} | {m['observed']} | {rate} | {m['mean']:.3f} +/- {m['sd']:.3f} | {z} | {m['p']:.6f} | {fallback_counts[name]} |")
    md += ['', '## Split and scribal composition','', '| Split | Section | Physical folios | Stem tokens | Tokens by hand |','|---|---|---:|---:|---|']
    md += [f'| {a} | {b} | {c} | {d} | {e} |' for a,b,c,d,e in summary]
    md += ['', '## Held-out full three-way bridges','', 'Ranked by total held-out frequency; these are candidate spellings, not identified ingredients.','']
    test_counts = Counter(s for r in test for _,s,_ in r['items'])
    for name,r in results.items():
        top = sorted(r['bridges'],key=lambda s:(-test_counts[s],s))[:20]
        md += [f"- Rule {name}: " + (', '.join(f'`{s}` ({test_counts[s]})' for s in top) or 'none')]
    md += ['', '## Conclusion','']
    significant = [(name,i) for name,r in results.items() for i,m in enumerate(r['metrics']) if m['p']<0.05]
    md += [('At least one unadjusted comparison is below 0.05; assess all six comparisons and the stated design limits before interpretation.' if significant else 'No rule/metric comparison reaches an unadjusted upper-tail p < 0.05.'),'']
    (args.output_dir/'HELDOUT_SUPPLY_CHAIN.md').write_text('\n'.join(md),encoding='utf-8')
    plot(results,args.output_dir/'heldout_supply_chain.png')
    print('\n'.join(md[24:33]))
    print('Saved HELDOUT_SUPPLY_CHAIN.md and heldout_supply_chain.png')


def plot(results,path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':'#e8edf3',
        'axes.labelcolor':'#e8edf3','xtick.color':'#e8edf3','ytick.color':'#e8edf3',
        'axes.edgecolor':'#59616c','axes.titleweight':'bold'})
    fig,axes=plt.subplots(2,3,figsize=(15,8),facecolor='#0c1118')
    for col,(name,r) in enumerate(results.items()):
        for row,m in enumerate(r['metrics']):
            ax=axes[row,col];ax.set_facecolor('#161e29')
            lo=min(min(m['null']),m['observed']);hi=max(max(m['null']),m['observed'])
            ax.hist(m['null'],bins=[x-.5 for x in range(lo,hi+2)],color='#69afff',alpha=.8,label='Matched null (1,000 trials)')
            ax.axvline(m['observed'],color='#ffcc66',linewidth=2.5,label=f"Observed = {m['observed']}")
            z=f"{m['z']:+.2f}" if m['z'] is not None else 'undefined'
            ax.set_title(f"Rule {name} | {'Jar -> Recipe' if row==0 else 'Full 3-way'}\nZ={z}, p={m['p']:.4f}",color='#e8edf3',pad=12)
            ax.set_xlabel('Held-out matching stem slots');ax.set_ylabel('Null trials')
            ax.grid(axis='y',alpha=.12);ax.legend(fontsize=8,facecolor='#161e29',labelcolor='#e8edf3')
    fig.suptitle('Held-out supply-chain vocabulary | Odd train / Even test',fontsize=19,fontweight='bold',y=.98)
    fig.text(.5,.018,'Length + frequency + dominant-hand matching; held-out section sizes fixed | Exploratory, unadjusted p-values',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.045,1,.94))
    fig.savefig(path,dpi=200,facecolor=fig.get_facecolor(),metadata={'Software':'heldout_supply_chain_validator.py'})
    plt.close(fig)


if __name__=='__main__':
    main()

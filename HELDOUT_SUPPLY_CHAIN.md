# Held-out Plant -> Jar -> Recipe Validator

Retrospective holdout on a previously explored manuscript. Candidate rules use odd folios only; even folios are evaluated after rules are frozen.

## Frozen protocol

- Train: odd physical folio numbers; test: even. Recto/verso and subpanels remain together.
- Case-sensitive stems: remove at most one eligible prefix and one suffix, retaining at least two characters. ASCII alphanumeric tokens only; annotation text is removed.
- Labels: explicit [LABEL], .labels/.label/.L annotations or lines of at most six cleaned tokens.
- Rule A: raw/bare herbal-or-jar label stem plus 4o- recipe form in training; total train stem frequency <=150.
- Rule B: training Herbal / Jar Labels / Recipes intersection; total train stem frequency <=150.
- Rule C: A intersect B. No threshold tuning or best-rule selection after test scoring.
- Null: 1,000 trials, Random(42), exact stem length / whole-corpus frequency tier / whole-corpus dominant hand. Frequency tiers: 1, 2-5, 6-20, 21-150, >150. Hand ties break lexically.
- If an exact stratum has fewer than two stems, fall back to length/frequency only. Sample independently with replacement per candidate; sampled duplicate slots are counted. Candidates themselves remain eligible controls.
- Held-out pages and section sizes remain fixed across null trials. Parity does not guarantee equal section sizes or hands.
- Whole-corpus null matching uses held-out marginal information (transductive control); this is not fully blind training-only matching.
- Six correlated rule/metric tests are exploratory; p-values below are unadjusted. No claim of translated ingredients, plant identities or causal supply-chain direction follows from overlap alone.
- Frozen protocol/candidate SHA-256: `e604acdec3c0458221bc1420909545f5dd5e55aa84075a25f91ef23813dd7ddf`
- Corpus SHA-256: `0a96fbcf38e298689589dd8d4d4ba97d4856c2370a94602b83bb1cfd88dbaaae`
- Script SHA-256: `9933d420f46cde05f9919e72fa0fa6802a5254933f12ba365147ec13358df66a`

## Held-out results

| Rule | Metric | Predicted | Observed | Hit rate | Null mean +/- SD | Z | Upper-tail p | Hand fallback |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A | Jar -> Recipe | 60 | 25 | 41.67% | 22.306 +/- 3.089 | +0.872 | 0.242757 | 0 |
| A | Full 3-way | 60 | 24 | 40.00% | 22.138 +/- 3.067 | +0.607 | 0.322677 | 0 |
| B | Jar -> Recipe | 102 | 42 | 41.18% | 37.318 +/- 3.856 | +1.214 | 0.139860 | 1 |
| B | Full 3-way | 102 | 41 | 40.20% | 36.936 +/- 3.804 | +1.068 | 0.166833 | 1 |
| C | Jar -> Recipe | 37 | 21 | 56.76% | 17.538 +/- 2.398 | +1.444 | 0.106893 | 0 |
| C | Full 3-way | 37 | 20 | 54.05% | 17.439 +/- 2.376 | +1.078 | 0.196803 | 0 |

## Split and scribal composition

| Split | Section | Physical folios | Stem tokens | Tokens by hand |
|---|---|---:|---:|---|
| Train (odd) | Herbal | 30 | 5018 | {'1': 3519, '2': 1189, '3': 67, '5': 243} |
| Train (odd) | Jars | 6 | 381 | {'1': 381} |
| Train (odd) | Recipes | 6 | 5870 | {'3': 5465, '5': 405} |
| Test (even) | Herbal | 29 | 5814 | {'1': 4125, '2': 1275, '5': 414} |
| Test (even) | Jars | 6 | 291 | {'1': 291} |
| Test (even) | Recipes | 6 | 5229 | {'3': 5229} |

## Held-out full three-way bridges

Ranked by total held-out frequency; these are candidate spellings, not identified ingredients.

- Rule A: `h1` (156), `kc` (154), `k1` (125), `h9` (110), `ka` (94), `kae` (89), `K9` (87), `hoe` (87), `hco` (86), `az` (84), `C9` (81), `koe` (81), `H9` (75), `ko` (71), `ho` (64), `ch` (55), `1c` (42), `kco` (41), `k1o` (40), `Hc` (37)
- Rule B: `h1` (156), `kc` (154), `k1` (125), `h9` (110), `o8` (103), `coe` (99), `ka` (94), `kae` (89), `K9` (87), `hoe` (87), `hco` (86), `koe` (81), `1o` (78), `4o` (77), `H9` (75), `ko` (71), `ho` (64), `oh` (64), `ok` (49), `e1c` (45)
- Rule C: `h1` (156), `kc` (154), `k1` (125), `h9` (110), `ka` (94), `kae` (89), `K9` (87), `hoe` (87), `hco` (86), `koe` (81), `H9` (75), `ko` (71), `ho` (64), `1c` (42), `kco` (41), `k1o` (40), `Hc` (37), `7am` (36), `h1co` (9), `kco8` (5)

## Conclusion

No rule/metric comparison reaches an unadjusted upper-tail p < 0.05.

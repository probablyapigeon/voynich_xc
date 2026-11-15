# voynich_xc ? Structural Visibility, Pharmaceutical Supply Chains & Falsifiable Grammar Discovery

Built on **XC (XEMBRA Code)** (`probablyapigeon/xembra-xc`), this repository applies history-dependent state vectors $\Psi(c, p, r, s, \Phi, \mathcal{T}, E, d, a)$, directed coupling links $\tau_{ij}$, and `Ouroboros` evolution operators to uncover explicit, reproducible, and falsifiable structural laws inside the 15th-century **Voynich Manuscript**.

---

## Key Discoveries Surfaced by `.xc`

### 1. Macro-Structural & Codicological Probes
* **Sequential Order Sensitivity (`voynich_control.xc`):** Scrambling the opening 500 words causes suffix convergence $s$ to surge from `0.164` to `0.289` (+76%), proving strong sequential word-order dependencies.
* **Currier A -> B Phase Shift (`voynich_full_scan.xc` & `visualize_voynich.py`):** Scanning across offsets `0` to `25,000` maps a sharp phase jump around Offset `15,000` (Astronomical / Balneological sections), where $p$ drops to `0.186` and word-length energy $E$ peaks at `0.108`.
* **Gallows-Reset Falsification (`voynich_gallows_reset.xc`):** Forcing `Ouroboros` resets on tall gallows characters (`K, T, P, F`) degrades coherence $\Phi$ (`0.347` -> `0.326`), falsifying the cipher-reset hypothesis and showing gallows glyphs are integrated vocabulary.
* **Line-Boundary Grammar Locking (`voynich_lines.xc` & `voynich_linebreak_test.xc`):** Line-initial words carry +84% higher resonance $r$ (`0.178` vs. `0.137`) than mid-line words, and resetting at physical parchment line breaks increases temporal stability $\mathcal{T}$ (`0.161` -> `0.166`).
* **High-Energy Picture Labels (`voynich_labels_vs_paras.xc` & `voynich_top_labels.xc`):** Standalone 1-2 word picture labels exhibit +86% higher energy $E$ (`0.106` vs. `0.057`) than dense paragraph text, isolating un-diluted botanical, astronomical, and pharmaceutical root nouns.

### 2. Cross-Section Master Keys & Morphological Conjugation
* **4-Section Master Key `okoe` (`voynich_full_bridges.xc` & `voynich_okoe_grammar.xc`):**
  * The standalone label `okoe` bridges **Herbal Plants (`5v`)**, **Astronomy (`68v1`)**, **Bathing Pools (`77r/77v`)**, and **Apothecary Jars (`87v`)**.
  * In Herbal folios, `okoe` takes `-oe/-am` followers (`1oe`, `8am`; $c=0.817, s=0.271$); in Bathing folios, it shifts to `-9/-89` followers (`1c89`, `oj1c89`; $c=0.651, s=0.384$).
* **5-Section Root Stem Conjugation (`voynich_root_stems.xc`):**
  * Stems `ham`, `han`, `hae`, and `hC` take bare `o-` prefixes in Herbal/Zodiac (`oham`, `ohan`, `ohae`, `ohC9`) and lock onto `4o-` (`qo-`) prefixes in Bathing and Starred Recipes (`4oham`, `4ohan`, `4ohae`, `4ohC9`).
  * `han` surges 10x into `4ohan` inside Bathing (`226` hits) and Recipes (`202` hits), acting as a procedural action verb.
* **Procedural Recipe Clause Loop (`voynich_procedural_probe.xc` & `voynich_recipe_phrasebook.xc`):**
  * Exposes a recurring directional syntax chain: `[4ohan]` (Clause Opener / Verb) -> `[oe / 4oe]` (Prepositional Bridge) -> `[1c89]` (Clause Closer / Target).

### 3. Starred Recipe Cards & 3-Way Supply Chain (`1r-66v` -> `87r-102v` -> `103r-116v`)
* **359 Segmented Recipe Cards (`voynich_recipe_cards.xc`):** Extracts all `359` star-marked recipe paragraphs across folios `103r-116v` into a 4-slot grammar schema: `[1. OPENER] -> [2. INGREDIENT/PREP] -> [3. ACTION] -> [4. CLOSER]`.
* **312 Three-Way Verified Ingredients (`voynich_ingredient_index.xc`):** Cross-matches `[2. INGREDIENT/PREP]` nouns directly against **Herbal Plant labels (`1r-66v`)** and **Apothecary Jar labels (`87r-102v`)**:
  * **`oham` -> `4oham` Activation Pair:** Raw `oham` dominates Herbal (`55` hits, `24` label hits) and Apothecary jar labels (`88v`, `89r1`), while activated `4oham` surges into `75` Starred Recipe Cards.
  * **`1coe` (Jar Staple #1):** Appears `51` times in Apothecary Jars (`87r.15[LABEL]`, `87r.16[LABEL]`, `87v.12[LABEL]`) and feeds `42` Starred Recipe Cards.
  * **`4ohC9` (Universal Recipe Base):** Appears in `86` of `359` Starred Recipe Cards (~24% of all recipes), traced back to Herbal labels (`3r.14`, `17v.8`, `31r.3`) and Jar folios (`88r-89r2`).
* **Annotated Multi-Ingredient Recipe Reconstructions (`voynich_translated_cards.xc`):**
  * Reconstructs clause-by-clause provenance glossaries for high-density formulas including **Card #38 (`104r.14`, 11 verified 3-way ingredients)**, **Card #14 (`103r.42`, 10 verified 3-way ingredients)**, and **Card #206 (`111v.3`, 25 verified 3-way ingredients)**.
* **3D Supply-Chain Lattice (`visualize_supply_chain.py`):**
  * Maps the morphological phase transition in $(c, p, r)$ state space from the **Raw Botanical/Jar Cluster** ($c \approx 0.39\text{--}0.46, p \approx 0.15\text{--}0.50$) through the **Central Apothecary Hub** ($c = 0.65, p = 0.50, r = 0.95$) into the **Activated `4o-` Recipe Cluster** ($c \approx 0.88\text{--}0.90, p \approx 0.74\text{--}0.85$).

---

## Repository Contents & Quickstart

```bash
pip install -r requirements.txt

# 1. Core Structural & Cross-Section Probes
python xc_interpreter.py voynich_full_scan.xc
python xc_interpreter.py voynich_control.xc
python xc_interpreter.py voynich_gallows_reset.xc
python xc_interpreter.py voynich_lines.xc
python xc_interpreter.py voynich_linebreak_test.xc
python xc_interpreter.py voynich_labels_vs_paras.xc
python xc_interpreter.py voynich_top_labels.xc
python xc_interpreter.py voynich_full_bridges.xc
python xc_interpreter.py voynich_okoe_grammar.xc
python xc_interpreter.py voynich_root_stems.xc
python xc_interpreter.py voynich_procedural_probe.xc

# 2. Starred Recipes, Ingredient Index & Reconstructed Recipe Cards
python xc_interpreter.py voynich_recipe_phrasebook.xc
python xc_interpreter.py voynich_recipe_cards.xc
python xc_interpreter.py voynich_ingredient_index.xc
python xc_interpreter.py voynich_translated_cards.xc
python xc_interpreter.py voynich_codex_summary.xc  # Verifies all 359 cards in voynich_recipe_codex.md & .json

# 3. 3D XEMBRA Lattice Visualizers
python visualize_voynich.py
python visualize_bridges.py
python visualize_supply_chain.py
```

## New XC Structural, Reduplication & Proto-Recipe Probes (14 Scripts)

1. **`voynich_triad_inspector.xc`** ? Audits all `X X X` triplicate constructions in Starred Recipes (`103r?116v`).
2. **`voynich_clean_phrasebook.xc`** ? Extracts clean, readable recipe phrases from `voynich_recipe_codex.json`.
3. **`voynich_reduplication_probe.xc`** ? Maps zero-gap (`X X`) vs. bridged (`X + mid + X`) reduplications across Starred Recipes.
4. **`voynich_reduplication_cards.xc`** ? Links doubled stems directly to their `voynich_recipe_codex.json` recipe cards.
5. **`voynich_cluster_cards_inspector.xc`** ? Inspects dense reduplication clusters across `103r?116v`.
6. **`voynich_separator_audit.xc`** ? Audits 1?2 character connectors (`e`, `o`, `h`, `4o`, `1s`, `ae`, `ay`) inside `X + mid + X` triples.
7. **`voynich_cross_section_separator.xc`** ? Compares zero-gap vs. bridged reduplications across **Herbal (`1r?66v`)**, **Bathing (`75r?84v`)**, and **Starred Recipes (`103r?116v`)**, proving `X + 4o + X` raw-to-prepared stepping occurs in both Herbal (`56r.3`: `hC9 4o hC9`) and Recipes (`104v.33`: `ham 4o ham`).
8. **`voynich_herbal_1oe_probe.xc`** ? Analyzes all 19 occurrences of `1oe 1oe` (including `1oe 1oe 1oe` triplicates on `8v.8` and `47r.7`) in Herbal (`1r?66v`).
9. **`voynich_folio_56v_inspector.xc`** ? Line-by-line audit of Folio `56v` (`56v.1?56v.16`), uncovering three `1oe 1oe` chains and 8 verified 3-way recipe ingredients (`4okC9`, `4oh1c9`, `4ok1c9`, `hcc9`, `1oh9`, `h1oe`, `4oh1o`, `hccoe`).
10. **`voynich_herbal_currier_b_bridge.xc`** ? Ranks all 118 Herbal folios by `4o-` (`PREPARED`) recipe vocabulary overlap (`112/118` folios share `4o-` recipe tokens, led by `58v` and `66r`).
11. **`voynich_58v_66r_proto_recipes.xc`** ? Confirms Folios `58v` (`68.32%` recipe overlap) and `66r` (`56.41%` recipe overlap) as full-page proto-recipe instruction pages inside the Herbal section.
12. **`voynich_66r_margin_mapper.xc`** ? Maps `66r.labels_down_left_side` (`4ohae`, `sam`, `9hcoe`, `yay9`) into Starred Recipes and tests `66r.glyph_column` (`34` symbols, `0` line-initial matches).
13. **`voynich_glyph_column_scanner.xc`** ? Scans the entire manuscript for single-character key sequences, linking `66r.glyph_column` (`30/34` symbol overlap) directly to Folio `57v`'s concentric cipher rings.
14. **`voynich_57v_rings_inspector.xc`** ? Audits Folio `57v`'s four concentric rings (`o e 8 y ^ | h p g ? k y ? ? 9 E ?` 4-quadrant cycle) and bridges its outer text rings (`ohae ohae`, `4ohay`, `8am`, `sam`, `okae`) into `58v`, `66r`, and `103r?116v`.

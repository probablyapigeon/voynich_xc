# voynich_xc — Structural Visibility & Falsifiable Grammar Discovery on the Voynich Manuscript

Built on **XC (XEMBRA Code)** (`probablyapigeon/xembra-xc`), this repository applies history-dependent state vectors `Ψ(c, p, r, s, Φ, 𝒯, E, d, a)`, coupling links `τᵢⱼ`, and `Ouroboros` evolution operators to uncover explicit, reproducible, and falsifiable structural laws inside the 15th-century **Voynich Manuscript**.

## Key Discoveries Surfaced by `.xc`

1. **Sequential Order Sensitivity (`voynich_control.xc`)**
   - Scrambling the first 500 words causes suffix convergence `s` to surge from `0.164` to `0.289` (+76%), proving strong sequential word-order dependencies.
2. **Currier A → B Phase Shift (`voynich_full_scan.xc` & `visualize_voynich.py`)**
   - Scanning across offsets `0` to `25,000` maps a sharp state jump around Offset `15,000` (Astronomical / Balneological sections), where `p` drops to `0.186` and word-length energy `E` peaks at `0.108`.
3. **Falsification of Gallows-Reset Hypothesis (`voynich_gallows_reset.xc`)**
   - Forcing `Ouroboros` resets on tall gallows characters (`K, T, P, F`) degrades coherence `Φ` (`0.347 → 0.326`), proving gallows glyphs are integrated vocabulary rather than cipher-key resets.
4. **Line-Boundary Grammar Locking (`voynich_lines.xc` & `voynich_linebreak_test.xc`)**
   - Line-initial words carry +84% higher resonance `r` (`0.178` vs. `0.137`) than mid-line words, and resetting at physical parchment line breaks increases temporal stability `𝒯` (`0.161 → 0.166`).
5. **High-Energy Picture Labels (`voynich_labels_vs_paras.xc`)**
   - Standalone 1–2 word picture labels exhibit +86% higher energy `E` (`0.106` vs. `0.057`) than dense paragraph text, isolating un-diluted root nouns.
6. **4-Section Master Key `okoe` & Grammatical Partner Switch (`voynich_full_bridges.xc` & `voynich_okoe_grammar.xc`)**
   - The standalone label `okoe` bridges **Herbal Plants (`5v`)**, **Astronomy (`68v1`)**, **Bathing Pools (`77r/77v`)**, and **Apothecary Jars (`87v`)**.
   - In Herbal sections, `okoe` pairs with `-oe`/`-am` followers (`1oe`, `8am`; `c=0.817, s=0.271`); in Bathing sections, it switches to `-9`/`-89` followers (`1c89`, `oj1c89`; `c=0.651, s=0.384`).

## Reproduce All Experiments
```bash
pip install -r requirements.txt
python xc_interpreter.py voynich_full_scan.xc
python xc_interpreter.py voynich_gallows_reset.xc
python xc_interpreter.py voynich_lines.xc
python xc_interpreter.py voynich_labels_vs_paras.xc
python xc_interpreter.py voynich_full_bridges.xc
python xc_interpreter.py voynich_okoe_grammar.xc
python visualize_voynich.py
python visualize_bridges.py
```

# voynich_xc

Structural visibility and falsifiable state-trajectory experiments on the **Voynich Manuscript** using **XC (XEMBRA Code)**.

## Overview
Rather than guessing unverified phonetic translations, `voynich_xc` streams the Voynich transcription through history-dependent `Ψ(c, p, r, s, Φ, 𝒯, E, d, a)` state vectors and `Ouroboros` dynamics to make internal structural shifts explicit, reproducible, and falsifiable.

## Key Findings
1. **Sequential Order Sensitivity (Falsifiability Control):** Scrambling the first 500 words causes suffix convergence (`s`) to jump from `0.164` to `0.289` (+76%), demonstrating non-random sequential structure.
2. **Currier A → B Phase Shift:** Scanning across offsets `0` to `25,000` reveals a sharp state jump around Offset `15,000` (Astronomical / Balneological sections), where `p` drops to `0.186` and word-length energy `E` peaks at `0.108`.

## Quickstart
```bash
pip install -r requirements.txt
python xc_interpreter.py voynich_full_scan.xc
python xc_interpreter.py voynich_control.xc
python visualize_voynich.py
```

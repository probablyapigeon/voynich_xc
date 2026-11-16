# Step 4: 20-Window Human Prose vs. Autoregressive AI & Voynich Polarity Benchmark

![Human vs AI 20-Window Polarity](human_vs_llm_polarity.png)

Evaluates **20 independent non-overlapping 300-token windows per corpus** (`100` real windows + `3,000` Monte Carlo shuffle controls = `3,100` `Ouroboros` runs, `seed=42`) after cleaning `data/dna_hbb.txt` and `data/human_frankenstein.txt` to pure source sequences.

| Corpus | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Human Prose)` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Human Historical Prose (n=20)** | `20` | `-0.48 ± 1.32` | `+1.01 ± 1.19` | `-0.96 ± 2.01` | `+0.4398` |
| **2. Human Herbal Prose (n=20)** | `20` | `+0.14 ± 0.90` | `+0.18 ± 0.92` | `-0.49 ± 1.32` | `+0.2313` |
| **3. Live AI + Autoreg. (n=20)** | `20` | `-0.50 ± 1.35` | `+0.89 ± 1.53` | `-1.15 ± 2.18` | `+0.3326` |
| **4. Voynich Currier A (n=20)** | `20` | `-0.40 ± 1.51` | `+0.34 ± 1.40` | `-0.72 ± 2.07` | `+0.1569` |
| **5. Voynich Currier B (n=20)** | `20` | `-0.18 ± 1.05` | `+0.17 ± 1.10` | `+0.29 ± 1.04` | `-0.2373` |

# Step 4: 20-Window Human Prose vs. Autoregressive AI & Voynich Polarity Benchmark

![Human vs AI 20-Window Polarity](human_vs_llm_polarity.png)

Evaluates **20 independent non-overlapping 300-token windows per corpus** (`100` real windows + `3,000` Monte Carlo shuffle controls = `3,100` `Ouroboros` runs, `seed=42`) after cleaning `data/dna_hbb.txt` and `data/human_frankenstein.txt` to pure source sequences.

| Corpus | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Human Prose)` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Human Historical Prose (n=20)** | `9` | `-2.61 ± 1.89` | `+3.94 ± 2.25` | `-0.27 ± 0.61` | `+0.7689` |
| **2. Human Herbal Prose (n=20)** | `9` | `-3.01 ± 1.74` | `+4.78 ± 2.89` | `-0.36 ± 0.63` | `+0.7749` |
| **3. Live AI + Autoreg. (n=20)** | `20` | `-2.42 ± 1.79` | `+3.03 ± 1.95` | `-1.38 ± 2.89` | `+0.6675` |
| **4. Voynich Currier A (n=20)** | `20` | `-0.32 ± 1.62` | `+0.27 ± 1.47` | `-0.79 ± 2.09` | `+0.2041` |
| **5. Voynich Currier B (n=20)** | `20` | `-0.10 ± 0.96` | `+0.09 ± 1.04` | `+0.26 ± 0.95` | `+0.0281` |

# Multi-Window Cross-Domain Structural Stability Benchmark

Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`) to measure across-corpus variance and confidence intervals.

| Domain | Windows | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | Cosine to Voynich (`Mean ± SD`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1_DNA_Human_HBB** | `5` | `-7.01 ± 4.70` | `+6.02 ± 3.77` | `+0.69 ± 0.64` | `+0.2633 ± 0.1191` |
| **2_Music_Norbeck_ABC** | `1` | `+0.66 ± 0.00` | `+0.88 ± 0.00` | `-1.70 ± 0.00` | `+0.7691 ± 0.0000` |
| **3_Runtime_Opcodes** | `5` | `-0.61 ± 1.27` | `+7.19 ± 3.83` | `+0.66 ± 1.15` | `+0.1357 ± 0.4352` |
| **4_AI_Prose_Live_LLM** | `1` | `-1.87 ± 0.00` | `+1.81 ± 0.00` | `+0.38 ± 0.00` | `+0.1599 ± 0.0000` |
| **5_Human_Frankenstein** | `5` | `-1.29 ± 1.40` | `+3.48 ± 2.76` | `-1.15 ± 1.80` | `+0.4287 ± 0.3928` |
| **6_Voynich_MS408** | `10` | `-0.49 ± 1.74` | `+0.44 ± 1.59` | `-0.80 ± 3.13` | `+0.0344 ± 0.5055` |
| **7_Bengalese_Finch** | `10` | `-26.16 ± 5.51` | `+31.93 ± 10.90` | `+0.28 ± 2.22` | `+0.3241 ± 0.0821` |

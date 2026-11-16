# Multi-Window Cross-Domain Stability Benchmark (Split Currier A & Currier B)

Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`), separating **Currier A (`offset=0`)** from **Currier B (`offset=30000`)**.

| Domain | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1_DNA_Human_HBB** | `5` | `-6.98 ± 5.57` | `+5.75 ± 4.20` | `+0.71 ± 0.64` | `+0.4584` | `+0.5645` |
| **2_Music_Norbeck_ABC** | `1` | `+0.45 ± 0.00` | `+1.78 ± 0.00` | `-2.10 ± 0.00` | `+0.7075` | `-0.7592` |
| **3_Runtime_Opcodes** | `5` | `-0.79 ± 1.17` | `+6.86 ± 3.47` | `+0.75 ± 0.93` | `+0.2317` | `+0.3964` |
| **4_AI_Prose_Live_LLM** | `1` | `-2.26 ± 0.00` | `+1.80 ± 0.00` | `+0.40 ± 0.00` | `+0.4390` | `+0.6003` |
| **5_Human_Frankenstein** | `5` | `-1.43 ± 1.44` | `+4.73 ± 4.82` | `-1.11 ± 1.66` | `+0.4953` | `+0.0675` |
| **6A_Voynich_Currier_A** | `10` | `-0.51 ± 1.52` | `+0.52 ± 1.37` | `-0.47 ± 1.93` | `+0.1829` | `+0.1839` |
| **6B_Voynich_Currier_B** | `10` | `-0.34 ± 0.83` | `+0.35 ± 0.81` | `+0.45 ± 0.65` | `-0.2106` | `+0.4791` |
| **7_Bengalese_Finch** | `10` | `-29.10 ± 6.86` | `+39.76 ± 13.67` | `+0.25 ± 2.01` | `+0.5219` | `+0.4231` |

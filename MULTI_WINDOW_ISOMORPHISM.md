# Multi-Window Cross-Domain Stability Benchmark (Split Currier A & Currier B)

Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`), separating **Currier A (`offset=0`)** from **Currier B (`offset=30000`)**.

| Domain | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1_DNA_Human_HBB** | `5` | `-4.64 ± 0.67` | `+7.93 ± 1.72` | `+0.52 ± 0.43` | `+0.6101` | `+0.5875` |
| **2_Music_Norbeck_ABC** | `1` | `+0.45 ± 0.00` | `+1.78 ± 0.00` | `-2.10 ± 0.00` | `+0.5525` | `-0.7235` |
| **3_Runtime_Opcodes** | `5` | `-0.79 ± 1.17` | `+6.86 ± 3.47` | `+0.75 ± 0.93` | `+0.3630` | `+0.4012` |
| **4_AI_Prose_Live_LLM** | `1` | `-2.26 ± 0.00` | `+1.80 ± 0.00` | `+0.40 ± 0.00` | `+0.6231` | `+0.7297` |
| **5_Human_Frankenstein** | `10` | `-0.24 ± 0.96` | `+0.58 ± 0.81` | `-0.63 ± 1.94` | `+0.1277` | `+0.0605` |
| **6A_Voynich_Currier_A** | `10` | `-0.59 ± 1.50` | `+0.54 ± 1.33` | `-0.29 ± 1.82` | `+0.1881` | `+0.2424` |
| **6B_Voynich_Currier_B** | `10` | `-0.39 ± 0.94` | `+0.35 ± 0.97` | `+0.38 ± 0.64` | `-0.0082` | `+0.3359` |
| **7_Bengalese_Finch** | `10` | `-26.69 ± 10.20` | `+31.01 ± 12.09` | `+0.32 ± 2.25` | `+0.7065` | `+0.4897` |

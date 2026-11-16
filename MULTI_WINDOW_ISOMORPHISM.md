# Multi-Window Cross-Domain Stability Benchmark (Split Currier A & Currier B)

Evaluates up to **10 non-overlapping 300-token windows per domain** (`30` Monte Carlo shuffles per window, `seed=42`), separating **Currier A (`offset=0`)** from **Currier B (`offset=30000`)**.

| Domain | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1_DNA_Human_HBB** | `5` | `-4.18 ± 0.91` | `+6.95 ± 1.17` | `+0.33 ± 0.47` | `+0.4362` | `+0.5972` |
| **2_Music_Norbeck_ABC** | `1` | `+0.45 ± 0.00` | `+1.04 ± 0.00` | `-1.64 ± 0.00` | `+0.7167` | `-0.7533` |
| **3_Runtime_Opcodes** | `5` | `-0.61 ± 1.26` | `+6.77 ± 3.43` | `+0.85 ± 1.13` | `+0.2250` | `+0.3915` |
| **4_AI_Prose_Live_LLM** | `1` | `-2.06 ± 0.00` | `+1.65 ± 0.00` | `+0.19 ± 0.00` | `+0.4142` | `+0.6493` |
| **5_Human_Frankenstein** | `10` | `+0.15 ± 0.98` | `-0.06 ± 1.00` | `-0.14 ± 0.87` | `+0.0402` | `-0.0888` |
| **6A_Voynich_Currier_A** | `10` | `-0.34 ± 1.58` | `+0.32 ± 1.42` | `-0.31 ± 1.68` | `+0.0891` | `+0.2184` |
| **6B_Voynich_Currier_B** | `10` | `-0.45 ± 0.79` | `+0.45 ± 0.75` | `+0.42 ± 0.62` | `-0.0642` | `+0.4374` |
| **7_Bengalese_Finch** | `10` | `-29.25 ± 7.15` | `+35.40 ± 10.66` | `+0.26 ± 2.06` | `+0.5293` | `+0.5351` |

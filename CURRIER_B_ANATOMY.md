# Currier B Anatomy Probe: What Generative Mechanism Matches Currier B?

![Currier B Anatomy Comparison](currier_b_anatomy.png)

Tests four candidate generative mechanisms against actual **Voynich Currier B** across **10 independent 300-token windows** (`30` Monte Carlo shuffles/window, `seed=42`).

| Mechanism | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Vowel-Dropped Abjad** | `0` | `+nan ± nan` | `+nan ± nan` | `+nan ± nan` | `+nan` |
| **2. Combinatorial Grille (AxBxC)** | `10` | `+0.38 ± 1.46` | `-0.32 ± 1.31` | `-0.99 ± 2.07` | `-0.1282` |
| **3. Apothecary Ledger (4-Slot)** | `10` | `-1.03 ± 0.50` | `+6.91 ± 1.75` | `-0.35 ± 1.10` | `+0.3320` |
| **4. Currier B Affix-Stripped** | `10` | `-0.67 ± 1.31` | `+0.66 ± 1.26` | `+0.39 ± 0.78` | `+0.3277` |
| **5. Voynich Currier B (Actual)** | `10` | `-0.48 ± 1.01` | `+0.49 ± 0.99` | `+0.46 ± 0.57` | `+0.5158` |

# Currier B Anatomy Probe: Combined Apothecary Ledger + Abjad Shorthand

![Currier B Anatomy Comparison](currier_b_anatomy.png)

Tests **Apothecary Ledger + Vowel-Dropped Abjad Shorthand** (with and without morphological affix tags) against actual **Voynich Currier B** across **10 independent 300-token windows** (`30` Monte Carlo shuffles/window, `seed=42`).

| Mechanism | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Vowel-Dropped Abjad** | `10` | `-5.41 ± 3.92` | `+6.60 ± 4.50` | `-0.68 ± 1.73` | `+0.0683` |
| **2. Apothecary Ledger (4-Slot)** | `10` | `-1.02 ± 0.51` | `+5.15 ± 2.02` | `-0.01 ± 0.90` | `+0.2818` |
| **3. Ledger + Abjad Combined** | `10` | `-1.42 ± 1.34` | `+4.72 ± 2.34` | `-0.29 ± 0.75` | `+0.1090` |
| **4. Ledger + Abjad + Affixes** | `10` | `-0.35 ± 0.46` | `+0.82 ± 0.65` | `-0.30 ± 0.76` | `+0.0191` |
| **5. Currier B Affix-Stripped** | `10` | `-0.60 ± 1.17` | `+0.57 ± 1.11` | `+0.37 ± 0.84` | `+0.2076` |
| **6. Voynich Currier B (Actual)** | `10` | `-0.37 ± 0.91` | `+0.32 ± 0.99` | `+0.49 ± 0.62` | `+0.4584` |

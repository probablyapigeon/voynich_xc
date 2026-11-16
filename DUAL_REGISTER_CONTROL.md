# Step 2: Single-Source Dual-Register Control (Historical Herbal vs. 14th-Century Recipes)

![Dual-Register Polarity Control](dual_register_polarity.png)

Tests whether authentic historical **descriptive herbal entries** (*Culpeper's Complete Herbal*, PG #49513) vs. **procedural compounding recipes** (*The Forme of Cury*, c. 1390, PG #8102) reproduce the same $Z_\Phi$ polarity flip seen between **Voynich Currier A** and **Voynich Currier B** across **10 non-overlapping 300-token windows** (`30` Monte Carlo shuffles/window, `seed=42`).

| Corpus | Wins | $Z_c$ (`Mean ± SD`) | $Z_s$ (`Mean ± SD`) | $Z_\Phi$ (`Mean ± SD`) | `cos(Currier A)` | `cos(Currier B)` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Historical Herbal (Desc.)** | `10` | `-3.63 ± 2.93` | `+4.90 ± 3.40` | `-0.57 ± 1.75` | `+0.4162` | `+0.2200` |
| **2. 14th-C. Recipes (Proc.)** | `10` | `-3.30 ± 2.62` | `+4.29 ± 3.00` | `-0.55 ± 1.73` | `+0.3911` | `+0.2198` |
| **3. Voynich Currier A (Herbal)** | `10` | `-0.39 ± 1.51` | `+0.39 ± 1.43` | `-0.46 ± 1.93` | `+0.1212` | `+0.1728` |
| **4. Voynich Currier B (Recipe)** | `10` | `-0.48 ± 1.01` | `+0.49 ± 0.99` | `+0.46 ± 0.57` | `-0.2350` | `+0.5158` |

# Voynich Currier A vs. Currier B Dialect Split & Morphological Ablation (`.xc` Benchmark)

Evaluates 300-token streams from **Currier A (`0..300`, Herbal)**, **Currier B (`30000..30300`, Quire 13 Balneological)**, and **Currier B (`40245..40545`, Quire 20 Starred Recipes)** across 50 Monte Carlo random-shuffle surrogates per condition alongside all 7 baseline domains.

## 1. Three-Stage Morphological Ablation (`Surface` $\rightarrow$ `Stem` $\rightarrow$ `Gallows Core`)

| Condition | $\Psi(c)$ | $\Psi(\Phi)$ | $Z_c$ (Recurrence) | $Z_s$ (Transition) | $Z_\Phi$ (Coherence) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **SURF_CA_Herbal_00000** | `0.848` | `0.254` | `+3.54` | `-2.74` | `-4.36` |
| **SURF_CB_Quire13_30000** | `0.805` | `0.275` | `+0.02` | `-0.59` | `+1.77` |
| **SURF_CB_Tail_40245** | `0.822` | `0.273` | `+0.36` | `-0.62` | `+1.37` |
| **STEM_CA_Herbal_00000** | `0.877` | `0.230` | `+3.43` | `-2.84` | `-4.38` |
| **STEM_CB_Quire13_30000** | `0.815` | `0.269` | `-0.34` | `-0.38` | `+2.04` |
| **STEM_CB_Tail_40245** | `0.848` | `0.255` | `+0.96` | `-0.84` | `-0.21` |
| **GALLOWS_CA_Herbal_00000** | `0.880` | `0.227` | `+3.04` | `-2.68` | `-3.20` |
| **GALLOWS_CB_Quire13_30000** | `0.840` | `0.252` | `+0.23` | `-0.64` | `+0.78` |
| **GALLOWS_CB_Tail_40245** | `0.852` | `0.251` | `+0.62` | `-0.71` | `+0.37` |

## 2. Attractor Collapse Trajectory ($\cos\theta$)

| Dialect Pair | Surface $\cos\theta$ | Stem-Normalized $\cos\theta$ | Gallows-Core $\cos\theta$ |
| :--- | :---: | :---: | :---: |
| **CA (00000) <-> CB Tail (40245)** | `-0.6090` | `+0.5755` | `-0.0390` |
| **CA (00000) <-> CB Q13  (30000)** | `-0.8165` | `-0.8758` | `-0.5460` |
| **CB Q13 (30000) <-> CB Tail (40245)** | `+0.9154` | `-0.1880` | `+0.7650` |

## 3. Gallows-Core Cross-Domain Isomorphism ($\cos\theta$)

| Baseline Domain | Gallows Currier A (`00000`) | Gallows Currier B Q13 (`30000`) | Gallows Currier B Tail (`40245`) |
| :--- | :---: | :---: | :---: |
| **1_DNA_Human_HBB** | `-0.4471` | `-0.4705` | `-0.6668` |
| **2_Music_Norbeck_ABC** | `+0.9221` | `-0.5845` | `+0.0383` |
| **3_Runtime_Opcodes** | `+0.0693` | `-0.5882` | `-0.3065` |
| **4_AI_Prose_Live_LLM** | `-0.0081` | `-0.8098` | `-0.9257` |
| **5_Human_Frankenstein** | `+0.9653` | `-0.7305` | `-0.2390` |
| **6_Voynich_MS408** | `+0.9937` | `-0.6326` | `-0.1337` |
| **7_Bengalese_Finch** | `+0.9839` | `-0.5653` | `-0.1166` |

# Voynich Manuscript Full-Corpus Dialect Classification Benchmark (`1r`–`116v`)

Evaluates `72` paleographically assigned folios (`>= 150` tokens each; excluding `6` unassigned Astronomical/Zodiac folios) against **Prescott Currier's** Language A / Language B ground truth.

## 1. Classifier Performance Comparison

| Classifier Architecture | Accuracy | Precision (CB) | Recall (CB) | F1 Score | Confusion (`TP / FP / FN / TN`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Single-Prototype Surface (`CB_Q20`)** | `65.3%` | `94.1%` | `58.2%` | `71.9%` | `32 / 2 / 23 / 15` |
| **2. Dual-Prototype Surface (`CB_Q13 + CB_Q20`)** | `68.1%` | `94.4%` | `61.8%` | `74.7%` | `34 / 2 / 21 / 15` |
| **3. Dual-Prototype Hybrid (`Surface + Gallows`)** | `52.8%` | `81.8%` | `49.1%` | `61.4%` | `27 / 6 / 28 / 11` |

> **Class-Balance Note:** Because 55 of the 72 assigned folios (76.4%) are paleographically Currier B, a trivial majority-class baseline achieves 76.4% raw accuracy. The .xc dual-prototype model operates as a **high-precision selective filter** (94.4% Currier B precision, 88.2% Currier A specificity).

# Quire 13 (`75r`–`84v`) Top-of-Page vs. Bottom-of-Page vs. Full-Folio Ablation

Tests whether Quire 13 recto folios flip from **Currier A** to **Currier B** when top-of-page nymph captions (`[:300]`) are replaced by bottom-of-page prose (`[-300:]`) or full-folio sequences.

| Folio | Tokens | Top-300 Regime | Bottom-300 Regime | Full-Folio Regime | Bottom $\cos(\text{CB})$ | Full $\cos(\text{CB})$ | Full $Z_\Phi$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `75r` | 429 | Currier A | **Currier A** | **Currier A** | `-0.6939` | `-0.5965` | `-1.61` |
| `75v` | 373 | Currier B | **Currier B** | **Currier A** | `-0.2613` | `-0.4966` | `+0.10` |
| `76r` | 581 | Currier A | **Currier A** | **Currier B** | `-0.3127` | `+0.9012` | `+0.41` |
| `76v` | 411 | Currier B | **Currier B** | **Currier A** | `+0.5277` | `+0.2698` | `-0.22` |
| `77r` | 341 | Currier B | **Currier A** | **Currier A** | `-0.5415` | `-0.5520` | `-1.66` |
| `77v` | 362 | Currier B | **Currier B** | **Currier B** | `+0.7148` | `+0.9039` | `+1.28` |
| `78r` | 308 | Currier A | **Currier A** | **Currier A** | `-0.9608` | `-0.9167` | `-1.22` |
| `78v` | 311 | Currier A | **Currier B** | **Currier B** | `+0.2165` | `+0.3718` | `+0.67` |
| `79r` | 413 | Currier B | **Currier A** | **Currier A** | `-0.7517` | `-0.7049` | `-0.69` |
| `79v` | 383 | Currier B | **Currier A** | **Currier A** | `+0.1106` | `+0.1688` | `-0.62` |
| `80r` | 470 | Currier A | **Currier A** | **Currier A** | `-0.5750` | `-0.3649` | `-1.19` |
| `80v` | 407 | Currier A | **Currier B** | **Currier B** | `+0.9692` | `+0.9315` | `+1.21` |
| `81r` | 221 | Currier A | **Currier A** | **Currier A** | `-0.1611` | `-0.1611` | `-0.65` |
| `81v` | 277 | Currier A | **Currier A** | **Currier A** | `-0.8595` | `-0.8595` | `-0.88` |
| `82r` | 307 | Currier B | **Currier A** | **Currier A** | `+0.0967` | `+0.0049` | `-0.93` |
| `82v` | 335 | Currier B | **Currier B** | **Currier B** | `+0.2004` | `+0.1673` | `+0.84` |
| `83r` | 361 | Currier A | **Currier A** | **Currier A** | `-0.1921` | `+0.1395` | `-0.32` |
| `83v` | 274 | Currier A | **Currier A** | **Currier A** | `-0.5052` | `-0.5052` | `-2.44` |
| `84r` | 394 | Currier B | **Currier A** | **Currier A** | `-0.8269` | `-0.9073` | `-1.56` |
| `84v` | 359 | Currier B | **Currier A** | **Currier A** | `-0.4194` | `-0.5250` | `-0.25` |

**Currier B Recall across Quire 13:** `Top-300` = **10/20** (`50%`) $\rightarrow$ `Bottom-300` = **6/20** (`30%`) $\rightarrow$ `Full-Folio` = **5/20** (`25%`).


# Voynich Manuscript Sliding-Window Dialect Sweep (`.xc` Ouroboros)

Evaluates `41` sliding windows (`WIN_SIZE=300`, `STEP=1000`) across `40,545` tokens in `data/voynich_clean.txt`, measuring cosine alignment against **Currier A** (`0..300`) and **Currier B** (`-300:`) Monte Carlo Z-score attractors.

## 1. Detected Phase Transitions

- **Token ~02000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.9383`, `cos B = +0.8037`)
- **Token ~03000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.5772`, `cos B = -0.9946`)
- **Token ~04000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.2740`, `cos B = +0.8193`)
- **Token ~07000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = -0.2787`, `cos B = -0.5321`)
- **Token ~10000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.2118`, `cos B = +0.9014`)
- **Token ~12000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.3913`, `cos B = -0.9605`)
- **Token ~13000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.2035`, `cos B = +0.8837`)
- **Token ~16000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.8698`, `cos B = -0.9079`)
- **Token ~17000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.8563`, `cos B = +0.1356`)
- **Token ~18000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.5849`, `cos B = -0.9862`)
- **Token ~22000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = +0.2806`, `cos B = +0.5564`)
- **Token ~23000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.5642`, `cos B = -0.6463`)
- **Token ~27000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.8361`, `cos B = +0.1561`)
- **Token ~28000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.8528`, `cos B = -0.1252`)
- **Token ~29000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.5702`, `cos B = +0.5765`)
- **Token ~31000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.6358`, `cos B = -0.9885`)
- **Token ~32000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.4410`, `cos B = -0.2915`)
- **Token ~33000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.9243`, `cos B = -0.7833`)
- **Token ~35000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.5500`, `cos B = +0.7929`)
- **Token ~36000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.4440`, `cos B = -0.8671`)
- **Token ~37000:** `Currier A` $\rightarrow$ `Currier B` (`cos A = -0.7508`, `cos B = -0.0300`)
- **Token ~39000:** `Currier B` $\rightarrow$ `Currier A` (`cos A = +0.7000`, `cos B = -0.8287`)

## 2. Full Manuscript Trajectory

| Token Span | $\cos(\text{Currier A})$ | $\cos(\text{Currier B})$ | $Z_c$ | $Z_s$ | $Z_\Phi$ | Dominant Regime | Sample Tokens |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `00000..00300` | `+0.9993` | `-0.5886` | `+3.58` | `-3.03` | `-4.18` | **Currier A** | `fa19s 9 hae ay Akam` |
| `01000..01300` | `+0.9012` | `-0.2451` | `+1.91` | `-1.32` | `-1.09` | **Currier A** | `1oy K9 4oKoe (o8am K9` |
| `02000..02300` | `-0.9383` | `+0.8037` | `-1.06` | `+0.92` | `+1.79` | **Currier B** | `sok19 h19 ohoyoy9 hoaiy 1kom` |
| `03000..03300` | `+0.5772` | `-0.9946` | `-0.48` | `+0.63` | `-1.25` | **Currier A** | `8am 4okoe 9koe 8aM 9k1` |
| `04000..04300` | `-0.2740` | `+0.8193` | `+0.18` | `+0.24` | `+0.72` | **Currier B** | `8am 4og1c9 ok1c9 4of1oy sos` |
| `05000..05300` | `-0.6210` | `+0.5888` | `-1.06` | `+1.51` | `+0.49` | **Currier B** | `9ham 1Ch5cc9 91chccoy 1coy oy` |
| `06000..06300` | `-0.8687` | `+0.1719` | `-2.30` | `+2.07` | `+0.98` | **Currier B** | `1hoe okoe9 %oy 2oe 4oh19` |
| `07000..07300` | `-0.2787` | `-0.5321` | `-1.54` | `+0.68` | `-0.04` | **Currier A** | `1och9 8å 8 an 8ae` |
| `08000..08300` | `-0.1075` | `-0.6997` | `-1.66` | `+1.31` | `-0.60` | **Currier A** | `ok2caekay 2oeh29 4ohay 1coe ohae` |
| `09000..09300` | `+0.8279` | `-0.9400` | `+0.24` | `+0.22` | `-2.29` | **Currier A** | `(h1A8am (hae8 91os ay 1H9` |
| `10000..10300` | `-0.2118` | `+0.9014` | `+1.25` | `-1.32` | `+0.83` | **Currier B** | `h1cc9 s am 1oh1oe 1oy` |
| `11000..11300` | `-0.8234` | `+0.1833` | `-1.77` | `+1.62` | `+0.66` | **Currier B** | `4ohcos ohae ay oho s` |
| `12000..12300` | `+0.3913` | `-0.9605` | `-1.14` | `+0.74` | `-1.32` | **Currier A** | `soeaz Fc9 soeae 8ae9 ohcoe` |
| `13000..13300` | `-0.2035` | `+0.8837` | `+1.07` | `-0.82` | `+0.92` | **Currier B** | `8ae okcc9 okC9 o1o9h ohco` |
| `14000..14300` | `-0.9617` | `+0.5405` | `-1.51` | `+1.57` | `+1.12` | **Currier B** | `ay9 okccay9 okaz 69 ohaiy1ap` |
| `15000..15300` | `-0.4545` | `+0.9126` | `+0.12` | `+0.21` | `+1.19` | **Currier B** | `e1c79 yap 8an oe 2coe` |
| `16000..16300` | `+0.8698` | `-0.9079` | `+0.36` | `-0.16` | `-1.50` | **Currier A** | `1c9 e5 8am 1c9 e1c89` |
| `17000..17300` | `-0.8563` | `+0.1356` | `-3.34` | `+1.80` | `+1.80` | **Currier B** | `eap soy 2coe 179 4ohC79` |
| `18000..18300` | `+0.5849` | `-0.9862` | `-0.79` | `+1.12` | `-2.10` | **Currier A** | `1c79 k2c9 8379 ok1ay 2ch` |
| `19000..19300` | `-0.0078` | `-0.7131` | `-0.40` | `+0.27` | `-0.25` | **Currier A** | `k9 koy 1c9h9 k okoe` |
| `20000..20300` | `-0.3104` | `-0.5482` | `-1.60` | `+1.61` | `-0.03` | **Currier A** | `1kc89kay 3oe 4ch19 9ham oehan` |
| `21000..21300` | `+0.7518` | `+0.0402` | `+2.65` | `-1.70` | `-1.17` | **Currier A** | `e1c79 8oe2c8 4oh19 sam 1ch9` |
| `22000..22300` | `+0.2806` | `+0.5564` | `+1.25` | `-0.75` | `+0.20` | **Currier B** | `ohc9 ohc39 oe19 4ohan oe` |
| `23000..23300` | `+0.5642` | `-0.6463` | `-0.66` | `+1.42` | `-0.90` | **Currier A** | `ae hay ap 9kam 9kaz` |
| `24000..24300` | `+0.9736` | `-0.6570` | `+2.62` | `-2.47` | `-2.68` | **Currier A** | `okay okcs Aham 7ae ae` |
| `25000..25300` | `+0.9554` | `-0.7733` | `+0.81` | `-0.48` | `-1.28` | **Currier A** | `e189 4ohco y an koehCo8am` |
| `26000..26300` | `+0.5398` | `-0.9156` | `+0.06` | `-0.15` | `-0.84` | **Currier A** | `4oH9 1oe oe saes soe` |
| `27000..27300` | `-0.8361` | `+0.1561` | `-1.76` | `+1.57` | `+0.55` | **Currier B** | `8kco8om sayo 4o1cs 9 1cop` |
| `28000..28300` | `+0.8528` | `-0.1252` | `+2.04` | `-1.82` | `-0.83` | **Currier A** | `ohco8 ÷c9 7An oe 1co` |
| `29000..29300` | `-0.5702` | `+0.5765` | `+0.44` | `-1.30` | `+0.98` | **Currier B** | `ohc89 4oh9 j1c79 ohae9 4ohC79` |
| `30000..30300` | `-0.7475` | `+0.9488` | `+0.40` | `-0.93` | `+2.12` | **Currier B** | `h2c89 ko am 18ay okay` |
| `31000..31300` | `+0.6358` | `-0.9885` | `-0.43` | `+0.62` | `-1.31` | **Currier A** | `oe y am ohC89 oehcco89` |
| `32000..32300` | `-0.4410` | `-0.2915` | `-1.31` | `+1.62` | `-0.10` | **Currier B** | `yam 19 y o89 1eay` |
| `33000..33300` | `+0.9243` | `-0.7833` | `+1.94` | `-1.92` | `-2.36` | **Currier A** | `1cc9 oe1coe ham okaz ohae` |
| `34000..34300` | `+0.2868` | `+0.0119` | `+0.33` | `-0.52` | `-0.12` | **Currier A** | `8ae 4oham okae oe 2c89` |
| `35000..35300` | `-0.5500` | `+0.7929` | `+0.42` | `-0.53` | `+0.53` | **Currier B** | `1C89 4ohC9 4ohc79 1l9 ok2c89` |
| `36000..36300` | `+0.4440` | `-0.8671` | `-0.05` | `+0.13` | `-0.38` | **Currier A** | `kay oe og1c89 4okay okay` |
| `37000..37300` | `-0.7508` | `-0.0300` | `-0.87` | `+0.56` | `+0.43` | **Currier B** | `okcc89 4okcc9 4okan 1K8 9` |
| `38000..38300` | `-0.6364` | `-0.1653` | `-2.20` | `+1.90` | `+0.25` | **Currier B** | `gAesaz9 okco 4ohC7( 4oham ohae` |
| `39000..39300` | `+0.7000` | `-0.8287` | `-0.01` | `+0.16` | `-0.30` | **Currier A** | `ap 81C9 oe 1co7aM 4ohay` |
| `40000..40300` | `+0.0934` | `-0.3964` | `-0.41` | `+0.71` | `-0.36` | **Currier A** | `K9 e2c89 okcoy 5c9 4o` |

from xembra_core import PsiVector, connect, Ouroboros
from xembra_visualizer import visualize_lattice

words = open('data/voynich_clean.txt', encoding='utf-8', errors='ignore').read().split()
offsets = list(range(0, min(len(words), 30000), 5000))
nodes = []

for off in offsets:
    reader = PsiVector(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, T=0.5, E=0.5, d=0.5, a=0.5)
    for w in words[off:off+500]:
        c_val = 0.9 if w.startswith(('8','4o','2','o')) else 0.2
        s_val = 0.9 if w.endswith(('9','am','ay','89')) else 0.2
        e_val = round(min(len(w)/10.0, 1.0), 3)
        tok = PsiVector(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, T=0.4, E=e_val, d=0.3, a=0.5)
        connect(reader, tok, weight=0.25, type='scan')
        reader = Ouroboros(reader, target=tok)
    nodes.append(reader)

# Connect consecutive manuscript sections with τᵢⱼ links to show structural drift
for i in range(len(nodes) - 1):
    connect(nodes[i], nodes[i+1], weight=0.85, type='manuscript_flow')

visualize_lattice(nodes, title='Voynich Manuscript Structural Trajectory (Offsets 0 -> 25,000)')

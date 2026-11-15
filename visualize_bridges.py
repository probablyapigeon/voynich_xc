from xembra_core import PsiVector, connect
from xembra_visualizer import visualize_lattice

bridges = [(4, 5, 'okoe', ['Apothecary', 'Bathing', 'Herbal', 'Zodiac']), (3, 6, 'oham', ['Bathing', 'Herbal', 'Zodiac']), (3, 4, 'ohay', ['Herbal', 'Rosettes', 'Zodiac']), (3, 3, '2o8am', ['Apothecary', 'Herbal', 'Rosettes']), (2, 4, 'ok189', ['Bathing', 'Zodiac']), (2, 3, 'okam', ['Bathing', 'Herbal']), (2, 3, '8ay9', ['Herbal', 'Zodiac']), (2, 3, '1coe', ['Apothecary', 'Herbal']), (2, 2, 'okcoe', ['Apothecary', 'Zodiac']), (2, 2, 'okay', ['Apothecary', 'Zodiac']), (2, 2, 'okae9', ['Bathing', 'Zodiac']), (2, 2, 'ok19', ['Rosettes', 'Zodiac']), (2, 2, 'oh1oe', ['Herbal', 'Zodiac']), (2, 2, 'oh19', ['Herbal', 'Rosettes']), (2, 2, '8ae9', ['Rosettes', 'Zodiac']), (2, 2, '81C9', ['Recipes', 'Zodiac']), (2, 2, '4ohoe', ['Bathing', 'Zodiac']), (2, 2, '4ohc79', ['Herbal', 'Rosettes']), (2, 2, '4ohay', ['Apothecary', 'Herbal']), (2, 2, '4oh1o', ['Apothecary', 'Herbal']), (2, 2, '1oy9', ['Apothecary', 'Herbal']), (2, 2, '1ch9', ['Apothecary', 'Zodiac']), (2, 2, '1c89', ['Bathing', 'Recipes'])]
nodes = []
meta = []

for sec_cnt, hits, word, secs in bridges:
    c_val = 0.9 if word.startswith(('8','4o','2','o')) else 0.3
    p_val = round(sec_cnt / 5.0, 2)
    r_val = round(min(hits / 6.0, 1.0), 2)
    s_val = 0.9 if word.endswith(('9','am','ay','89')) else 0.3
    v = PsiVector(c=c_val, p=p_val, r=r_val, s=s_val, Φ=0.85, T=0.75, E=r_val, d=0.1, a=p_val)
    nodes.append(v)
    meta.append((word, secs))

# Link bridge words that share at least two manuscript sections
for i in range(len(nodes)):
    for j in range(i+1, len(nodes)):
        shared = set(meta[i][1]).intersection(meta[j][1])
        if len(shared) >= 2:
            connect(nodes[i], nodes[j], weight=0.7, type='shared_sections')

visualize_lattice(nodes, title='Voynich Rosetta Bridge Words (c=Prefix, p=Sections Bridged, r=Frequency)')

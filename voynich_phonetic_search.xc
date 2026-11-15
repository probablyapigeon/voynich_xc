# XC Automated Phonetic Key Search & Falsification Probe
top_keys = [(0.509, {'o': 'co', 'k': 'r', 'h': 'q', 'e': 'n', 'a': 'u', 'm': '', 'n': 'e', 'y': 'us', 'c': 'u', '8': 're', '9': 'a', '4': '', '1': 'd', 'z': 't', 'd': 'm'}, [('okoe', 'corcon', 'succus', 0.3, '4-Section Bridge Element'), ('oe', 'con', 'con', 1.0, "Preposition ('in / with')"), ('4ohan', 'coque', 'coque', 1.0, "Active Verb ('infuse/decoct')"), ('4ohC9', 'coqua', 'aqua', 0.44, "Aqueous Base ('decoction')"), ('okam', 'coru', 'cera', 0.5, "Lipid Base ('oil / salve')"), ('okay', 'coruus', 'syrupus', 0.368, "Sweet Excipient ('honey')"), ('okC89', 'corurea', 'centaurea', 0.37, 'Herb-41v (Jar 95r2)'), ('okaz', 'corut', 'ruta', 0.44, 'Herb-58v (Jar 89v2)'), ('ohd9', 'coqma', 'malva', 0.371, 'Herb-17v (Jar 101v2)'), ('ohCo', 'coquco', 'mentha', 0.3, 'Herb-31v (Jar 87r)')]), (0.502, {'o': '', 'k': 'm', 'h': 'co', 'e': 'in', 'a': 'e', 'm': 're', 'n': 'c', 'y': 'l', 'c': 'co', '8': 'c', '9': 'a', '4': 're', '1': 'in', 'z': 'us', 'd': 'l'}, [('okoe', 'min', 'ros', 0.3, '4-Section Bridge Element'), ('oe', 'in', 'in', 1.0, "Preposition ('in / with')"), ('4ohan', 'recoec', 'recipe', 0.543, "Active Verb ('infuse/decoct')"), ('4ohC9', 'recocoa', 'decocio', 0.487, "Aqueous Base ('decoction')"), ('okam', 'mere', 'cera', 0.4, "Lipid Base ('oil / salve')"), ('okay', 'mel', 'mel', 1.0, "Sweet Excipient ('honey')"), ('okC89', 'mcoca', 'urtica', 0.312, 'Herb-41v (Jar 95r2)'), ('okaz', 'meus', 'ruta', 0.3, 'Herb-58v (Jar 89v2)'), ('ohd9', 'cola', 'viola', 0.44, 'Herb-17v (Jar 101v2)'), ('ohCo', 'coco', 'apium', 0.24, 'Herb-31v (Jar 87r)')]), (0.498, {'o': 'i', 'k': 'c', 'h': 'u', 'e': 'n', 'a': 'e', 'm': 'r', 'n': 'co', 'y': 'l', 'c': 'a', '8': 're', '9': 'q', '4': '', '1': 'i', 'z': 'us', 'd': 're'}, [('okoe', 'icin', 'aqua', 0.3, '4-Section Bridge Element'), ('oe', 'in', 'in', 1.0, "Preposition ('in / with')"), ('4ohan', 'iueco', 'coque', 0.467, "Active Verb ('infuse/decoct')"), ('4ohC9', 'iuaq', 'aqua', 0.75, "Aqueous Base ('decoction')"), ('okam', 'icer', 'cera', 0.75, "Lipid Base ('oil / salve')"), ('okay', 'icel', 'mel', 0.35, "Sweet Excipient ('honey')"), ('okC89', 'icareq', 'urtica', 0.425, 'Herb-41v (Jar 95r2)'), ('okaz', 'iceus', 'laurus', 0.312, 'Herb-58v (Jar 89v2)'), ('ohd9', 'iureq', 'malva', 0.3, 'Herb-17v (Jar 101v2)'), ('ohCo', 'iuai', 'apium', 0.323, 'Herb-31v (Jar 87r)')])]
print('=== TOP 3 OPTIMIZED PHONETIC CIPHER KEYS (18,000 CANDIDATES TESTED) ===')

rank = 1
for mean_score, key_map, rows in top_keys:
    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
    print('\nRANK #' + str(rank) + ' | Mean Cross-Crib Alignment:', mean_score)
    print('  Glyph Key:', key_map)
    for tok, rend, gloss, sim, role in rows:
        node = Ψ(c=sim, p=0.85, r=sim, s=sim, Φ=sim, 𝒯=sim, E=sim, d=1.0-sim, a=sim)
        τᵢⱼ(agent, node, weight=0.35, type='optimized_crib')
        agent = Ouroboros(agent, target=node)
        print(f'  {tok:<8} -> {rend:<12} | Best Gloss: {gloss:<12} (sim={sim}) | {role}')
    print('  Converged XEMBRA State:', agent)
    rank = rank + 1

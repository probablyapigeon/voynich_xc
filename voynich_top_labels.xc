# XC High-Energy Standalone Label Extractor (Pure XEMBRA Primitives)
top_labels = [('ok189', 3, 0.9, 0.9, 0.5), ('ohC9', 3, 0.9, 0.9, 0.4), ('8ay9', 2, 0.9, 0.9, 0.4), ('2o8am', 2, 0.9, 0.9, 0.5), ('say9', 2, 0.2, 0.9, 0.4), ('oham', 2, 0.9, 0.9, 0.4), ('ohco8', 2, 0.9, 0.2, 0.5), ('okcoe', 2, 0.9, 0.2, 0.5), ('oyoe', 2, 0.9, 0.2, 0.4), ('okam', 1, 0.9, 0.9, 0.4), ('soyan', 1, 0.2, 0.2, 0.5), ('2oyo8o', 1, 0.9, 0.2, 0.6), ('4oh9', 1, 0.9, 0.9, 0.4), ('8ano8', 1, 0.9, 0.2, 0.5), ('91caeo8', 1, 0.2, 0.2, 0.7), ('9kam', 1, 0.2, 0.9, 0.4), ('sohay', 1, 0.2, 0.9, 0.5), ('oaoyay', 1, 0.9, 0.9, 0.6), ('91ch19', 1, 0.2, 0.9, 0.6), ('h1am', 1, 0.2, 0.9, 0.4)]
print('=== TOP 20 REPEATING HIGH-ENERGY PICTURE LABELS ===')
for word, count, c_val, s_val, e_val in top_labels:
    node = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.7, 𝒯=0.5, E=e_val, d=0.2, a=0.5)
    print(word, '| count:', count, '|', node)

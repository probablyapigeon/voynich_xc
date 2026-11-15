# XC Exact Page & Line Locator for Top Labels
hits = [('8ay9', '<32r.9>', 737, '89k1oy 8ay9'), ('2o8am', '<32r.12>', 740, '2o8am Ekoe'), ('ok189', '<67v2.label_upper_left>', 1582, 'ok189'), ('oham', '<68r1.4>', 1624, '81ot oham'), ('ok189', '<68v2.pieslice_2>', 1688, 'ok189 1ikae'), ('8ay9', '<68v2.radial_6>', 1696, '1okC9 8ay9'), ('ohC9', '<69r.radial_12>', 1725, '1ohco8 ohC9'), ('ohC9', '<69v.radial_3>', 1743, 'ohC9 say'), ('ohC9', '<69v.radial_10>', 1750, 'ohC9 89'), ('ohco8', '<69v.radial_17>', 1757, 'ohco8'), ('okcoe', '<69v.radial_19>', 1759, 'okcoe'), ('ohco8', '<69v.radial_21>', 1761, 'ohco8'), ('ok189', '<77r.labels_side_1>', 2041, 'ok189'), ('oyoe', '<80v.44>', 2376, '4ohae oyoe'), ('oyoe', '<82r.label_middle>', 2436, 'oyoe 8az'), ('oham', '<83v.label_bottom_2>', 2566, 'oham'), ('2o8am', '<rose.seast_center_9>', 2900, 'yaZ 2o8am'), ('okcoe', '<100r.labels_3>', 3287, '2oHc9 okcoe')]
print('=== EXACT PAGE HEADERS & LINE NUMBERS ===')
for word, page, line_no, full_line in hits:
    node = Ψ(c=0.9, p=0.5, r=0.5, s=0.9, Φ=0.8, 𝒯=0.6, E=0.5, d=0.1, a=0.5)
    print(word, '| Line:', line_no, '| Header:', page, '| Label:', full_line)

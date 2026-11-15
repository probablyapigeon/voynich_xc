# XC Folio Locator for Top Repeating Picture Labels
hits = [('8ay9', 'unknown', '89k1oy 8ay9', 0.4), ('2o8am', 'unknown', '2o8am Ekoe', 0.5), ('ok189', 'unknown', 'ok189', 0.5), ('oham', 'unknown', '81ot oham', 0.4), ('ok189', 'unknown', 'ok189 1ikae', 0.5), ('8ay9', 'unknown', '1okC9 8ay9', 0.4), ('ohC9', 'unknown', '1ohco8 ohC9', 0.4), ('ohC9', 'unknown', 'ohC9 say', 0.4), ('ohC9', 'unknown', 'ohC9 89', 0.4), ('ohco8', 'unknown', 'ohco8', 0.5), ('okcoe', 'unknown', 'okcoe', 0.5), ('ohco8', 'unknown', 'ohco8', 0.5), ('ok189', 'unknown', 'ok189', 0.5), ('oyoe', 'unknown', '4ohae oyoe', 0.4), ('oyoe', 'unknown', 'oyoe 8az', 0.4), ('oham', 'unknown', 'oham', 0.4), ('2o8am', 'unknown', 'yaZ 2o8am', 0.5), ('okcoe', 'unknown', '2oHc9 okcoe', 0.5)]
print('=== FOLIO LOCATIONS OF TOP PICTURE LABELS ===')
for word, folio, full_line, e_val in hits:
    node = Ψ(c=0.9, p=0.5, r=e_val, s=0.9, Φ=0.8, 𝒯=0.6, E=e_val, d=0.1, a=0.5)
    print(word, '| Folio:', folio, '| Label Line:', full_line, '|', node)

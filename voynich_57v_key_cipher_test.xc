# XC Folio 57v 17-Character Cycle Substitution & Positional Cipher Test
unique_key_glyphs = ['o', 'e', '8', 'y', '^', 'h', 'p', 'g', '?', 'k', '9', 'E']
top_eva_glyphs = ['o', '9', 'a', 'c', '1', 'e', '8', 'h', 'y', 'k', '4', 'm', '2', 'C', '7']
overlap_summary = [('57v.5th_ring', 31, 20, 64.52), ('57v.center', 30, 19, 63.33), ('66r.glyph_column', 35, 23, 65.71), ('66r.1_sample', 46, 21, 45.65)]
rotation_results = [(0, 0, [], '4os+4aowyaza34uw4oacwmyykoy9cko\\ja'), (1, 0, [], 'm9s+mc9wkazc3muwm9c1w2kk49ka149\\jc'), (2, 0, [], '2as+21aw4az132uw2a1ewC44ma4cema\\j1'), (3, 0, [], 'Ccs+Cecwmaze3CuwCce8w7mm2cm182c\\je'), (4, 0, [], '71s+781w2az837uw718hwo22C12ehC1\\j8'), (5, 0, [], 'oes+ohewCazh3ouwoehyw9CC7eC8y7e\\jh'), (6, 0, [], '98s+9y8w7azy39uw98ykwa77o87hko8\\jy'), (7, 0, [], 'ahs+akhwoazk3auwahk4wcoo9hoy49h\\jk'), (8, 0, [], 'cys+c4yw9az43cuwcy4mw199ay9kmay\\j4'), (9, 0, [], '1ks+1mkwaazm31uw1km2weaacka42ck\\jm'), (10, 0, [], 'e4s+e24wcaz23euwe42Cw8cc14cmC14\\j2'), (11, 0, [], '8ms+8Cmw1azC38uw8mC7wh11em127em\\jC')]
half1 = ['9', 'o', 's', '+', '9', '8', 'o', 'w', '?', '|', 'az', '8', '3', '9', 'u', 'w', '9']
half2 = ['o', '8', 'y', 'w', 'E', '?', '?', 'k', 'o', '?', 'e', 'y', 'k', 'o', '\\', 'j', '8']
pos_matches_17 = 0

print('=== 1. 57v.2nd_ring KEY GLYPH INVENTORY VS. TOP MANUSCRIPT EVA GLYPHS ===')
print('15 Unique Key Glyphs (57v.2nd_ring):', unique_key_glyphs)
print('Top 15 Global EVA Glyphs (Full MS): ', top_eva_glyphs)

print('\n=== 2. TARGET CHARACTER COVERAGE BY 57v KEY INVENTORY ===')
for name, total_c, in_k, pct in overlap_summary:
    print(name, '| Total Chars:', total_c, '| In 57v Key:', in_k, '| Coverage:', pct, '%')

print('\n=== 3. 34-GLYPH COLUMN (66r) SPLIT AT PERIOD 17 (HALF 1 VS HALF 2) ===')
print('First 17 :', ' '.join(half1))
print('Second 17:', ' '.join(half2))
print('Exact Positional Matches at Period 17:', pos_matches_17, '/ 17')

print('\n=== 4. CYCLIC SUBSTITUTION ROTATIONS (SHIFT 0..14) ON 57v INNER RINGS & 66r COLUMN ===')
for shift, hcnt, hits, gcol_dec in rotation_results:
    print('Shift', shift, '| Recipe Vocab Hits on 57v Inner:', hcnt, '| Hits:', hits)
    print('   Decoded 66r Glyph Column:', gcol_dec)

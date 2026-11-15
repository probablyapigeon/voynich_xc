# XC Triplicate Formula Context Inspector
matches = [('4ohae okae okap', 3725, '106v.12', False, '106v.11: k189s ay 2c7( okCo79 h2c79 4ok189 4okay 2c79 4okc89 og19 Wam 3ap', '91C9 4o C 89 1o8an okae 179 4oham 1oham 1o89 4ohae okae okap', '106v.13: oehccae h1c89 4oCc9 yae 1S ae 9kay 2s9 e1c9 9ham 29 ehap', [(0.2, 0.9, 0.4), (0.9, 0.2, 0.2), (0.2, 0.2, 0.1), (0.9, 0.9, 0.2), (0.9, 0.9, 0.5), (0.9, 0.2, 0.4), (0.9, 0.9, 0.3), (0.9, 0.9, 0.5), (0.9, 0.9, 0.5), (0.9, 0.9, 0.4), (0.9, 0.2, 0.5), (0.9, 0.2, 0.4), (0.9, 0.2, 0.4)]), ('oham okam okay', 3794, '107r.34', False, '107r.33: 9am 1ch an 1co ham 1c9 4oe haM 1h9 e 1cce ehay ohae', 'faisay ae ayo ehC9 4okae 1cokan 8ay oham okam okay ogaP', '107r.35: 8am %e ehCoe e 1c79 4oho y eham 1c89 4okam ae oe hae7aP', [(0.2, 0.9, 0.6), (0.2, 0.2, 0.2), (0.2, 0.2, 0.3), (0.2, 0.9, 0.4), (0.9, 0.2, 0.5), (0.9, 0.9, 0.6), (0.9, 0.9, 0.3), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.9, 0.2, 0.4)]), ('4ohae okae okap', 3801, '107r.41', False, '107r.40: eoeham 1c9 4o ham 1ae am okam oehay okaz Ahae ohae', '4ohan ay oHc9 4ohae okae okap', '107r.42: g1oeh9 so hcc9 am okC9 9h1c9 gai19 ohC9 kan ay ayo8e hazcp', [(0.9, 0.9, 0.5), (0.2, 0.9, 0.2), (0.9, 0.9, 0.4), (0.9, 0.2, 0.5), (0.9, 0.2, 0.4), (0.9, 0.2, 0.4)]), ('oham okam okay', 4233, '113v.22', False, '113v.21: goe am okay 4okan 1koe kayoe 1coe ham 1jh1cos ohay aVay eo', 'oham oham 1Ch9 y am oeae oham 1co89 oham okam okay ae9', '113v.23: 9ham ae hay ohan 4o ham 1Ahaz ohay ae 1co89 4ohay okae ehe eoe', [(0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.2, 0.2, 0.1), (0.2, 0.9, 0.2), (0.9, 0.2, 0.4), (0.9, 0.9, 0.4), (0.9, 0.9, 0.5), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.2, 0.9, 0.3)])]
print('=== EXACT FOLIO CONTEXT FOR TRIPLICATE FORMULAS ===')

for tri, line_no, page, is_star, prev_line, curr_line, next_line, obs in matches:
    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
    for c_val, s_val, e_val in obs:
        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)
        τᵢⱼ(agent, tok, weight=0.3, type='triad_context')
        agent = Ouroboros(agent, target=tok)
    print('\nTRIAD:', tri, '| Line:', line_no, '| Folio:', page, '| Paragraph Start:', is_star)
    print('   Line State:', agent)
    print('   [PREV] ', prev_line)
    print('   [MATCH]', curr_line)
    print('   [NEXT] ', next_line)

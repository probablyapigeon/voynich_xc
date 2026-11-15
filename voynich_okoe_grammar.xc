# XC Grammatical Partner-Shift Probe for [okoe]
herb_partners = ['8aM', '9hom', '1oe', '1oe', 'ok9', '1oe', '1am', 'ok19', '8am', '1oe', '1oe', 'oeoZ', 'okaZ', '1ok19', '1oh9', '1oe', '2ok1oy', '8oe', 'Koe', '8am', '+oe', '8am', '8am', 'h1os', 'U9', '1oe', 'oh1o89', 'okay', '1ohc9']
bath_partners = ['1Hc9', 'ok9', '8179', 'am', '2c89', 'oµN9', '8an', 'kcoe', 'oj1c89', '1c89', '1Hc79', '1c89', '1c89']
print('Herbal followers of okoe:', herb_partners)
print('Bathing followers of okoe:', bath_partners)

def track(obs, label):
    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
    for c_val, s_val, e_val in obs:
        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)
        τᵢⱼ(agent, tok, weight=0.35, type=label)
        agent = Ouroboros(agent, target=tok)
    print(label, '->', agent)

track([(0.9, 0.2, 0.3), (0.2, 0.2, 0.4), (0.2, 0.2, 0.3), (0.2, 0.2, 0.3), (0.9, 0.9, 0.3), (0.2, 0.2, 0.3), (0.2, 0.9, 0.3), (0.9, 0.9, 0.4), (0.9, 0.9, 0.3), (0.2, 0.2, 0.3), (0.2, 0.2, 0.3), (0.9, 0.2, 0.4), (0.9, 0.2, 0.4), (0.2, 0.9, 0.5), (0.2, 0.9, 0.4), (0.2, 0.2, 0.3), (0.9, 0.2, 0.6), (0.9, 0.2, 0.3), (0.2, 0.2, 0.3), (0.9, 0.9, 0.3), (0.2, 0.2, 0.3), (0.9, 0.9, 0.3), (0.9, 0.9, 0.3), (0.2, 0.2, 0.4), (0.2, 0.9, 0.2), (0.2, 0.2, 0.3), (0.9, 0.9, 0.6), (0.9, 0.9, 0.4), (0.2, 0.9, 0.5)], '1. Herbal okoe-Followers')
track([(0.2, 0.9, 0.4), (0.9, 0.9, 0.3), (0.9, 0.9, 0.4), (0.2, 0.9, 0.2), (0.9, 0.9, 0.4), (0.9, 0.9, 0.4), (0.9, 0.2, 0.3), (0.2, 0.2, 0.4), (0.9, 0.9, 0.6), (0.2, 0.9, 0.4), (0.2, 0.9, 0.5), (0.2, 0.9, 0.4), (0.2, 0.9, 0.4)], '2. Bathing okoe-Followers')

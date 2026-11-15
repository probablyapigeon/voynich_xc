# XC Birdsong Motif Mutation & Cadence Resolution Probe (Pure XEMBRA)
bouts = [[(1, 0.7, 0.2, 0.4), (0, 0.7, 0.2, 0.7), (0, 0.3, 0.2, 0.4), (0, 0.9, 0.2, 0.8), (0, 0.9, 0.9, 0.7), (0, 0.3, 0.9, 0.7)], [(1, 0.7, 0.2, 0.4), (0, 0.9, 0.2, 0.8), (0, 0.9, 0.2, 0.8), (0, 0.3, 0.2, 0.4), (0, 0.9, 0.9, 0.8), (0, 0.7, 0.9, 0.6)], [(1, 0.7, 0.2, 0.4), (0, 0.7, 0.2, 0.7), (0, 0.9, 0.2, 1.0), (0, 0.9, 0.9, 0.7), (0, 0.3, 0.9, 0.7)], [(1, 0.7, 0.2, 0.4), (0, 0.3, 0.2, 0.4), (0, 0.9, 0.2, 1.0), (0, 0.9, 0.9, 0.7), (0, 0.9, 0.9, 0.8)]]
shuffled = [(0.9, 0.9, 0.7), (0.7, 0.2, 0.4), (0.3, 0.9, 0.7), (0.9, 0.2, 0.8), (0.7, 0.9, 0.6), (0.3, 0.2, 0.4), (0.7, 0.2, 0.7), (0.9, 0.9, 0.8), (0.7, 0.2, 0.4), (0.9, 0.2, 0.8), (0.3, 0.9, 0.7), (0.9, 0.2, 1.0), (0.7, 0.2, 0.7), (0.9, 0.9, 0.7), (0.3, 0.2, 0.4), (0.9, 0.9, 0.8), (0.7, 0.2, 0.4), (0.9, 0.2, 1.0), (0.9, 0.2, 0.8), (0.3, 0.2, 0.4), (0.7, 0.2, 0.4), (0.9, 0.9, 0.7)]

baseline = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
continuous_bird = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
breath_reset_bird = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)

for bout in bouts:
    breath_reset_bird = Ouroboros(breath_reset_bird, target=baseline)
    for is_first, c_val, s_val, e_val in bout:
        p_val = 0.9 if is_first == 1 else 0.2
        tok = Ψ(c=c_val, p=p_val, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)

        τᵢⱼ(continuous_bird, tok, weight=0.30, type='continuous_song')
        continuous_bird = Ouroboros(continuous_bird, target=tok)

        τᵢⱼ(breath_reset_bird, tok, weight=0.30, type='bout_reset_song')
        breath_reset_bird = Ouroboros(breath_reset_bird, target=tok)

shuffled_bird = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
for c_val, s_val, e_val in shuffled:
    tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)
    τᵢⱼ(shuffled_bird, tok, weight=0.30, type='shuffled_control')
    shuffled_bird = Ouroboros(shuffled_bird, target=tok)

print('=== BIRDSONG MOTIF & CADENCE PROBE RESULTS ===')
print('1. Continuous Stream (Cross-Bout Memory) :', continuous_bird)
print('2. Breath-Reset Stream (Bout-Locked)     :', breath_reset_bird)
print('3. Shuffled Control (Scrambled Order)    :', shuffled_bird)

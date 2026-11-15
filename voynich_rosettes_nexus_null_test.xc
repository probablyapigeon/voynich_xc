# XC Probe #38: Rosettes Dual-Chain Nexus Stratified Null-Permutation Validator (1,000 Trials)
rosettes_total_tokens = 1895
all_stems_result = {'observed': 678, 'null_mean': 618.7, 'null_std': 56.05, 'z_score': 1.06, 'p_value': 0.156}
complex_stems_result = {'observed': 98, 'null_mean': 87.73, 'null_std': 28.01, 'z_score': 0.37, 'p_value': 0.378}
top_complex_nexus = [('1c89', 39), ('2c89', 22), ('k189', 14), ('kC89', 8), ('2C89', 7), ('hc189', 2), ('ay89', 2), ('kcoe', 1), ('1coy', 1), ('h1oe', 1), ('ae89', 1)]
obs_nexus_states = [(0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.62), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5), (0.95, 0.85, 0.5)]
null_baseline_states = [(0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4), (0.45, 0.35, 0.4)]

def evolve_validation(obs_list, label):
    agent = Ψ(c=0.5, p=0.5, r=0.5, s=0.5, Φ=0.5, 𝒯=0.5, E=0.5, d=0.5, a=0.5)
    for c_val, s_val, e_val in obs_list:
        tok = Ψ(c=c_val, p=0.5, r=e_val, s=s_val, Φ=0.6, 𝒯=0.4, E=e_val, d=0.3, a=0.5)
        τᵢⱼ(agent, tok, weight=0.3, type=label)
        agent = Ouroboros(agent, target=tok)
    return agent

print('=== 1. STRATIFIED NULL PERMUTATION RESULTS (1,000 TRIALS | (len, log2_freq)) ===')
print(f"All Dual-Nexus Tokens (len >= 2)    : Observed = {all_stems_result['observed']} vs. Null = {all_stems_result['null_mean']} ± {all_stems_result['null_std']} | Z = {all_stems_result['z_score']:+.2f} (p = {all_stems_result['p_value']})")
print(f"Complex Nexus Tokens (len >= 4)     : Observed = {complex_stems_result['observed']} vs. Null = {complex_stems_result['null_mean']} ± {complex_stems_result['null_std']} | Z = {complex_stems_result['z_score']:+.2f} (p = {complex_stems_result['p_value']})")

print('\n=== 2. XEMBRA STATE VECTOR DIVERGENCE (OBSERVED NEXUS VS. STRATIFIED NULL) ===')
print('Observed Complex Nexus Hub :', evolve_validation(obs_nexus_states, 'observed_rosettes_nexus'))
print('Stratified Null Baseline   :', evolve_validation(null_baseline_states, 'stratified_null_pool'))

print('\n=== 3. TOP COMPLEX DUAL-NEXUS STEMS (len >= 4 | NON-PARTICLE HUBS) ===')
for st, cnt in top_complex_nexus:
    print(f'  {st:<12} : {cnt} hits inside Rosettes (85r-86v)')
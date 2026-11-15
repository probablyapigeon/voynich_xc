from xembra_core import PsiVector, connect
from xembra_visualizer import visualize_lattice

# Stage Anchors in (c=Prefix Lock, p=Section Depth, r=Cross-Section Reach)
herbal_hub = PsiVector(c=0.45, p=0.15, r=0.95, s=0.35, Φ=0.85, T=0.70, E=0.80, d=0.20, a=0.85)
apoth_hub  = PsiVector(c=0.65, p=0.50, r=0.95, s=0.55, Φ=0.90, T=0.80, E=0.85, d=0.15, a=0.90)
recipe_hub = PsiVector(c=0.88, p=0.85, r=0.95, s=0.85, Φ=0.95, T=0.85, E=0.90, d=0.10, a=0.95)

# Top 3-Way Supply Chain Compounds: (name, c_prefix, p_stage, r_reach, s_suffix, E_energy)
supply_nodes = [
    # Raw Herbal -> Jar Label Compounds (o- / 1- prefix cluster)
    ("oham (Raw Herb/Jar)",   0.45, 0.25, 0.88, 0.90, 0.78),
    ("1coe (Jar Staple #1)",  0.39, 0.48, 0.92, 0.30, 0.86),
    ("okoe (4-Sec Master)",   0.46, 0.42, 1.00, 0.28, 0.92),
    ("okam (Herbal/Recipe)",  0.45, 0.35, 0.76, 0.90, 0.74),
    ("ohae (Leaf/Prep)",      0.46, 0.38, 0.78, 0.28, 0.75),
    ("1coy (Jar/Herbal)",     0.39, 0.45, 0.72, 0.30, 0.71),
    # Activated Recipe Compounds (4o- / qo- prefix cluster)
    ("4oham (Active oham)",   0.89, 0.78, 0.86, 0.90, 0.84),
    ("4ohC9 (Universal Base)",0.90, 0.82, 0.94, 0.90, 0.88),
    ("4ohoe (Activated ohoe)",0.88, 0.74, 0.70, 0.30, 0.79),
    ("4ohay (Activated ohay)",0.89, 0.76, 0.74, 0.90, 0.80),
]

nodes = [herbal_hub, apoth_hub, recipe_hub]
for name, c_v, p_v, r_v, s_v, e_v in supply_nodes:
    nodes.append(PsiVector(c=c_v, p=p_v, r=r_v, s=s_v, Φ=0.85, T=0.75, E=e_v, d=0.15, a=0.85))

# Connect Stage Backbone: Herbal (0) -> Apothecary (1) -> Starred Recipes (2)
connect(nodes[0], nodes[1], weight=0.95, type="botanical_to_jar")
connect(nodes[1], nodes[2], weight=0.95, type="jar_to_recipe")

# Connect Raw Herbal/Jar nodes (3..8) to Herbal & Apothecary hubs
for i in range(3, 9):
    connect(nodes[0], nodes[i], weight=0.75, type="harvest_source")
    connect(nodes[i], nodes[1], weight=0.80, type="jar_storage")

# Connect Activated 4o- Recipe nodes (9..12) from Apothecary hub into Starred Recipes hub
for j in range(9, 13):
    connect(nodes[1], nodes[j], weight=0.85, type="4o_activation")
    connect(nodes[j], nodes[2], weight=0.90, type="recipe_synthesis")

# Direct morphological transformation links: oham -> 4oham and ohae -> 4ohay
connect(nodes[3], nodes[9],  weight=0.98, type="prefix_shift_o_to_4o")
connect(nodes[7], nodes[12], weight=0.92, type="prefix_shift_o_to_4o")

visualize_lattice(
    nodes,
    title="Voynich Supply Chain Lattice: Herbal (p=0.15) -> Apothecary (p=0.50) -> Recipes (p=0.85)"
)

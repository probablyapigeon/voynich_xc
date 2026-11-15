"""3D visualizer for XC Ψ states and τᵢⱼ links."""
import matplotlib.pyplot as plt

from xembra_core import PsiVector, tau_ij, connect


def visualize_lattice(lattice, title="XEMBRA Lattice"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    for i, psi in enumerate(lattice):
        ax.scatter(psi.c, psi.p, psi.r, s=100, label="Ψ vectors" if i == 0 else None)

    seen = set()
    first_link = True
    for (psi1, psi2), props in tau_ij.items():
        pair = frozenset((id(psi1), id(psi2)))
        if pair in seen or psi1 not in lattice or psi2 not in lattice:
            continue
        seen.add(pair)
        ax.plot(
            [psi1.c, psi2.c], [psi1.p, psi2.p], [psi1.r, psi2.r],
            linewidth=max(0.5, props["weight"] * 5), alpha=0.7,
            label="τᵢⱼ links" if first_link else None,
        )
        first_link = False

    ax.set_title(title)
    ax.set_xlabel("c")
    ax.set_ylabel("p")
    ax.set_zlabel("r")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    thought = PsiVector(c=0.9, p=0.2, r=0.8, s=0.5, Φ=0.7, T=0.6, E=0.4, d=0.3, a=0.5)
    emotion = PsiVector(c=0.3, p=0.4, r=0.6, s=0.7, Φ=0.8, T=0.9, E=0.9, d=0.5, a=0.2)
    memory = PsiVector(c=0.5, p=0.3, r=0.7, s=0.6, Φ=0.6, T=0.8, E=0.5, d=0.4, a=0.3)
    connect(thought, emotion, weight=0.8, type="emotional")
    connect(emotion, memory, weight=0.6, type="memory")
    visualize_lattice([thought, emotion, memory], title="Example XEMBRA Lattice")

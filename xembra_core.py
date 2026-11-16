"""XEMBRA Code (XC) prototype core.

This is a classical toy dynamical-system implementation of the legacy XC ideas.
Names such as Ψ, Ouroboros, and QTC are project vocabulary. In particular, QTC
is an engineered state transform here, not a quantum-mechanical collapse model.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Dict, Tuple


@dataclass(eq=False)
class PsiVector:
    """Nine-dimensional classical state vector used by the XC prototype.

    Every field defaults to 0.0 so XC examples can specify partial target states,
    e.g. Ψ(Φ=1.0, T=1.0).
    """

    c: float = 0.0
    p: float = 0.0
    r: float = 0.0
    s: float = 0.0
    Φ: float = 0.0
    T: float = 0.0
    E: float = 0.0
    d: float = 0.0
    a: float = 0.0

    def copy(self) -> "PsiVector":
        return PsiVector(**self.as_dict())

    def as_dict(self) -> dict:
        return {
            "c": float(self.c), "p": float(self.p), "r": float(self.r),
            "s": float(self.s), "Φ": float(self.Φ), "T": float(self.T),
            "E": float(self.E), "d": float(self.d), "a": float(self.a),
        }

    def __add__(self, other: "PsiVector") -> "PsiVector":
        """Average two states; legacy XC called this 'superposition'.

        This is only arithmetic averaging and should not be confused with
        quantum superposition.
        """
        if not isinstance(other, PsiVector):
            return NotImplemented
        a = self.as_dict()
        b = other.as_dict()
        return PsiVector(**{k: (a[k] + b[k]) / 2.0 for k in a})

    def __repr__(self) -> str:
        return (
            f"Ψ(c={self.c:.3f}, p={self.p:.3f}, r={self.r:.3f}, s={self.s:.3f}, "
            f"Φ={self.Φ:.3f}, 𝒯={self.T:.3f}, E={self.E:.3f}, "
            f"d={self.d:.3f}, a={self.a:.3f})"
        )


tau_ij: Dict[Tuple[PsiVector, PsiVector], dict] = {}


def connect(psi1: PsiVector, psi2: PsiVector, weight: float = 1.0, type: str = "generic") -> None:
    props = {"weight": float(weight), "type": str(type)}
    tau_ij[(psi1, psi2)] = dict(props)
    tau_ij[(psi2, psi1)] = dict(props)


def F(psi: PsiVector) -> PsiVector:
    psi.c *= 1.1
    return psi


def D(psi: PsiVector) -> PsiVector:
    psi.E *= 0.9
    return psi


def V(psi: PsiVector, target: PsiVector, alpha: float = 0.05) -> PsiVector:
    alpha = float(alpha)
    for name in ("c", "p", "r", "s", "Φ", "T", "E", "d", "a"):
        current = getattr(psi, name)
        goal = getattr(target, name)
        setattr(psi, name, current + alpha * (goal - current))
    return psi


def H(psi: PsiVector) -> PsiVector:
    vals = list(psi.as_dict().values())
    norm = sqrt(sum(v * v for v in vals))
    if norm > 0.0:
        for name in ("c", "p", "r", "s", "Φ", "T", "E", "d", "a"):
            setattr(psi, name, getattr(psi, name) / norm)
    return psi


def Ouroboros(psi: PsiVector, target: PsiVector, alpha: float = 0.05) -> PsiVector:
    link = tau_ij.get((psi, target))
    eff_alpha = float(alpha) * float(link["weight"]) if link is not None else float(alpha)
    return H(V(D(F(psi)), target, alpha=eff_alpha))


def QTC(psi: PsiVector, order: str = "A→N→G") -> PsiVector:
    """Legacy 'QTC' selection transform.

    This function is a classical hard-coded state mutation. It does not simulate
    quantum measurement, entanglement, or physical wave-function collapse.
    """
    if order == "A→N→G":
        psi.E = 0.1
        psi.d = 0.1
    elif order == "G→N→A":
        psi.E = 0.9
        psi.d = 0.9
    else:
        raise ValueError(f"unknown QTC order: {order!r}")
    return psi


Ψ = PsiVector


def tau(psi1: PsiVector, psi2: PsiVector, weight: float = 1.0, type: str = "generic") -> None:
    return connect(psi1, psi2, weight=weight, type=type)


if __name__ == "__main__":
    thought = PsiVector(c=0.9, p=0.2, r=0.8, s=0.5, Φ=0.7, T=0.6, E=0.4, d=0.3, a=0.5)
    emotion = PsiVector(c=0.3, p=0.4, r=0.6, s=0.7, Φ=0.8, T=0.9, E=0.9, d=0.5, a=0.2)
    connect(thought, emotion, weight=0.8, type="emotional")
    updated = Ouroboros(thought, target=emotion)
    print("Updated Thought:", updated)
    print("QTC Output:", QTC(updated, order="A→N→G"))

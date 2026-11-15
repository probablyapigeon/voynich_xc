"""Tiny interpreter/runner for the XC prototype syntax.

XC v0.1 is intentionally close to Python. This runner translates the two main
Unicode surface tokens into safe Python-side names and executes trusted local
XC scripts in a small namespace.

Security note: this is a prototype runner, not a hardened sandbox. Run only XC
files you trust.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from xembra_core import PsiVector, Ψ, connect, tau, F, D, V, H, Ouroboros, QTC, tau_ij


def preprocess(source: str) -> str:
    source = source.replace("τᵢⱼ", "tau")
    source = source.replace("𝒯=", "T=")
    return source


def run_xc(path: str | Path, *, capabilities: dict | None = None) -> dict:
    path = Path(path)
    source = preprocess(path.read_text(encoding="utf-8"))
    env = {
        "__builtins__": {"print": print},
        "PsiVector": PsiVector,
        "Ψ": Ψ,
        "connect": connect,
        "tau": tau,
        "F": F,
        "D": D,
        "V": V,
        "H": H,
        "Ouroboros": Ouroboros,
        "QTC": QTC,
        "tau_ij": tau_ij,
    }
    if capabilities is not None:
        for name, capability in capabilities.items():
            if (
                not isinstance(name, str) or not name.isidentifier()
                or name.startswith('_') or name in env or name in env['__builtins__']
            ):
                raise ValueError(f"invalid or reserved XC capability name: {name!r}")
            if not callable(capability):
                raise TypeError(f"XC capability {name!r} must be callable")
        env.update(capabilities)
    exec(compile(source, str(path), "exec"), env, env)
    return env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a trusted XC prototype program")
    parser.add_argument("file", help="path to .xc file")
    args = parser.parse_args()
    run_xc(args.file)


if __name__ == "__main__":
    main()

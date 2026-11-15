SCRIBE_MAP: dict[str, int] = {
    # Scribe 1 (Currier A: Herbal A & Pharmaceutical Jars)
    **{f"{n}{side}": 1 for n in [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 27, 28, 29, 30, 32, 35, 36, 37, 38, 42, 44, 45,
        47, 49, 51, 52, 53, 54, 56, 58, 65, 87, 88, 89, 90, 93, 94, 95, 96,
        99, 100, 101, 102
    ] for side in ("r", "v")},

    # Scribe 2 (Currier B: Herbal B, Balneological & Rosettes Foldout)
    **{f"{n}{side}": 2 for n in [
        26, 31, 33, 34, 39, 40, 43, 46, 48, 50, 55,
        75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86
    ] for side in ("r", "v")},

    # Scribe 3 (Currier B: Folio 57v & Starred Recipes except 115v)
    "57v": 3,
    **{f"{n}{side}": 3 for n in [
        103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114
    ] for side in ("r", "v")},
    "115r": 3,
    "116r": 3,

    # Scribe 4 (Currier B: Astronomical & Zodiac Section)
    **{f"{n}{side}": 4 for n in [
        67, 68, 69, 70, 71, 72, 73
    ] for side in ("r", "v")},

    # Scribe 5 (Currier B: 41r-v, 57r, 66r-v, and 115v)
    "41r": 5, "41v": 5,
    "57r": 5,
    "66r": 5, "66v": 5,
    "115v": 5,
}


def get_scribe_id(folio_tag: str) -> int | None:
    """
    Resolve a folio or sub-panel tag (e.g., '89r1', '68v3', '104r.14')
    to its Scribe ID (1-5). Returns None for missing folios or 116v.
    """
    base = folio_tag.split(".")[0].strip()
    if base in SCRIBE_MAP:
        return SCRIBE_MAP[base]
    normalized = base.rstrip("0123456789")
    return SCRIBE_MAP.get(normalized)


if __name__ == "__main__":
    print(f"Loaded {len(SCRIBE_MAP)} folio sides.")
    for sample in ("5v", "89r1", "77r", "104r.14", "115r", "115v"):
        print(f"  {sample} -> Scribe {get_scribe_id(sample)}")

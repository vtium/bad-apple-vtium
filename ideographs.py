"""The ideograph pool the CJK stream of act 6 draws from (effects.py).

Copied from fork/demo/glyph-text.py in the kmscon fork at
https://github.com/aaronsb/kmscon (commit cca86bed). That script draws the
same pool, and the two copies may drift.
"""


def ideographs(rng):
    """6000 ideographs of the URO block in an order rng shuffles, and their
    weights by Zipf's law, the first commonest."""
    chars = [chr(c) for c in range(0x4E00, 0x9FF0)]
    rng.shuffle(chars)
    chars = chars[:6000]
    return chars, [1.0 / (rank + 1) for rank in range(len(chars))]

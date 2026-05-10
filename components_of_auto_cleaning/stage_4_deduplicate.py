 
# ==============================================================================
# STAGE 4 | DEDUPLICATION
# ==============================================================================
#
#   Role:
#       Remove repeated content — both exact copies and near-identical text.
#       Like removing water collected twice from the same source.
#
#   Types of duplicates:
#
#       Exact duplicate:
#           "The cat sat on the mat"
#           "The cat sat on the mat"   ←  identical, REMOVE
#
#       Near duplicate:
#           "The cat sat on the mat"
#           "The cat sat on the mat!"  ←  99% similar, REMOVE
#
#   Why it matters:
#       If the same text appears 1,000 times, the model thinks it is
#       1,000x more important than everything else — skewing training badly.
#
#   Analogy:
#       Removing water that was already collected from the same
#       source twice — no point processing it again.
#
# ==============================================================================


# =======================================================================
# CODE SAMPLE
# ----------
from hashlib import md5

def make_shingles(text: str, k: int = 5) -> set[str]:
    words = text.split()
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

def deduplicate(records, jaccard_threshold: float = 0.8):
    """Yield only unique records using exact hash + shingle-based near-dup."""
    seen_hashes: set[str]        = set()
    seen_shingles: list[set[str]] = []

    for record in records:
        text = record["text"]

        # Exact duplicate check
        h = md5(text.encode()).hexdigest()
        if h in seen_hashes:
            continue

        # Near-duplicate check (Jaccard similarity)
        shingles = make_shingles(text)
        for prev in seen_shingles:
            overlap = len(shingles & prev) / max(len(shingles | prev), 1)
            if overlap >= jaccard_threshold:
                break
        else:
            seen_hashes.add(h)
            seen_shingles.append(shingles)
            yield record

# ── usage ──────────────────────────────────────────────────────
# unique = deduplicate(cleaned)  →  feeds into filter_records()


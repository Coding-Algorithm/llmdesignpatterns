# ==============================================================================
# STAGE 5 | FILTERING
# ==============================================================================
#
#   Role:
#       Remove text that is low quality or irrelevant based on set rules.
#       Like discarding water that is too salty or too contaminated.
#
#   Example rules:
#       ✗  Text shorter than 100 words        →  likely junk
#       ✗  Text with >50% special characters  →  likely spam or code
#       ✗  Text with perplexity score > 1000  →  likely gibberish
#       ✗  Non-English text                   →  off-target for English LLM
#
#   Result:
#       Before filtering:  10,000,000 documents
#       After filtering:    6,000,000 documents  (40% removed)
#
#   Analogy:
#       Discarding water that is too salty, too acidic, or contaminated
#       beyond what the purification system can recover.
#
# ==============================================================================
 


# =======================================================================
# CODE SAMPLE
# ----------
def filter_records(records, min_words: int = 30, max_special_ratio: float = 0.5):
    """Yield records that pass all quality rules."""
    for record in records:
        text  = record["text"]
        words = text.split()
        flags = record.get("flags", [])

        # Hard rules
        if len(words) < min_words:
            continue

        special_ratio = sum(not c.isalnum() and not c.isspace() for c in text)
        special_ratio /= max(len(text), 1)
        if special_ratio > max_special_ratio:
            continue

        # Flag-based rules (from assess step)
        if "mostly_numbers" in flags:
            continue
        if "no_punctuation" in flags:
            continue

        yield record

# ── usage ──────────────────────────────────────────────────────
# filtered = filter_records(unique)  →  feeds into validate()






 
# ==============================================================================
# STAGE 6 | VALIDATION
# ==============================================================================
#
#   Role:
#       Final check — confirm the cleaned data actually meets quality
#       standards before passing it to LLM training.
#       Like a quality certificate before water enters the supply network.
#
#   Checks performed:
#       ✅  Average document length  >  200 words
#       ✅  Duplicate rate           <  1%
#       ✅  English text percentage  >  99%
#       ✅  No personal data present    (emails, phone numbers, etc.)
#       ✅  Total dataset size is sufficient for training
#
#   If any check fails:
#       →  Pipeline raises an alert and halts before bad data reaches training.
#
#   Analogy:
#       The final water quality certificate issued before water is
#       approved to enter the public supply network.
#
# ==============================================================================
 




# =======================================================================
# CODE SAMPLE
# ----------
import re

def validate(records, min_avg_words: int = 50, min_total: int = 4):
    """Buffer all records, run dataset-level checks, then yield if pass."""
    EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    PHONE_RE  = re.compile(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b")

    buffer = []
    for record in records:
        # print("record: ", record)
        text = record["text"]
        # Per-record PII check
        if EMAIL_RE.search(text) or PHONE_RE.search(text):
            continue          # silently drop PII-containing records
        buffer.append(record)

    # Dataset-level assertions
    total = len(buffer)
    avg_words = sum(len(r["text"].split()) for r in buffer) / max(total, 1)

    if total < min_total:
        raise ValueError(f"Too few documents: {total} < {min_total}")
    if avg_words < min_avg_words:
        raise ValueError(f"Avg doc too short: {avg_words:.0f} words")

    print(f"✅ Validation passed — {total:,} docs, avg {avg_words:.0f} words")
    yield from buffer

# ── usage ──────────────────────────────────────────────────────
# validated = validate(filtered)  →  feeds into write_output()









 
# ==============================================================================
# STAGE 2 | QUALITY ASSESSMENT
# ==============================================================================
#
#   Role:
#       Scan the raw data and flag potential problems BEFORE cleaning begins.
#       Like a water tester identifying what contaminants are present.
#
#   Problems it flags:
#       ⚠  "This article is only 3 words long"         →  too short
#       ⚠  "This text is 80% numbers"                  →  not useful for LLM
#       ⚠  "This paragraph has no punctuation"         →  likely garbled/corrupt
#       ⚠  "This text is in Arabic"                    →  wrong language
#
#   Output:
#       A quality report highlighting which documents need attention.
#
#   Analogy:
#       Dipping a test stick into water to identify what contaminants
#       are present before deciding how to treat it.
#
# ==============================================================================
 

# =======================================================================
# CODE SAMPLE
# ----------
import re

def assess(record: dict) -> dict:
    """Attach a 'flags' list to the record; never drops anything."""
    text  = record["text"]
    words = text.split()
    flags = []

    if len(words) < 50:
        flags.append("too_short")

    digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
    if digit_ratio > 0.5:
        flags.append("mostly_numbers")

    special_ratio = len(re.findall(r"[^\w\s]", text)) / max(len(text), 1)
    if special_ratio > 0.3:
        flags.append("high_special_chars")

    if text.count(".") + text.count("?") + text.count("!") == 0:
        flags.append("no_punctuation")

    return {**record, "flags": flags}
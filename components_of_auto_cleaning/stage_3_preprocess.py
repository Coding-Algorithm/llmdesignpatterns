# ==============================================================================
# STAGE 3 | PREPROCESSING
# ==============================================================================
#
#   Role:
#       Clean and standardize the text so it's consistent across the dataset.
#       Like filtering out visible dirt and debris from water.
#
#   Example:
#
#       BEFORE:
#           "  HELLO!!!   Visit www.spam.com 😊 <b>Click here</b>  "
#
#       AFTER:
#           "hello visit click here"
#
#   Transformations applied:
#       ✓  Lowercase all text
#       ✓  Remove extra whitespace
#       ✓  Strip HTML tags         (<b>, <div>, etc.)
#       ✓  Remove URLs             (www.spam.com)
#       ✓  Remove emojis           (😊)
#       ✓  Remove excessive punctuation
#
#   Analogy:
#       Filtering out visible dirt, leaves, and debris from water
#       before the deeper purification begins.
#
# ==============================================================================
 

# =======================================================================
# CODE SAMPLE
# ----------
import re, unicodedata, html

def preprocess(record: dict) -> dict:
    """Return record with cleaned 'text'. Original preserved as 'raw_text'."""
    text = record["text"]
    text = html.unescape(text)                        # & → &
    text = re.sub(r"<[^>]+>", " ", text)            # strip HTML tags
    text = re.sub(r"https?://\S+", "", text)        # strip URLs
    text = re.sub(r"[^\x00-\x7F]+", " ", text)      # strip non-ASCII
    text = re.sub(r"[!?.,]{2,}", ".", text)          # collapse punc runs
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()          # normalise whitespace

    return {**record, "raw_text": record["text"], "text": text}

# ── usage ──────────────────────────────────────────────────────
# cleaned = (preprocess(r) for r in assessed)  →  feeds into deduplicate()









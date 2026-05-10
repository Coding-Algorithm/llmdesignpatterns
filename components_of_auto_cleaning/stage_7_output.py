# ==============================================================================
# STAGE 7 | OUTPUT
# ==============================================================================
#
#   Role:
#       Save the cleaned data in a format the LLM training pipeline
#       can efficiently read and load.
#       Like bottling clean water into standard containers for distribution.
#
#   Input:
#       Messy .xml, .json, .html files from various raw sources
#
#   Output formats:
#       .parquet  →  fast, compressed, best for large datasets
#       .jsonl    →  one clean document per line, easy to stream
#       .txt      →  plain text, simple and universally compatible
#
#   Analogy:
#       Bottling purified water into standard, labeled containers
#       ready for distribution and use.
#
# ==============================================================================
 


# =======================================================================
# CODE SAMPLE
# ----------
import json
from pathlib import Path

def write_output(records, out_path: str = "clean_data.jsonl") -> int:
    """Write one clean doc per line. Returns count written."""
    out = Path(out_path)
    count = 0
    with out.open("w", encoding="utf-8") as f:
        for record in records:
            line = {"text": record["text"], "source": record["source"]}
            f.write(json.dumps(line) + "\n")
            count += 1
    print(f"📦 Wrote {count:,} records → {out_path}")
    return count






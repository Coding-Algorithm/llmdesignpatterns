# ==============================================================================
# STAGE 1 | DATA INGESTION
# ==============================================================================
#
#   Role:
#       Collect and load raw data from various sources into the pipeline.
#       Think of it as a truck collecting water from different rivers and lakes.
#
#   Sources:
#       - Wikipedia dump     →  large .xml files (~20GB)
#       - Reddit comments    →  .json files
#       - Books              →  .txt files
#       - Websites           →  scraped HTML
#
#   What happens:
#       All sources  →  loaded  →  unified pipeline
#
#   Analogy:
#       A truck collecting water from different rivers and lakes,
#       bringing it all to one central processing plant.
#
# ==============================================================================
 


# =======================================================================
# CODE SAMPLE
# ----------
import json, glob
from pathlib import Path
from typing import Iterator

def ingest(sources: dict[str, list[str]]) -> Iterator[dict]:
    """Yield raw records from every source as {"text": ..., "source": ...}"""
    print('sources --- ', sources)
    for file in sources.get("txt", []):
        text = Path(file).read_text(encoding="utf-8", errors="ignore")
        yield {"text": text, "source": file}

    for file in sources.get("jsonl", []):
        with open(file) as f:
            for line in f:
                obj = json.loads(line)
                yield {"text": obj.get("text", ""), "source": file}

    for pattern in sources.get("glob", []):
        for file in glob.iglob(pattern, recursive=True):
            text = Path(file).read_text(errors="ignore")
            yield {"text": text, "source": file}

# ── usage ──────────────────────────────────────────────────────
# sources = {
#   "txt":  ["books/war_and_peace.txt"],
#   "jsonl": ["reddit/comments.jsonl"],
#   "glob": ["wiki/**/*.txt"],
# }
# stream = ingest(sources)  →  feeds into assess()











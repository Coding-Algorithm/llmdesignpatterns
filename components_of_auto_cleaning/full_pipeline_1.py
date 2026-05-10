from stage_1_ingest           import ingest
from stage_2_assess           import assess
from stage_3_preprocess       import preprocess
from stage_4_deduplicate      import deduplicate
from stage_5_filter           import filter_records
from stage_6_validate         import validate
from stage_7_output           import write_output



sources = {
    "txt":   ["data/war_and_peace.txt", "data/french_revolution.txt", "data/neural_networks.txt"],
    "jsonl": ["data/comments.jsonl"],
}

total = write_output(
    validate(
        filter_records(
            deduplicate(
                preprocess(r)
                for r in (
                    assess(raw)
                    for raw in ingest(sources)
                )
            )
        )
    ),
    out_path="clean_data.jsonl",
)

# Feed into your training loop:
# for line in open("clean_data.jsonl"):
#     record = json.loads(line)
#     trainer.feed(record["text"])
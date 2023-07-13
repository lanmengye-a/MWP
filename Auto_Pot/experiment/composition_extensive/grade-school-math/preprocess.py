import json
with open("test_raw.jsonl", "r") as reader:
    lines = reader.readlines()
    lines = [json.loads(line) for line in lines]
import re
with open("test.jsonl", "a+") as writer:
    for item in lines:
        itemms = {}
        itemms["question"] = item["question"]
        item["gold_ans"]= item["answer"].split("####")[-1].strip()
        itemms["gold_ans"] = item["gold_ans"]
        writer.write(json.dumps(itemms)+"\n")

import json
import re
with open("test_raw.jsonl") as reader:
    lines = reader.readlines()
    lines = [json.loads(line) for line in lines]
with open("test.jsonl", "a+") as writer:
    for idx,line in enumerate(lines):
        itemms = {}
        itemms["question"] = line["question"]
        answer = line["correct"]
        for item in line["options"]:
            if answer in item:
                itemms["gold_ans"] = item.split(")")[1].strip()
        writer.write(json.dumps(itemms)+"\n")

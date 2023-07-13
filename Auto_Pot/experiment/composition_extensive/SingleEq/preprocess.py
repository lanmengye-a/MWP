import json
with open("questions.json","r") as reader:
    lines = reader.read()
    lines = json.loads(lines)
with open("questions.jsonl", "a+") as writer:
    itemm = {}
    for item in lines:
        itemm["index"] = item["iIndex"]
        itemm["question"] = item["sQuestion"]
        itemm["gold_ans"] = item["lSolutions"]
        itemm["Equation"] = item["lEquations"]
        writer.write(json.dumps(itemm)+"\n")


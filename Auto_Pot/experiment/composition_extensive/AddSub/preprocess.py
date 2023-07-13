import json
with open("AddSub.json","r") as reader:
    lines = reader.read()
    lines = json.loads(lines)
with open("AddSub.jsonl", "a+") as writer:
    itemm = {}
    for item in lines:
        itemm["index"] = item["iIndex"]
        itemm["question"] = item["sQuestion"]
        itemm["gold_ans"] = item["lSolutions"]
        itemm["Equation"] = item["lEquations"]
        writer.write(json.dumps(itemm)+"\n")


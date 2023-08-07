import json
with open("svamp_autopot_programseed1_5.jsonl") as reader:
    lines=reader.readlines()
    lines=[json.loads(line) for line in lines]
correct = 0
for item in lines:
    if item["Prediction"] == item["Answer"]:
        correct+=1
print(correct/len(lines))

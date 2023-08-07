import json
with open("dataset/demos/svamp/demo8_test1.json","r") as reader:
    demo=json.load(reader)
with open("dataset/svamp/svamp_test.jsonl","r") as reader:
    lines = reader.readlines()
    testData = [json.loads(line) for line in lines]

items = []
for item in demo:
    t = testData[item["Index"]]
    gold_ans = t["Answer"]
    item["gold_ans"] = gold_ans
    item["question"] = t["Question"]
    items.append(item)
with open("dataset/demos/svamp/demo8_test.json","w") as writer:
    writer.write(json.dumps({"demo":items},indent=4))
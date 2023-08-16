import json
with open("self_ask_8demo.jsonl") as reader:
    lines = reader.readlines()
    for line in lines:
        line = json.loads(line)
        print(line["Question"])
        print(line["Prediction"])
        print(line["Answer"])
        print(line["Program"])
        input("1 or 0?")
import json

correct = 0

with open("self_ask_2_100_Yes"
          ""
          "2_1.jsonl") as reader:
    lines = reader.readlines()
    # lines = [json.loads(line) for line in lines]
    for line in lines[20:]:
        line = json.loads(line)
        print(line["Question"])
        print(line["Prediction"])
        print(line["Answer"])
        print(line["Program"])
        input("1 or 0?")
# for line in li1nes:
#     if line["Prediction"] == line["Answer"]:
#         correct += 1
# print(correct)
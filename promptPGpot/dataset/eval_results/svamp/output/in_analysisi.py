import json
import re
import collections
import pandas as pd
dic = collections.defaultdict(list)
with open("dataset/eval_results/svamp/output/self_ask_2_100_1.jsonl") as reader:
    lines = reader.readlines()
    Nos = [json.loads(line) for line in lines]
with open("dataset/eval_results/svamp/output/self_ask_2_100_Yes_1.jsonl") as reader:
    lines = reader.readlines()
    Yess = [json.loads(line) for line in lines]
items = []
for No,Yes in zip(Nos,Yess):
    item = {}
    if No["Question"] != Yes["Question"]:
        break
    question = No["Question"]
    ques = re.split("\.|\,", question)[-1]
    body = re.split("\.|\,", question)[:-1]
    body = ".".join(body)
    item["Question"] = question
    item["Body"] = body
    item["Len"] = len(ques)
    if No["Prediction"] != No["Answer"]:
        item["Nos"] = 0
    else:
        item["Nos"] = 1
    if Yes["Prediction"] != Yes["Answer"]:
        item["Yess"] = 0
    else:
        item["Yess"] = 1
    items.append(item)
df=pd.DataFrame(items)
df.to_excel("dataset/eval_results/svamp/output/svamp_selfask.xlsx")
import json

with open("svampexpFormula_80_test_TQ-SA_2_seed_2.json","r") as reader:
    reader = json.load(reader)
results=reader["results"]
dic = {}
for idx,item in results.items():
    item["Question"]=item["Question"].split("Question:")[-1]
    if item["Answer"] != item["prediction"]:
        dic[idx] = item
        # del dic[idx]["prompt"]
        del dic[idx]["shot_pids"]
with open("svampexpFormula_inspect.json","w") as writer:
    writer.write(json.dumps(dic,indent=4))

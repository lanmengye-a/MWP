import json
count = 0
total = 0
with open("svampexpFormula_inspect.json") as reader:
    reader = json.load(reader)
    for line in reader.values():
        if not line["rawEquation"]:
            count += 1
        else:
            total += 1
print(count/total,count,total)
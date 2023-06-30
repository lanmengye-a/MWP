import json
with open("svamp_inspect.jsonl","r") as reader:
    for line in reader:
        line = json.loads(line)
        for k,v in line.items():
            print(k,":",v)
        input("read")

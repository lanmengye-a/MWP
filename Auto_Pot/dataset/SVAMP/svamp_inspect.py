import json
with open("SVAMP_AutoCot.jsonl","r") as reader:
    with open("SVAMP_AutoCot_inspect.jsonl","w") as writer:
        for line in reader:
            line = json.loads(line)
            print(line["quesiton"],"\n",line["relationles"],"\n",line["pred_ans"],"\n",line["gold_ans"])
            print("--------------------------------------------------")
            jd = input("1 or 0")
            if(jd == "0"):
                writer.write(json.dumps(line))
                writer.write("\n")
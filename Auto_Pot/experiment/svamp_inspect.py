import json
with open("svamp2.jsonl","r") as reader:
    correct = 0
    with open("svamp_inspect.jsonl","a+") as writer:
        for idx,line in enumerate(reader):
            if (idx == 99):
                print(correct)
                break
            line = json.loads(line)
            print("question:",line["question"].strip("\n"))
            print("rationale:",line["rationale"])
            print("gold_ans:",line["gold_ans"])
            print("pred_ans:",line["pred_ans"])
            jd = input("1 or 0 ")
            if(jd == "1"):
                correct += 1
            else:
                writer.write(json.dumps(line))
                writer.write("\n")


import json

# with open("svamp_inspect_follow_up_inspect.jsonl", "r") as f:
#     lines = f.readlines()
#     f=[json.loads(line) for line in lines]
with open("svamp_out.jsonl","r") as reader:

        correct = 0
        with open("svamp_inspect.jsonl","a+") as writer:
            for idx,line in enumerate(reader):
                line = json.loads(line)
                # l= f[idx]
                print("question:",line["question"].strip("\n"))
                # print("rationale:", l["rationale"])
                # print("pred_ans:",l["pred_ans"])
                print("Program:", line["program"])
                print("Ans:", line["Ans"])
                print("gold_ans:", line["gold_ans"])
                jd = input("1 or 0 ")
                if(jd == "1"):
                    correct += 1
                else:
                    writer.write(json.dumps(line))
                    writer.write("\n")
        print(correct)


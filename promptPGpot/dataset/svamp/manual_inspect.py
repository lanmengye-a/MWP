import json
from tool import safe_execute, floatify_ans,finqa_equal
correct= 1
from tools.tool import finqa_equal
with open("manualpot_8seed1.jsonl","r") as reader:
    with open("svamp_error.jsonl","a+") as writer:
        # for line in reader:
        #     data = json.loads(line)
        #     # ans = safe_execute(data["executed"])
        #     # ans = floatify_ans(ans)
        #     if  finqa_equal(data["Prediction"],data["Answer"]):
        #         correct += 1
        # print(correct)
        for line in reader:
            data = json.loads(line)
            print(data["Question"],"\n",data["Program"],'\n',data["Prediction"],"\n",data["Answer"])
            number=input("1 or 0")
            if number=="0":
                writer.write(json.dumps(data) + '\n')
import random

import numpy as np
import json
from annotated_demos.auto_annotated.self_ask.annotated import get_rationales
# get_rationales 有answer self-teaching
# MODE = "ZERO" # "FEW"
# MODE = "ONE" # "FEW"
# DEMO_DIR = None
# dem_dir 和上面的get_rationales 导入的库位置对应
MODE= "FEW"
DEMO_DIR = "dataset/demos/svamp/self_ask_8demo.jsonl"

def testdata(output_dir, input_data,cand):
    correct_list = []
    total = 0
    with open(output_dir, "a") as wp:
        cnt = 0
        for i, data in enumerate(input_data):
            if i not in cand:
                continue
            output_line = {}
            print('*************************')
            cnt += 1
            print("{}st data".format(cnt))
            # Prepare question template ...
            x, y = data["Question"], data["Answer"]
            output_line["Question"] = x
            output_line["Answer"] = y
            # few_prompt = MATH_PROMPT
            if MODE == "ZERO":
                few_prompt = None
                answer = y
            elif MODE == "FEW":
                answer = None
                from annotated_demos.auto_annotated.self_ask.one_prompt import MATH_PROMPT
                few_prompt = MATH_PROMPT
                # with open(DEMO_DIR) as reader:
                #     lines = reader.readlines()
                #     few_prompt= [json.loads(line)["Program"] for line in lines]
                # few_prompt = "\n".join(few_prompt)
            else:
                from annotated_demos.auto_annotated.self_ask.one_prompt import MATH_PROMPT
                few_prompt = MATH_PROMPT
                answer = y

            z = get_rationales(x, few_prompt,answer)
            output_line["Program"] = z[1]
            pred = z[0]
            output_line["Prediction"] = z[0]
            # output_line["wrap_que"] = x

            output_json = json.dumps(output_line, skipkeys=True)
            wp.write(output_json + '\n')

            # Choose the most frequent answer from the list ...
            print("pred : {}".format(pred))
            print("GT : " + str(y))
            print('*************************')

            # Checking answer ...
            correct = (np.array([pred]) == np.array([y])).sum().item()
            correct_list.append(correct)
            total += 1  # np.array([y]).size(0)

    # Calculate accuracy ...
    accuracy = (sum(correct_list) * 1.0 / total) * 100
    print("accuracy : {}".format(accuracy))
if __name__ == "__main__":
    # input_dir = "dataset/demos/svamp/demo8_train.json"
    input_dir = "dataset/svamp/svamp_test.jsonl"
    # input_dir = "dataset/eval_results/svamp/output/self_ask_2_100_Yes_1.jsonl"
    with open(input_dir) as reader:
        if input_dir.endswith("jsonl"):
            lines = reader.readlines()
            inputdata = [json.loads(line) for line in lines]
        else:
            inputdata = json.loads(reader.read())
    # output_dir = "dataset/eval_results/svamp/output/selfaskpot_8" + "seed" + str(random_seed) +"_"+one_prompt+ '.jsonl'
    if MODE == "ZERO" or MODE == "ONE":
        inputdata = inputdata["demo"]
        idxs = [i for i in range(len(inputdata))]
        cand = idxs
        output_dir = "dataset/demos/svamp/self_ask_8" + "demo" + '.jsonl'
    else:
        idxs = [i for i in range(len(inputdata))]

        random_seed = 1
        cand = random.sample(idxs,100)
        cand = idxs
        # output_dir = "dataset/eval_results/svamp/output/self_ask_2" + "_1000_" + str(random_seed) + '.jsonl'
        output_dir = "dataset/eval_results/svamp/output/self_ask_2" + "_1000_Yes" '.jsonl'
    testdata(output_dir, inputdata,cand)
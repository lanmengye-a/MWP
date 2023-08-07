import random

import numpy as np

from annotated_demos.mannual_pot.utilities1 import get_gpt3_output
from math_prompts import MATH_PROMPT
import json


def get_rationales(question, few_prompt):
    prefix = """
# Read the following passages to answer questions with Python code,store the result as a 'ans' variable:
"""
    midfix = f"""
# Question: {question}
# Program:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
"""
    if few_prompt is not None:
        message = prefix + "\n\n" + few_prompt.strip() + "\n\n" + midfix + "\n"
    program, prediction = get_gpt3_output(message, 1,midfix)

    return prediction, program


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

            # print(x, y)

            output_line["Question"] = x
            output_line["Answer"] = y
            few_prompt = MATH_PROMPT
            z = get_rationales(x, few_prompt)
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

    with open("dataset/svamp/svamp_test.jsonl") as reader:
        lines = reader.readlines()
        svamp_demos = [json.loads(line) for line in lines]

    random_seed = 1
    one_prompt = "addprefix"
    output_dir = "dataset/eval_results/svamp/svamp_selfask_program" + "seed" + str(random_seed) +"_"+one_prompt+ '.jsonl'
    idxs = [i for i in range(len(svamp_demos))]
    cand = random.sample(idxs,100)
    testdata(output_dir, svamp_demos,cand)

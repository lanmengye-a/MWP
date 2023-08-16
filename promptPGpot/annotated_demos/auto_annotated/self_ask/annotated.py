import random

import numpy as np

from tools.utilities1 import get_gpt3_output
from annotated_demos.auto_annotated.self_ask.one_prompt import MATH_PROMPT
import json
def get_rationales(question,few_prompt=None,answer=None,follow_up="Yes"):
    import re
    lis = re.split("\.|\,", question)
    ques = lis[-1]
    body = lis[:-1]
    body = ".".join(body)
    prefix = \
        "# Read the following passages to answer questions with Python code,store the result as a 'ans' variable" \
        "\n# if followed up question needed,there are at least 2 '# Follow up:' " \
        f"\n# the last one is  '# Follow up:{ques}' "

    midfix = f"""
# Passage: {body}
# Question:{ques}
# Thought:
import numpy as np
# Are follow up questions needed here:{follow_up}.
# According to the question, we can define the variable:
"""
    if few_prompt is not None:
        message = prefix.strip("\n") +"\n\n"+few_prompt.strip()+"\n\n"+midfix.strip("\n") +"\n"
    else:
        message = prefix.strip("\n") + "\n\n" + midfix.strip("\n")  + "\n"
    program,prediction=get_gpt3_output(message,5,midfix,answer)
    return prediction, program

if __name__ == "__main__":
    from annotated_demos.utils import testdata
    with open("dataset/demos/svamp/demo8_train.json") as f:
        files = json.load(f)
        svamp_demos = files["demo"]
    new_demos = [{"Question":item["question"],"Answer":item["gold_ans"],"index":item["index"]} for item in svamp_demos]
    one_prompt = "addprefix"
    output_dir = f"dataset/demos/svamp/svamp_selfask_program" + f"demoFtestdata"+'.jsonl'
    testdata(output_dir,new_demos)

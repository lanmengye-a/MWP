import json

import pandas as pd
import re

def replace_numbers_with_variables(data):
    body = data["Question"]
    equation = data["Equation"]
    variables = []
    var_counter = ord('a')
    body_vars = re.findall(r'\d+', body)
    for i, num in enumerate(body_vars):
        #var_name = chr(var_counter)
        var_name = f"number{i}"
        # 这里要改成依次出现 第二次重复出现的数字也要重新命名
        # 只替换第一次出现的数字
        body = body.replace(num, var_name, 1)
        # body = body.replace(num, var_name)
        equation = equation.replace(num, var_name)
        # 删除equation中字母+-*/()除外的内容
        equation = equation.replace(".0","")
        equation = equation.replace(" ", "")
        variables.append(str(float(num)))
        var_counter += 1
    data["Question"] = body
    data["infixEquation"] = equation
    data["Numbers"] = " ".join(variables)
    return data
if __name__ == "__main__":
    with open("svampformula_test.jsonl","w") as writer:
        with open("svamp_test.json") as reader:
            data = json.load(reader)
        for item in data:
            item = replace_numbers_with_variables(item)
            writer.write(json.dumps(item)+"\n")
# data = {
#     "ID": "chal-3",
#     "Body": "Paco had 26 salty cookies and 17 sweet cookies. He ate 14 sweet cookies and 9 salty cookies.",
#     "Question": "How many salty cookies did Paco have left?",
#     "Equation": "( 26.0 - 9.0 )",
#     "Answer": 17.0,
#     "Type": "Subtraction"
# }
#
# updated_data = replace_numbers_with_variables(data)
#
# print("Updated Data:")
# print(updated_data)


# if __name__ == '__main__':

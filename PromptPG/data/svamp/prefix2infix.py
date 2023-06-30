# 去除字符串中间的空格
import json

import pandas as pd
import sympy


def remove_space(expression):
    expression = expression.replace(" ", "")
    return expression

def replace_variate(expression):
    # 将expression中的变量number#替换为a-z
    var_arr = []
    for i in range(10):
        expression = expression.replace(f"number{i}", chr(97+i))
        var_arr.append(chr(97 + i))
    return expression,var_arr
    # expression = expression.replace("number0", "a")


def prefix_to_infix(expression):
    expression = remove_space(expression)
    expression,var_arr = replace_variate(expression)
    stack = []
    # 从右到左遍历前缀表达式
    for char in reversed(expression):
        # 如果是操作数，将其推入栈中
        if char.isalnum():
            stack.append(char)
        # 如果是运算符，从栈中弹出两个操作数并构建中缀表达式
        else:
            operand1 = stack.pop()
            operand2 = stack.pop()
            infix = "(" + operand1 + char + operand2 + ")"
            stack.append(infix)

    # 最后栈中剩下的元素就是中缀表达式
    return stack.pop(),var_arr

def calculate(var_arr,args,expression):
    var_str = " ".join(var_arr)
    var = sympy.symbols(var_str)
    if (len(var) == 1):
        var = [var]
    dic = zip(var, args)
    # 字符串转sym表达式
    expression = sympy.sympify(expression)
    result = expression.subs(dic)
    return result


if __name__ == '__main__':
    # 测试示例
    df = pd.read_excel("train.xlsx")
    # 变量df中每个值
    df["Numbers"] = df["Numbers"].astype(str)
    with open("svampformula_train.jsonl", "a+", encoding="utf-8") as writer:
        for i in range(len(df)):
            prefix_expression = df.loc[i,"Equation"]
            try:
                infix_expression,var_arr = prefix_to_infix(prefix_expression)
                args = df.loc[i, "Numbers"].split(" ")
                result = calculate(var_arr, args, infix_expression)
                # infix_expression 中的变量a-z依次替回number0-number9
                # infixExpressionNumber = restore_variate(infix_expression)

            except:
                continue

            # 保留浮点数后两位小数
            result = round(result,2)

            print("中缀表达式计算结果:", result)
            print("正确结果:",df.loc[i,"Answer"])
            judge = input("结果是否正确")
            if(judge == "1"):
                # 取df中第i行的数据
                dic = df.loc[i,:].to_dict()
                dic["Index"] = i
                dic["infixEquation"] = infix_expression
                # dic["infixEquation"] = infixExpressionNumber
                writer.write(json.dumps(str(dic))+"\n")
            else:
                continue



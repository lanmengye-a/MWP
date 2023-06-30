import re
import random
import time
from functools import lru_cache

import numpy as np
import sympy

import chatgpt0

random.seed(123)

def replace_variate(expression):
    # 将expression中的变量number#替换为a-z
    var_arr = []
    for i in range(10):
        expression = expression.replace(f"number{i}", chr(97+i))
        var_arr.append(chr(97 + i))
    return expression,var_arr
    # expression = expression.replace("number0", "a")


def get_gpt3_output(prompt, args, numbs, pidId):
    algebraicPrompt = "Write a mathematical equation and generate the answer format starting with `Answer =' Attention there is a equation which could include mutiple variates "
    patience = 3

    while True:
        try:
            raw_formula = call_gpt3(prompt, algebraicPrompt, args.engine)
            if raw_formula == False:
                raise Exception("there is some error in call_gpt3")
            formula = normalize_formula(raw_formula)
            if formula == False:
                raise Exception("there is some error in normalize_formula")
            output = extract_prediction(formula, numbs)
            if output == False:
                raise Exception("there is some error in extract_prediction")
            output = normalize_answer(output)
            # check!!!
            # return formula,output
            return raw_formula, formula, output
        except Exception as e:

            #判断错误类型
            patience -= 1
            if patience == 0:
                # print("there is some error ", pidId, ":", raw_formula,formula)
                if e == "there is some error in call_gpt3":
                    return False, False, False
                elif e == "there is some error in normalize_formula":
                    return raw_formula, False, False
                else:
                    return raw_formula, formula, False
            else:
                time.sleep(5)

@lru_cache(maxsize=10000)
def call_gpt3(prompt, algebraicPrompt, engine):
    message = algebraicPrompt + "\n\n" + prompt
    reply = chatgpt0.call_gpt3(engine, message)
    return reply

def score_string_similarity(str1, str2):
    if str1 == str2:
        return 2.0
    if " " in str1 or " " in str2:
        str1_split = str1.split(" ")
        str2_split = str2.split(" ")
        overlap = list(set(str1_split) & set(str2_split))
        return len(overlap) / max(len(str1_split), len(str2_split))
    else:
        if str1 == str2:
            return 1.0
        else:
            return 0.0


def extract_prediction(formula,numbs):
    try:
        args = str(numbs).split()
        size = len(args)
        var_arr = []
        for i in range(size):
            var_arr.append(chr(97 + i))
        var_str = " ".join(var_arr)
        var = sympy.symbols(var_str)
        if (len(var) == 1):
            var = [var]
        dic = zip(var, args)
        # 将formula 转为sympy表达式
        formula = sympy.sympify(formula)
        result = formula.subs(dic)
        return result
        raise
    except Exception as e:
        return False

def normalize_formula(formula):
    try:

        formula = formula.split("Answer =")[1]
        formula = formula.strip(".")
        formula = formula.replace(" ", "")
        formula, vars = replace_variate(formula)
        formula = re.findall(r"(\([\da-z\+\-*\/()]+\))", formula)[0]
    except Exception as e:
        return False
    return formula


def normalize_answer(text):
    # ["1,000", "123", "3/4", "56.456", "$56.4", "-3", "-10.02", "-3/2"]
    if not isinstance(text, str):
        text = str(text)  # 将非字符串对象转换为字符串
    text = re.sub("^[\$]", "", text)
    text = re.sub("[\,\.\,\/]$", "", text)
    result = re.match("^[-+]?[\d,./]+$", text)

    if result is not None:
        # is number?
        text = text.replace(",", "")
        result = re.match("[-+]?\d+$", text)
        try:
            if result is not None:
                number = int(text)
            elif "/" in text:
                nums = text.split("/")
                number = round(float(nums[0]) / float(nums[1]), 3)
            else:
                number = round(float(text), 3)
            number = str(number)
            number = re.sub(r"\.[0]+$", "", number)
            return number
        except:
            return text



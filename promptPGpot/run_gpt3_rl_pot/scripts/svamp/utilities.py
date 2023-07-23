import re
import random
from functools import lru_cache

import numpy as np
import chatgpt0
import time
random.seed(123)

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


def extract_prediction(output, options, option_inds):
    # $\\frac{16}{95}$ -> 16/95
    output = re.sub(r"\$?\\frac\{([\d\.\,\-]+)\}\{([\d\.\,]+)\}\$?", r"\1/\2", output)

    output = re.sub(r"(?<![AP]\.M)\.$", "", output)
    output = re.sub(r"(?<=\d)[\=](?=[\-\$\d])", " = ", output)
    output = re.sub(r"\u2212", "-", output)

    ## Multi-choice questions
    if options:
        patterns = [
            r'^\(([A-Za-z])\)$',  # "(b)", "(B)"
            r'^([A-Za-z])$',  # "b", "B"
            r'^([A-Za-z]). ',  # "b", "B"
            r'[Th]he answer is ([A-Z])',  # "The answer is B"
            r'^\(([A-Za-z])\) [\s\S]+$',  # "(A) XXXXX"
            r'[Th]he answer is \(([A-Za-z])\) [\s\S]+$',  # "The answer is (B) XXXXX."
        ]

        # have "X" in the output
        for p in patterns:
            pattern = re.compile(p)
            res = pattern.findall(output)
            if len(res) > 0:
                pred = res[0].upper()  # e.g., "B"
                if pred in option_inds:
                    ind = option_inds.index(pred)  # 1
                    if ind >= len(options):
                        ind = random.choice(range(len(options)))
                    predition = options[ind]
                    return predition

        # find the most similar options
        scores = [score_string_similarity(x, output) for x in options]
        max_idx = int(np.argmax(scores))  # json does not recognize NumPy data types
        predition = options[max_idx]
        return predition

    else:
        ## free_text QA problems, numeric answer
        patterns = [
            # r'^\([A-Za-z]\) ([\s\S]+)$', # "(A) XXXXX"
            # r'[Th]he answer is \([A-Za-z]\) ([\s\S]+)$', # "The answer is (B) XXXXX."
            r'[Th]he answer is ([\s\S]+)$',  # "The answer is XXXXX.",
            r'[Th]he table shows that ([\d\$\.\,\/\:]+) ',
            r' = ([\d\$\.\,\/\:]+)',  # "= $1.40"
            r'(?<= be| is) ([\-\d\$\.\,\/\:]{0,}[\d]+)',  # "will be $1.40"
            r'(?<= are| was) ([\-\d\$\.\,\/\:]{0,}[\d]+)',  # "are $1.40"
            r'(?<= were) ([\-\d\$\.\,\/\:]{0,}[\d]+)',  # "are $1.40"
            r' ([\d\$\.\,\/\:]+ [AP]\.M\.)',  # 7:25 P.M.
            r'([\-\d\$\.\,\/\:]{0,}[\d]+)',  # 14.5
        ]

        for p in patterns:
            pattern = re.compile(p)
            res = pattern.findall(output)
            if len(res) > 0:
                predition = res[-1].strip()
                if predition.endswith(".") and ".M." not in predition:
                    predition = predition[:-1]
                return predition

    return output


def normalize_answer(text, unit):
    # ["1,000", "123", "3/4", "56.456", "$56.4", "-3", "-10.02", "-3/2"]

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
    else:
        # is text
        if unit:
            text = text.replace(unit, "").strip()
        return text

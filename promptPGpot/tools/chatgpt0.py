import argparse
import collections
import time

import openai

from tools.tool import parse_api_result, safe_execute, floatify_ans

openai.api_key = "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"
train_sample =[
    {
        "infixEquation":"Answer=number1+number2",
       "Question":"Tiffany was collecting cans for recycling. On monday she had number0 bags of cans. She found number1 bags of cans on the next day and number2 bags of cans the day after that.How many bags did she find after monday?"
    # "false_infixEquation":"Answer = (number0-number2)"
},
    {
        "infixEquation": "Answer=number0+number1+number2",
        "Question":"Tiffany was collecting cans for recycling. On monday she had number0 bags of cans. She found number1 bags of cans on the next day and number2 bags of cans the day after that.How many bags did she find ?"

    },
    {
        "Question":"At lunch a waiter had number0 customers and number1 of them did n't leave a tip . If he got $ number2 each from the ones who did tip , how much money did he earn ?",
        "infixEquation":"Answer = number2*(number0-number1)"
    }
    # {
    #     "Question":"Mary is baking a cake. The recipe calls for number0 cups of sugar and number1 cups of flour. She already put in number2 cups of flour and number3 cups of sugar.How many more cups of sugar does she need to add?",
    #     "infixEquation":"Answer = (number0-number3)",
    # }
]
algebraicPrompt = "Write a mathematical equation and generate the answer format starting with `Answer =' Attention there is a equation which could include mutiple variates "
def call_gpt3( prompt,engine="text-davinci-002"):
    response = openai.Completion.create(engine=engine,
                                        prompt=prompt,
                                        temperature=0.5,
                                        max_tokens=256,
                                        n=30,
                                        logprobs=1,
                                        # frequency_penalty=frequency_penalty,
                                        # presence_penalty=presence_penalty,
                                        stop=["\n\n"]
                                        )

    return response

def call_gpt30( engine,prompt):

    patience = 3
    while True:
        try:

            response = openai.Completion.create(engine=engine,
                                                prompt=prompt,
                                                temperature=0.5,
                                                # max_tokens=max_tokens,
                                                # top_p=top_p,
                                                # frequency_penalty=frequency_penalty,
                                                # presence_penalty=presence_penalty,
                                                stop=["\n"]
                                                )
            output = response["choices"][0]["text"].strip()
            break
        except Exception as e:
            print(e)
            patience -= 1
            if not patience:
                print("!!! running out of patience waiting for OpenAI")
            else:
                time.sleep(0.1)
    return output

def chatgpt(message):
    try:
        message = "\n\n".join([f"Question: {sample['Question']}\ninfixEquation: Answer={sample['infixEquation']}" for sample in
                              train_sample]) + "\n\n" + f"Question: {que}\ninfixEquation: "++ "\n\n"+algebraicPrompt
                  # + "\n\n" \
                  # + algebraicPrompt
         # message = [{"role":"user","content":message}]
        if message:
            response = openai.ChatCompletion.create(
                 model="gpt-3.5-turbo",
                # engine = "text-davinci-002",
                messages=message,
                #prompt = message,
                # top_p=args.top_p,

            )
            reply = response["choices"][0]["text"].strip()
            print(f"ChatGPT: {reply}")
            return reply
    except Exception as e:
        print(e)
        return False

    #print(f"ChatGPT: {reply}")
    # messages.append({"role": "assistant", "content": reply})
    # return reply
if __name__=="__main__":
    # GPT-3 settings
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, default='text-davinci-002', choices=['text-davinci-002', 'ada'])
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--max_tokens',
                        type=int,
                        default=512,
                        help='The maximum number of tokens allowed for the generated answer.')
    parser.add_argument('--top_p', type=float, default=1.0)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)
    args = parser.parse_args()
    # que="Frank made number0 dollars mowing lawns over the summer . If he spent number1 dollars buying new mower blades , how many number2 dollar games could he buy with the money he had left ?"
    # reply =chatgpt(que,args)
    # que = "Tiffany was collecting cans for recycling. On monday she had number0 bags of cans. She found number1 bags of cans on the next day and number2 bags of cans the day after that.How many bags did she find after monday?"
    # que ="After eating a hearty meal they went to see the Buckingham palace. There, Rachel learned that number0 visitors came to the Buckingham palace on the previous day. If there were number1 visitors on that dayHow many visited the Buckingham palace within number2 days?"
    #que = "A chef needs to cook number0 potatoes . He has already cooked number1 . If each potato takes number2 minutes to cook , how long will it take him to cook the rest ?"
    # que = "Frank made number0 dollars mowing lawns over the summer . If he spent number1 dollars buying new mower blades , how many number2 dollar games could he buy with the money he had left ?"
    # que ="There are number0 students trying out for the school 's trivia teams . If number1 of them did n't get picked for the team and the rest were put into number2 groups , how many students would be in each group ?"
    # que = "At the town carnival Billy rode the ferris wheel number0 times and the bumper cars number1 times . If each ride cost number2 tickets , how many tickets did he use ?"
    # que = "My car gets number0 miles per gallon of gas . If Grandma \u2019 s house is number1 miles away , how many gallons of gas would it take to get to her house ?"
    # que = "Paul had saved up number0 dollars . If he received another number1 dollars for his allowance , how many number2 dollar toys could he buy ?"
    que = "Billy was organizing his baseball cards in a binder with number0 on each page . If he had number1 new cards and number2 old cards to put in the binder , how many pages would he use ?"
    message = algebraicPrompt+ "\n\n" +"\n\n".join(
        [ f"Question: {sample['Question']}\ninfixEquation: {sample['infixEquation']}" for sample in
         train_sample]) + "\n\n" + f"Question: {que}\ninfixEquation: "
    DEMO_DIR = "dataset/demos/svamp/self_ask_8demo.jsonl"
    import json
    prefix = \
        "# Read the following passages to answer questions with Python code,store the result as a 'ans' variable" \
        "\nif followed up question needed,there are at least 2 '# Follow up:' " \
        "\nfinal is  '# Follow up:How much more money did she collect at the atm than she spent at the supermarket?' "
    with open(DEMO_DIR) as reader:
        lines = reader.readlines()
        few_prompt = [json.loads(line)["Program"] for line in lines]
    few_prompt = "\n".join(few_prompt)
    ques = """
# Passage: There were 3 dollars in Olivia's wallet. She collected 49 more dollars from an atm. After she visited a supermarket there were 49 dollars left
# Question:How much more money did she collect at the atm than she spent at the supermarket?
# Thought:
import numpy as np
# According to the question, we can define the variable:
wallet = 3
atm = 49
supermarket = 49
# Are followed up question needed here:Yes
"""
    prefix = \
        "# Read the following passages to answer questions with Python code,store the result as a 'ans' variable" \
        "\nif followed up question needed,there are at least 2 '# Follow up:' " \
        "\nfinal is  '# Follow up:How many peaches does Jill have?' "
    with open(DEMO_DIR) as reader:
        lines = reader.readlines()
        few_prompt = [json.loads(line)["Program"] for line in lines]
    few_prompt = "\n".join(few_prompt)
    ques = """
# Passage: Jake has 18 fewer peaches than Steven who has 13 more peaches than Jill. Steven has 19 peaches
# Question:How many peaches does Jill have?
# Thought:
import numpy as np
# According to the question, we can define the variable:

    """
    message = prefix+"\n"+few_prompt+"\n\n"+ques
    result = call_gpt3( message)
    codes = parse_api_result(result)
    result_counter = collections.Counter()
    result_dict = collections.defaultdict(list)
    for idx, r in enumerate(codes):
        r = ques+r
        ans = safe_execute(r)
        ans = floatify_ans(ans)
        codes[idx] = r.strip("\n\n")
        if ans is not None and not isinstance(ans, str):
            result_counter.update([abs(ans)])
            result_dict[abs(ans)].append(idx)
    if len(result_counter) > 0:
        prediction = result_counter.most_common(1)[0][0]
        program = codes[result_dict[prediction][0]].replace("    ", "")
    else:
        prediction, program = None, None
    print(prediction,program)
    # reply=chatgpt("hello what is your name")
    # print(reply)
import argparse
import time

import openai
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
def call_gpt3( engine,prompt):
    response = openai.Completion.create(engine=engine,
                                        prompt=prompt,
                                        temperature=0.5,
                                        max_tokens=400,
                                        n=10,
                                        # frequency_penalty=frequency_penalty,
                                        # presence_penalty=presence_penalty,
                                        # stop=["\n"])
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
                                                # stop=["\n"])
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
    reply = call_gpt3( "text-davinci-002",message)
    # reply=chatgpt("hello what is your name")
    print(reply)
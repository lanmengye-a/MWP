import argparse
import time

import openai
openai.api_key = "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"
train_sample =[
    {
        "Question":"23 children were riding on the bus. At the bus stop 24 children got on the bus while some got off the bus. Then there were 8 children altogether on the bus. How many more children got off the bus than those that got on?",
"Thought":"import math \nimport numpy as np\n# Are follow up questions needed here:Yes.# according to the questions, we can define the variables:”\nchildren_on_bus_before = 23\nchildren_on_bus_after = 8\nchildren_on_and_off_the_bus = 24\n# Follow up: how many children got off the bus?\nchildren_off_the_bus = children_on_bus_before + children_on_and_off_the_bus - children_on_bus_after\n# Follow up: how many more children got off the bus than those that got on?\nchildren_got_off_the_bus = children_off_the_bus - children_on_and_off_the_bus\nans= children_got_off_the_bus"    }
]
algebraicPrompt = "Write a mathematical equation and generate the answer format starting with `ans =' "
def call_gpt3( engine,que):
    message = algebraicPrompt + "\n\n".join(
        [f"Question: {sample['Question']}\nThought: {sample['Thought']}" for sample in
         train_sample]) + "\n\n" + f"Question: {que}\nThought:" + "# Are follow up questions needed here:Yes.# according to the questions, we can define the variables:"
    response = openai.Completion.create(engine=engine,
                                        prompt=message,
                                        temperature=0.5,
                                        max_tokens=400,
                                        # top_p=top_p,
                                        # frequency_penalty=frequency_penalty,
                                        # presence_penalty=presence_penalty,
                                        # stop=["\n"])
                                        )
    output = response["choices"][0]["text"].strip()
    return output

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
                max_tokens=300,
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
    # que = "Sandy sold lemonade in her neighborhood . She got number0 half - dollars on Saturday and number1 half - dollars on Sunday . What amount of money did Sandy receive ?"
    # que = "23 children were riding on the bus. At the bus stop 24 children got on the bus while some got off the bus. Then there were 8 children altogether on the bus. How many more children got off the bus than those that got on?"
    # que ="28 children were riding on the bus. At the bus stop, 82 children boarded the bus, while some others got off. Afterward, there were 30 children in total on the bus. How many more children boarded the bus than those who got off?"
    que = "Mary is baking a cake. The recipe calls for 12 cups of sugar and 14 cups of flour. She already put in 10 cups of sugar. How many more cups of flour than cups of sugar does she need to add now?"

    # que = "23 children were riding on the bus. At the bus stop 24 children got on the bus while some got off the bus. Then there were 8 children altogether on the bus. How many more children got off the bus than those that got on?"
    # que = "3 birds were sitting on the fence. 6 more storks and 2 more birds came to join them. How many more storks than birds are sitting on the fence?"
    message = algebraicPrompt+ "\n\n".join(
        [ f"Question: {sample['Question']}\nThought: {sample['Thought']}" for sample in
         train_sample]) + "\n\n" + f"Question: {que}\nThought:"+"# Are follow up questions needed here:Yes.# according to the questions, we can define the variables:"
    reply = call_gpt3( "text-davinci-003",message)
    # reply=chatgpt("hello what is your name")
    print(reply)
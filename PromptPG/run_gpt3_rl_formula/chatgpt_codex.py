import os
import openai

openai.api_key = "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"
def runSomeCode():
    response = openai.Completion.create(
      engine="code-davinci-002",
      prompt="\"\"\"\n1. Get a reputable free news api\n2. Make a request to the api for the latest news stories\n\"\"\"",
      temperature=0,
      max_tokens=1500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)
    if 'choices' in response:
        x = response['choices']
        if len(x) > 0:
            return x[0]['text']
        else:
            return ''
    else:
        return ''
answer = runSomeCode()
print(answer)
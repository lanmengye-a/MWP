import openai

# should be replaced by your API key
openai.api_key = "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"
messages = [
    {"role": "system", "content": "What can you do as an AI."},
]
demo = "'Question':'Mary is baking a cake. The recipe calls for 12 cups of sugar and 14 cups of flour. She already put in 10 cups of sugar. How many more cups of flour than cups of sugar does she need to add now?', \
'Thought':"
# Are follow up questions needed here:Yes.
# according to the questions, we can define the variables:"
messages.append({"role":"user","content":demo})
messages.append({"role":"system","content":"total_cups_of_sugar_needed = 12\
total_cups_of_flour_needed = 14\
cups_of_sugar_added = 10\
# Follow up: how many more cups of flour than cups of sugar does she need to add now?\
cups_of_flour_needed = total_cups_of_flour_needed - cups_of_sugar_added\
# Follow up: how many cups of flour does she need to add now?\
cups_of_flour_needed = total_cups_of_flour_needed - cups_of_sugar_added\
ans= cups_of_flour_needed"
                 })
messages.append({
    "role":"system","content":"Have I made any mistakes in any equation? If any , how should I fix them? please output complete answer"
})
messages.append({"role":"system","content":"\
Yes, there is a mistake in the equation. Here's the corrected version:\
'''python\
total_cups_of_sugar_needed = 12\
total_cups_of_flour_needed = 14\
cups_of_sugar_added = 10\
# Corrected equation: how many more cups of flour than cups of sugar does she need to add now?\
cups_of_flour_needed = total_cups_of_flour_needed - (cups_of_sugar_added - total_cups_of_sugar_needed)\
ans = cups_of_flour_needed\
'''"})

while True:
    # message = input("User : ")
    message = "Have you made any mistakes in any equation? If any , how should I fix them? please output complete answer"
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
    break
import json
with open("dataset/demos/svamp/svamp_selfask_programdemoaddprefix.jsonl") as f:
    lines = f.readlines()
    lines = [json.loads(line) for line in lines]
few_prompts = ""
for item in lines:
    #few_prompts += "#Question:" + item["Question"] + "\n" + "#Program:" + "\n" + item["Program"]+"\n\n"
    few_prompts +=  item["Program"] + "\n\n"
MATH_PROMPT = few_prompts
MATH_PROMPT ="""
# Question: Adam had 48.0 books . If he sold 19.0 of them and used the money he earned to buy 38.0 new books , how many books would Adam have ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
books_original = 48.0
books_sold = 19.0
books_bought = 38.0
# Follow up:How many books did Adam have before he sold any ?
books_before_sale = books_original
# Follow up: How many books does Adam have now ?
books_now = books_before_sale - books_sold + books_bought
ans = books_now


# Question: For Halloween Katie and her sister combined the candy they received . Katie had 8.0 pieces of candy while her sister had 23.0 . If they ate 8.0 pieces the first night , how many pieces do they have left ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
candy_katie = 8.0
candy_sister = 23.0
candy_ate = 8.0
# Follow up:How many pieces do they have left ?
candy_left = candy_katie + candy_sister - candy_ate
ans = candy_left


# Question: Mary picked 14.0 oranges and Jason picked 41.0 oranges . Keith picked 38.0 apples . How many oranges were picked in all ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
mary_oranges = 14.0
jason_oranges = 41.0
keith_apples = 38.0
# Follow up:How many oranges were picked in all ?
total_oranges = mary_oranges + jason_oranges
ans = total_oranges


# Question: Luke had 48.0 dollars in January . By March he had spent 11.0 dollars . If he got another 21.0 dollars from his mom , how much money would he have ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
money_january = 48.0
money_spend = 11.0
money_from_mom = 21.0
# Follow up:How much money does Luke have left in March ?
money_in_march = money_january - money_spend + money_from_mom
ans = money_in_march


# Question: There are 65.0 students trying out for the school 's trivia teams . If 17.0 of them did n't get picked for the team and the rest were put into 8.0 groups , how many students would be in each group ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
students_total = 65.0
students_not_picked = 17.0
groups = 8.0
# Follow up:How many students get picked for the team ?
student_picked = students_total - students_not_picked
# Follow up:How many students are in each group ?
students_per_group = student_picked / groups
ans = students_per_group


# Question: Christopher strolled 5.0 miles at 4.0 miles per hour . How long did Christopher stroll ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
distance = 5.0
speed = 4.0
# Follow up:How long did Christopher stroll ?
time = distance / speed
ans = time


# Question: Bianca had 45.0 coloring books . If she gave away 6.0 of them , but then bought 20.0 more , how many would she have total ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
coloring_books_original = 45.0
coloring_books_given_away = 6.0
coloring_books_bought = 20.0
# Follow up: How many coloring books does Bianca have left?
coloring_books_left = coloring_books_original - coloring_books_given_away
# Follow up: How many coloring books does Bianca have in total?
coloring_books_total = coloring_books_left + coloring_books_bought
ans = coloring_books_total


# Question: a pet shop has a total of 77 animals . 32 of them are kittens and 15 of them hamsters the rest are birds . how many birds are there ?
# Thought:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
total_animals = 77
kittens = 32
hamsters = 15
# Follow up:How many animals are not kittens or hamsters ?
not_kittens_hamsters = total_animals - (kittens + hamsters)
# Follow up:How many birds are there ?
birds = not_kittens_hamsters
ans = birds
"""



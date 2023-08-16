# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PREFIX ="""
# Read the following passages to answer questions with Python code,store the result as a 'ans' variable:
"""
MATH_PROMPT='''
# Passage:Mary is baking a cake. The recipe calls for 9 cups of sugar 7 cups of flour and 4 cups of salt. She already put in 2 cups of flour.
# Question:How many more cups of flour than cups of salt does she need to add now?
import numpy as np
# according to the questions, we can define the variables:
sugar_cups_needed = 12
flour_cups_needed = 14
sugar_cups_added = 10
# Are follow up questions needed here:Yes.
# Follow up:how many cups of sugar she need to add now?
sugar_cups_needed_now = sugar_cups_needed - sugar_cpus_added
# Follow up:how many cups of flour she need to add now?
flour_cups_needed_now = flour_cups_needed
# Follow up：How many more cups of flour than cups of sugar does she need to add now?
And = flour_cups_needed_now - sugar_cups_needed_now
'''
MATH_PROMPT = '''
# Passage:There are 65.0 students trying out for the school 's trivia teams . If 17.0 of them did n't get picked for the team and the rest were put into 8.0 groups 
# Question:how many students would be in each group ?
# Thought:
import numpy as np
# According to the question, we can define the variable:
students_total = 65.0
students_not_picked = 17.0
groups = 8.0
# Are followed up question needed here:Yes
# Follow up:How many students get picked for the team ?
student_picked = students_total - students_not_picked
# Follow up:How many students are in each group ?
students_per_group = studentt_picked / groups
ans = students_per_group

# Passage: a pet shop has a total of 77 animals . 32 of them are kittens and 15 of them hamsters the rest are birds 
# Question: how many birds are there ?
# Thought:
import numpy as np
# According to the question, we can define the variable:
total_animals = 77
kittens = 32
hamsters = 15
# Are followed up question needed here:No
# The number of birds is:
ans = total_animals - kittens - hamsters
'''




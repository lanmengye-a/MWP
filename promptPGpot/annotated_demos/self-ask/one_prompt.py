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

MATH_PROMPT = '''
# Question:There are 65.0 students trying out for the school 's trivia teams . If 17.0 of them did n't get picked for the team and the rest were put into 8.0 groups , how many students would be in each group ?
# Program:
# Are followed up question needed here:Yes
# According to the question, we can define the variable:
students_total = 65.0
students_not_picked = 17.0
groups = 8.0
# Follow up:How many students get picked for the team ?
student_picked = students_total - students_not_picked
# Follow up:How many students are in each group ?
students_per_group = studentt_picked / groups
ans = students_per_group
'''
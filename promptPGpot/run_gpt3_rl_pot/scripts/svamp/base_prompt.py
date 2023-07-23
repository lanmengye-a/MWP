import json


def get_table_text(problem):
    table = problem['table']
    title = problem['table_title']
    if title and len(title) > 0:
        table = f"[TITLE]: {title}\n{table}"
    return table


def get_question_text(problem, option_inds):
    question = problem['question']

    unit = problem['unit']
    if unit and len(unit) > 0:
        question = f"{question} (Unit: {unit})"

    choices = problem['choices']
    if choices and len(choices) > 0:
        choice_list = []
        for i, c in enumerate(choices):
            choice_list.append("({}) {}".format(option_inds[i], c))
        options = " ".join(choice_list)
        #print(options)
        question = f"{question}\nOptions: {options}"

    return question


def get_answer(problem):
    return problem['answer']


def get_solution_text(problem):
    # \\n: GPT-3 can generate the solution with more tokens
    solution = problem['solution'].replace("\n", "\\n")
    return solution


def create_one_example( question, answer, solution=None, test_example=True):

    # input_format, output_format = format.split("-")  # e.g., "TQ-A"

    elements = {
        "Q": f"Question: {question}",

        "S": f"Solution: {solution}",
        "T": f"Thought: \n{solution}",
        "A": f"Answer: The answer is {answer}.",
        "AS": f"Answer: The answer is {answer}. BECAUSE: {solution}",
        "SA": f"Answer: {solution} The answer is {answer}."
    }

    # Input
    # input = "\n".join(elements[label] for label in input_format)
    input = "Question:"+question
    # Output
    if test_example:
        output = "Thought:\n# Are follow up questions needed here:Yes.# according to the questions, we can define the variables:"
    else:
        output = elements["T"]

    # Prompt text
    text = input + "\n" + output
    text = text.replace("  ", " ").strip()

    return text


def build_prompt(problems, shot_pids, test_pid, args):
    examples = []
    pids = shot_pids + [test_pid]
    lines = json.load(open("dataset/demo8.json"))
    Index2idx = {item["Index"]:idx for idx,item in enumerate(lines)}
    # n-shot training examples
    for pid in pids:
        problem = problems[pid]
        # table = get_table_text(problem)
        question = problem["Question"]
        answer = problem["Answer"]
        if pid == test_pid:
            example = create_one_example(question, answer, solution, test_example=True)
        else:
            solution = lines[Index2idx[pid]]["Thought"]
            example = create_one_example(question, answer, solution, test_example=False)
        examples.append(example)

    # create the prompt input
    prompt_input = '\n\n'.join(examples)
    algebraicPrompt = "Write a mathematical equation and generate the answer format starting with `ans =' "
    prompt_input = algebraicPrompt +"\n\n" + prompt_input
    return prompt_input


def create_example_from_pid(pid, problems, args, test=False):
    lines = json.load(open("dataset/demo8.json"))
    Index2idx = {item["Index"]: idx for idx, item in enumerate(lines)}
    problem = problems[pid]
    question = problem["Question"]
    answer = problem["Answer"]

    if test:
        solution = None
        example = create_one_example( question, answer, solution, test_example=True)
    else:
        solution = lines[Index2idx[pid]]["Thought"]
        example = create_one_example(question, answer, solution, test_example=False)
    return example

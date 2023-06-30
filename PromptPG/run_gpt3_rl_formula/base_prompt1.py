

def get_question_text(problem):
    question =  problem["Question"]
    return question


def get_infixEquation(problem):
    return problem['infixEquation']



def create_one_example( question, infixEquation,test_example=True):

    input_format, output_format = "Q-A".split("-")  # e.g., "TQ-A"

    elements = {
        "Q": f"Question: {question}",
        "A": f"infixEquation: Answer = {infixEquation}.",

    }

    # Input
    input = "\n".join(elements[label] for label in input_format)

    # Output
    if test_example:
        output = "infixEquation:"
    else:
        output = elements[output_format]

    # Prompt text
    text = input + "\n" + output
    text = text.replace("  ", " ").strip()

    return text


def build_prompt(problems, shot_pids, test_pid):

    examples = []
    pids = shot_pids + [test_pid]

    # n-shot training examples
    for pid in pids:
        problem = problems[pid]

        question = get_question_text(problem)
        answer = get_infixEquation(problem)


        if pid == test_pid:
            assert pid not in shot_pids
            example = create_one_example( question, answer,  test_example=True)
        else:
            example = create_one_example(question, answer,  test_example=False)

        examples.append(example)

    # create the prompt input
    prompt_input = '\n\n'.join(examples)

    return prompt_input


def create_example_from_pid(pid, problems,testStage=False):
    problem = problems[pid]
    question = get_question_text(problem)
    infixEquation = get_infixEquation(problem)
    if testStage:
        example = create_one_example( question, infixEquation,  test_example=True)
    else:
        example = create_one_example(question, infixEquation,  test_example=False)
    return example

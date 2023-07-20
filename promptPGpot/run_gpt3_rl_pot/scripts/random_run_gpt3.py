import os
import json
import argparse
import random
import time

from base_prompt1 import *
from model import *
from utilities1 import extract_prediction, normalize_answer

import numpy as np
import torch
import torch.nn.functional as F
import openai

# openai.api_key = "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"
# openai.api_key = "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"
openai.api_key = "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"


def load_data(args):
    problems_test = json.load(open(os.path.join(args.data_root, f'svamp_{args.test_split}.json')))
    problems_train = json.load(open(os.path.join(args.data_root, f'svamp_train.json')))
    # 输出problems_test 和 problems_train的长度
    print(f"number of test problems: {len(problems_test)}")
    print(f"number of train problems: {len(problems_train)}")

    # 合并prolems_test和problems_train
    problems = [*problems_test,*problems_train]
    testLen=len(problems_test)
    # test problem ids
    test_pids = [item for item in range((testLen))]

    test_pids = test_pids[:args.test_number] if args.test_number > 0 else test_pids
    print(f"number of test problems: {len(test_pids)}\n")
    # pick up shot/in-context example candidates from the training set
    train_pids = [item for item in range((testLen),len(problems))]

    cand_pids = random.sample(train_pids, args.cand_number)  # random sample

    return problems, test_pids, cand_pids


def get_gpt3_output(prompt, args):
    patience = 2
    while True:
        try:
            print("prompt:", prompt)
            response = openai.Completion.create(engine=args.engine,
                                                prompt=prompt,
                                                temperature=args.temperature,
                                                max_tokens=args.max_tokens,
                                                top_p=args.top_p,
                                                frequency_penalty=args.frequency_penalty,
                                                presence_penalty=args.presence_penalty,
                                                stop=["\n"])
            output = response["choices"][0]["text"].strip()
            break
        except Exception as e:
            patience -= 1
            if not patience:
                print("!!! Running out of patience waiting for OpenAI")
            else:
                print(e)
                time.sleep(0.1)
    return output


def get_result_file(args):
    result_path = f"{args.output_root}/{args.model}"
    os.makedirs(result_path, exist_ok=True)

    result_file = "{}/{}_{}_{}_{}_seed_{}.json".format(result_path, args.label, args.test_split, args.prompt_format,
                                                       args.shot_number, args.seed)

    return result_file


def save_results(result_file, acc, correct, count, cand_pids, args, results):
    data = {}
    data['acc'] = acc
    data['correct'] = correct
    data['count'] = count
    data['cand_pids'] = cand_pids
    data['args'] = vars(args)
    data['results'] = results

    with open(result_file, 'w') as f:
        json.dump(data, f, indent=2, separators=(',', ': '))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', type=str, default='../data/svamp')
    parser.add_argument('--output_root', type=str, default='../results')
    parser.add_argument('--model', type=str, default='gpt3_rl')
    parser.add_argument('--option_inds', type=list, default=["A", "B", "C", "D", "E", "F"])

    # user options
    parser.add_argument('--label', type=str, default='svampexp')
    parser.add_argument('--test_split', type=str, default='test', choices=['dev', 'dev1k', 'test', 'test1k'])
    parser.add_argument('--test_number', type=int, default=100, help='GPT-3 is expensive. -1 for the whole test set')
    parser.add_argument('--save_every', type=int, default=10, help='Save the result with every n examples.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument(
        '--prompt_format',
        type=str,
        default='SVAMP',
        choices=['T-A', 'Q-A', 'Q-AS', 'Q-SA', 'TQ-A', 'TQ-AS', 'TQ-SA', 'QT-A', 'QT-AS', 'QT-SA', 'QTS-A', 'TQS-A'],
        help='prompt format template')
    parser.add_argument('--shot_number', type=int, default=2, help='Number of n-shot training examples.')
    parser.add_argument('--seed', type=int, default=1, help='random seed')

    # GPT-3 settings
    parser.add_argument('--engine', type=str, default='text-davinci-002', choices=['text-davinci-002', 'ada'])
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--max_tokens',
                        type=int,
                        default=512,
                        help='The maximum number of tokens allowed for the generated answer.')
    parser.add_argument('--top_p', type=float, default=1.0)
    parser.add_argument('--frequency_penalty', type=float, default=0.0)
    parser.add_argument('--presence_penalty', type=float, default=0.0)

    # Policy Model settings
    parser.add_argument('--gpu', type=str, default='0')
    parser.add_argument('--model_config',
                        type=str,
                        default='bert-base-uncased',
                        choices=['distilbert-base-uncased', 'bert-base-uncased'])
    parser.add_argument('--cand_number', type=int, default=20, help='Number of candidate prompts.')
    parser.add_argument('--embedding_size', type=int, default=128, help='Policy network final layer hidden state size.')
    parser.add_argument('--ckpt_root', type=str, default='../checkpoints')
    parser.add_argument('--ckpt', type=str, default=None)

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()
    print('====Input Arguments====')
    print(json.dumps(vars(args), indent=2, sort_keys=False))

    # https://pytorch.org/docs/stable/notes/randomness.html
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)  # CPU random seed
    torch.cuda.manual_seed(args.seed)  # GPU random seed
    torch.backends.cudnn.benchmark = True

    # problems, test question ids, candidate prompt pids, RL training pids
    problems, pids, cand_pids = load_data(args)
    result_file = get_result_file(args)
    # load the check point
    if os.path.exists(result_file):
        print("# The result file exists! We will load the learned check point!!!")
        check_point = json.load(open(result_file))
        results = check_point['results']
    else:
        results = {}

    total = len(pids)
    check_count = len(results)  # number of existing results
    correct = 0  # number of correct results




    cand_examples = []
    for pid in cand_pids:
        example = create_example_from_pid(pid, problems, args, test=True)  # CHECK !!!
        # print(example)
        # print("===========")
        cand_examples.append(example)

    # ======================================================= INFERENCE ===============================================


    for i, pid in enumerate(pids):
        print("inspect...",i)
        count = i + 1  # number of current results
        problem = problems[pid]
        # print("problem的属性值",problem.keys())
        answer = problems[pid]['Answer']
        options = problems[pid]['option']
        unit = problems[pid]['unit']
        example = create_example_from_pid(pid, problems, args, test=True)
        ids = [id for id in range(len(cand_pids))]
        cand_ids = random.sample(ids, args.shot_number)
        shot_pids = [cand_pids[cid] for cid in cand_ids[::-1]]
        prompt = build_prompt(problems, shot_pids, pid, args)  # generate the prompt input

        if pid in results:
            output = results[pid]["output"]
        else:
            output = get_gpt3_output(prompt, args)  # generate the output by GPT-3

        # the core prediction in the output
        prediction = extract_prediction(output, options, args.option_inds)

        # normalize the number in the text
        answer_norm = normalize_answer(answer, unit)
        prediction_norm = normalize_answer(prediction, unit)

        # save the results
        results[pid] = {}

        results[pid]["shot_pids"] = shot_pids
        results[pid]["prompt"] = prompt
        results[pid]["answer"] = answer
        results[pid]["answer_norm"] = answer_norm
        results[pid]["output"] = output
        results[pid]["prediction"] = prediction
        results[pid]["prediction_norm"] = prediction_norm

        # correct or not
        if answer_norm.lower() == prediction_norm.lower():
            correct += 1
            results[pid]["true_false"] = True
        else:
            results[pid]["true_false"] = False

        acc = correct / (i + 1) * 100

        # if args.debug or i < 10:
        #     print("\n##################################")
        #     print(prompt, "\n")
        #     print("[A] labeled answer (normalized):\t", answer_norm)
        #     print("[P] predicted answer (normalized):\t", prediction_norm)
        #     print("[Acc]:\t", results[pid]["true_false"])
        #     print("")
        #     print("[A] labeled answer:\t", answer)
        #     print("[P] predicted answer:\t", prediction)
        #     print("[P] generated output:\t", output)

        if count % args.save_every == 0 or count == total:
            if count >= check_count:
                # have new outputs
                print(f"{count}/{total}, correct: {correct}, acc: {round(acc, 2)}%, saved to {result_file}")
                save_results(result_file, acc, correct, count, cand_pids, args, results)
            else:
                # no new outputs, just print the accuracy
                print(f"{count}/{total}, correct: {correct}, acc: {round(acc, 2)}%")

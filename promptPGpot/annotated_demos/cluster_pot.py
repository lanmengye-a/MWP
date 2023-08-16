import argparse
from annotated import get_rationales
import json
"""
为选出的问题生成pot
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="Zero-shot-CoT")
    parser.add_argument(
        "--dry_run", type=bool, default=False, help="debug mode"
    )
    parser.add_argument(
        "--save_demo_dir", type=str, default="dataset/svamp/demo8_train.json", help="where to save the contructed demonstrations"
    )
    parser.add_argument(
        "--cluster_save_demo_dir", type=str, default="dataset/svamp/demos/demo8_train.json", help="where to save the contructed demonstrations"
    )

    parser.add_argument(
        "--debug", type=bool, default=True, help="debug mode"
    )
    parser.add_argument("--engine", default="text-davinci-003", type=str)
    parser.add_argument("--key", default="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", type=str)
    args = parser.parse_args()
    return args
def get_cluster_pot(args):
    with open(args.save_demo_dir,"r") as reader:
        items=json.load(reader)["demo"]
        demos = []
        for idx,item in enumerate(items):
            question = item["question"]
            prediction,program=get_rationales(args, question)
            c_pred_ans = prediction
            c_question = question
            c_rationale = program
            if args.debug:
                c_gold_ans = item["gold_ans"]
            else:
                c_gold_ans = None
            demo_element = {
                "question": c_question,
                 "rationale": c_rationale,
                "pred_ans": c_pred_ans,
                "gold_ans": c_gold_ans,
            }
            demos.append(demo_element)

    with open(args.cluster_save_demo_dir, 'w', encoding="utf-8") as write_f:
        json.dump(demos, write_f, indent=4, ensure_ascii=False)
if __name__ =="__main__":
    get_cluster_pot(parse_arguments())
import json
with open("results/gpt3_rl/exp0_best_loss_test_TQ-A_2_seed_1.json", "r") as f:
    data = json.load(f)
results=data["results"]
for idx,result in results.items():
    if(result["true_false"] == False):
        print("prompt:",result["prompt"])
        print("answer:",result["answer"])
        print("program:",result["program"])
        print("prediction:",result["prediction"])
        input("1 or 0")
import torch
from transformers import DebertaTokenizer, DebertaForMaskedLM, DebertaModel


def sim_deberta(text1,text2):
    # 加载预训练的DeBERTa模型和分词器
    model_name = 'microsoft/deberta-base'
    tokenizer = DebertaTokenizer.from_pretrained(model_name)
    model = DebertaModel.from_pretrained(model_name)
    # 分词并转换为模型输入格式
    inputs1 = tokenizer(text1,return_tensors='pt', padding=True, truncation=True)
    inputs2 = tokenizer(text2, return_tensors='pt', padding=True, truncation=True)

    # 计算相似度得分
    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)
    # 获取CLS token的输出向量
    cls_embedding1 = outputs1.last_hidden_state[:, 0, :]
    cls_embedding2 = outputs2.last_hidden_state[:, 0, :]
    # 计算相似度得分（可以根据任务具体需求使用不同的计算方法）
    similarity_score = torch.cosine_similarity(cls_embedding1[0], cls_embedding2[0], dim=0)
    # print("Similarity Score:", similarity_score.item())
    return similarity_score.item()

def analysis_file_sim(file_name):
    with open(file_name) as reader:
        text = json.load(reader)
    with open("dataset/svamp_test_pot.jsonl", "r") as reader:
        lines = reader.readlines()
        problems = [json.loads(line) for line in lines]
    sim = []
    for idx,item in text["results"].items():

        shot_pids = item["shot_pids"]
        avg_sim,total = 0,0
        for idx,pid in enumerate(shot_pids):
            ques = item["prompt"].split("\n\n")[-1].split("\n")[0].strip("Question:")
            total += sim_deberta(problems[pid-1]["Question"],ques)
            avg_sim = total/(idx+1)
            print(f"idx{idx}:sim:{avg_sim}")
            sim.append(avg_sim)
    return sim


if __name__ == "__main__":
    import json
    # file1 = "results/gpt3_rl/exp0_test_TQ-A_2_seed_1.json"
    # sim1=analysis_file_sim(file1)
    file2 = "results/gpt3_rl/exp0_random_test_TQ-A_2_seed_1.json"
    sim2 = analysis_file_sim(file2)
    from matplotlib import pyplot as plt
    ranges = [i for i in range(len(sim2))]
    # plt.plot(ranges,sim1,label="promptPG")
    plt.plot(ranges, sim2, label="random")
    plt.show()
    plt.savefig("results/fig/sim.png")


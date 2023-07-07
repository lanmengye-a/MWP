import random

import numpy
import torch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import json
import matplotlib.pyplot as plt
import argparse

from torch.version import cuda
from transformers import BertTokenizer, DebertaV2Tokenizer

from utils import fix_seed
from run_svamp_simple import get_rationales, create_reader_request
"""
选问题
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="Zero-shot-CoT")
    parser.add_argument(
        "--task", type=str, default="svamp",
        choices=["aqua", "gsm8k", "commonsensqa", "addsub", "multiarith", "strategyqa", "svamp", "singleeq", "coin_flip", "last_letters"], help="dataset used for experiment"
    )
    parser.add_argument(
        "--max_ra_len", type=int, default=5, help="maximum number of reasoning chains"
    )
    parser.add_argument(
        "--pred_file", type=str, default="dataset/SVAMP/SVAMP.json",
        help="use the reasoning chains generated by zero-shot-cot."
    )
    parser.add_argument(
        "--demo_save_dir", type=str, default="demos/svamp_pot_optim_deberta.json", help="where to save the contructed demonstrations"
    )
    parser.add_argument("--random_seed", type=int, default=192, help="random seed")
    parser.add_argument(
        "--encoder", type=str, default="all-MiniLM-L6-v2", help="which sentence-transformer encoder for clustering"
    )
    parser.add_argument(
        "--sampling", type=str, default="center", help="whether to sample the cluster center first"
    )
    parser.add_argument(
        "--debug", type=bool, default=True, help="debug mode"
    )
    parser.add_argument(
        "--dry_run", type=bool, default=False, help="debug mode"
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    fix_seed(args.random_seed)
    from transformers import AutoTokenizer, AutoModel
    from transformers import DebertaModel
    tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-base")
    model = DebertaModel.from_pretrained("microsoft/deberta-base")
    # encoder  = tokenizer
    # encoder = SentenceTransformer(args.encoder)


    task = args.task
    pred_file = args.pred_file
    save_file = args.demo_save_dir
    max_ra_len = args.max_ra_len
    if task == "last_letters":
        max_ra_len = 7
    if task == "aqua" or task == "last_letters":
        num_clusters = 4
    elif task == "commonsensqa":
        num_clusters = 7
    elif task == "strategyqa":
        num_clusters = 6
    else:
        num_clusters = 8

    corpus = []
    question = []
    rationale = []
    gold_ans = []
    pred_ans = []

    with open(pred_file, "r", encoding="utf-8") as fp:
        lines=json.load(fp)
        for line in lines:
            c_question = create_reader_request(line)
            corpus.append(c_question)
            gold_ans.append(line["Answer"])
    # corpus = numpy.array(corpus).reshape(1000,-1)
    corpus = corpus
    try:
        corpus_ids = tokenizer(corpus,return_tensors="pt",padding=True,truncation=True,max_length=128)
        corpus_embeddings = model(input_ids=corpus_ids["input_ids"],attention_mask = corpus_ids["attention_mask"],token_type_ids=corpus_ids["token_type_ids"] ).last_hidden_state
        corpus_embeddings = corpus_embeddings.last_hidden_state.detach().numpy()
    except Exception as e:
        print(e)

    # Perform kmean clustering
    clustering_model = KMeans(n_clusters=num_clusters, random_state=args.random_seed)
    device = torch.device("cuda:0") if cuda.is_available() else torch.device("cpu")
    clustering_model.fit(corpus_embeddings,device=device)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(num_clusters)]

    dist = clustering_model.transform(corpus_embeddings)
    clustered_dists = [[] for i in range(num_clusters)]
    clustered_idx = [[] for i in range(num_clusters)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(corpus[sentence_id])
        clustered_dists[cluster_id].append(dist[sentence_id][cluster_id])
        clustered_idx[cluster_id].append(sentence_id)

    demos = []

    for i in range(len(clustered_dists)):
        print("Cluster ", i+1)
        tmp = list(map(list, zip(range(len(clustered_dists[i])), clustered_dists[i])))
        top_min_dist = sorted(tmp, key=lambda x: x[1], reverse=False)
        if not args.sampling == "center":
            random.shuffle(top_min_dist)

        # 此处要修改成用问题生成 retionale
        for element in top_min_dist:
            min_idx = element[0]
            question = corpus[clustered_idx[i][min_idx]].strip()
            ans = gold_ans[clustered_idx[i][min_idx]]
            demos.append({"question":question,"gold_ans":ans})
            break

    demos = {"demo": demos}
    print("demos_length:",len(demos["demo"]))
    with open(args.demo_save_dir, 'w', encoding="utf-8") as write_f:
        json.dump(demos, write_f, indent=4, ensure_ascii=False)

    y_km = clustering_model.fit_predict(corpus_embeddings)
    pca_model = PCA(n_components=2, random_state=args.random_seed)
    transformed = pca_model.fit_transform(corpus_embeddings)
    centers = pca_model.transform(clustering_model.cluster_centers_)

    plt.scatter(x=transformed[:, 0], y=transformed[:, 1], c=y_km, s=50, cmap=plt.cm.Paired, alpha=0.4)
    plt.scatter(centers[:, 0],centers[:, 1],
            s=250, marker='*', label='centroids',
            edgecolor='black',
           c=np.arange(0,num_clusters),cmap=plt.cm.Paired,)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(save_file+".png", dpi=600)

if __name__ == "__main__":
    main()
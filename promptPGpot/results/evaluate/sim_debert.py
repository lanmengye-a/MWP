from transformers import DebertaTokenizer, DebertaModel,AutoTokenizer,BertModel
from scipy.spatial.distance import cosine
import torch
# 加载预训练模型和分词器
# tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')
# model = DebertaModel.from_pretrained('microsoft/deberta-base')
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
# 定义两个句子
sentence1 = "我喜欢吃苹果"
sentence2 = "我讨厌吃苹果，讨厌得很"

# 对句子进行编码
inputs1 = tokenizer(sentence1, return_tensors='pt')
inputs2 = tokenizer(sentence2, return_tensors='pt')

# 计算句子的嵌入向量
with torch.no_grad():
    embeddings1 = model(**inputs1).last_hidden_state[:, 0, :]
    embeddings2 = model(**inputs2).last_hidden_state[:, 0, :]

# 计算余弦相似度
similarity = 1 - cosine(embeddings1[0], embeddings2[0])
print(f"相似度: {similarity:.4f}")

# from transformers import AutoTokenizer, BertModel
# import torch
#
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# model = BertModel.from_pretrained("bert-base-uncased")
#
# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# outputs = model(**inputs)
#
# last_hidden_states = outputs.last_hidden_state
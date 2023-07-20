# train_data
import json
with open("dataset/svamp_train_pot.jsonl") as reader:
    lines = reader.readlines()
lines = [json.loads(line) for line in lines]

with open("dataset/svamp_pot_optim.json") as reader:
    demos = json.load(reader)['demo']
with open("dataset/svamp_pot_optim_trans.json","w") as writer:
    items=[]
    for item in demos:
        idx = item["Index"]-1
        item["trans"]= lines[idx]["Question"]
        items.append(item)
    writer.write(json.dumps(items),indent=4,ensure_ascii=False)


command: >-
python run_demo.py # 从训练集找到最有代表性的cand,做人工标注
output:
    dataset/svamp_pot_optim.json.png
    dataset/svamp_pot_optim.json

python run_gpt3_rl_pot/scripts/learn_policy.py
# export PYTHONPATH=$PYTHONPATH:/public/home/lianghe/lmy/Auto-pot_optim/promptPGpot
# python run_gpt3_rl_pot/scripts/learn_policy.py




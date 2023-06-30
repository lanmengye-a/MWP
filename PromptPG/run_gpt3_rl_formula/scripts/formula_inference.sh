 export PYTHONPATH=/public/home/lianghe/lmy/PromptPG:PYTHONPATH
 python run_gpt3_1.py \
 --label svampexpFormula_80 \
 --ckpt_root ../checkpoints \
 --model gpt3_rl_formula \
 --model_config bert-base-uncased \
 --test_split test \
 --shot_number 2 \
 --prompt_format TQ-SA \
 --seed 2 \
 --temperature 0.5 \
 --test_number -1\
 --cand_number 20 \
 --embedding_size 128 \
 --ckpt svampexpFormula_80/ckpt_best_reward.pt \
 --gpu 0
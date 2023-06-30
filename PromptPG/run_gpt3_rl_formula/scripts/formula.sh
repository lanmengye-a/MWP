export PYTHONPATH=/public/home/lianghe/lmy/PromptPG:PYTHONPATH
python learn_policy1.py \
--label svampexpFormula_80 \
--ckpt_root ../checkpoints \
--shot_number 2 \
--prompt_format TQ-SA \
--seed 2 \
--model_config bert-base-uncased \
--train_number 80 \
--cand_number 10 \
--lr 0.001 \
--epochs 20 \
--embedding_size 128 \
--batch_size 20 \
--gpu 0
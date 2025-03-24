from pathlib import Path
from subword_nmt.learn_bpe import learn_bpe
from subword_nmt.apply_bpe import BPE
from collections import Counter

# 文件路径
train_src_file = "pre/train.en"  # 训练BPE时使用的英文数据
train_trg_file = "pre/train.zh"  # 训练BPE时使用的中文数据
train_l_file = "train_l"         # 仍然用 train_cut.en 和 train_cut.zh 生成
bpe_code_file = "bpe.25000"
vocab_file = "vocab"
num_operations = 30000

# 1. 生成 train_l（使用 train_cut.en 和 train_cut.zh）
train_cut_src = "train_cut.en"
train_cut_trg = "train_cut.zh"

with open(train_l_file, "w", encoding="utf-8") as out_f:
    with open(train_cut_src, "r", encoding="utf-8") as src_f:
        out_f.writelines(src_f.readlines())
    with open(train_cut_trg, "r", encoding="utf-8") as trg_f:
        out_f.writelines(trg_f.readlines())

print("[Step 1] train_l 文件生成完成！")

# 2. 训练 BPE（使用 pre/train.en 和 pre/train.zh）
with open(train_src_file, "r", encoding="utf-8") as src_f, open(train_trg_file, "r", encoding="utf-8") as trg_f, \
     open(bpe_code_file, "w", encoding="utf-8") as f_out:
    learn_bpe(src_f, f_out, num_operations)  # 只用英文训练
    learn_bpe(trg_f, f_out, num_operations)  # 只用中文训练

print("[Step 2] BPE 训练完成！")

# 3. 读取训练好的 BPE 规则
with open(bpe_code_file, "r", encoding="utf-8") as f:
    bpe = BPE(f)

# 4. 手动生成词汇表
word_counts = Counter()

# 读取 train_l 数据并统计 BPE 词汇
with open(train_l_file, "r", encoding="utf-8") as f_in:
    for line in f_in:
        tokenized_line = bpe.process_line(line.strip()).split()
        word_counts.update(tokenized_line)

# 写入词汇表
with open(vocab_file, "w", encoding="utf-8") as vocab_out:
    for word, count in word_counts.most_common():
        vocab_out.write(f"{word} {count}\n")

print("[Step 3] 词汇表生成完成！")

# 5. 应用 BPE 分词
def apply_bpe_to_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            f_out.write(bpe.process_line(line.strip()) + "\n")

# 处理 train_cut、val_cut、test_cut
for mode in ["train", "val", "test"]:
    print(f"[Step 4] 处理 {mode} 数据...")
    apply_bpe_to_file(f"{mode}_cut.en", f"{mode}_src.bpe")
    apply_bpe_to_file(f"{mode}_cut.zh", f"{mode}_trg.bpe")

print("[Step 5] BPE 分词完成！")

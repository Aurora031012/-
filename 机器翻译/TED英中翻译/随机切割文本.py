
import random

# 读取文件内容
def read_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()

# 保存文件内容
def save_lines(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# 打乱行顺序，同时保持中英文对应关系
def shuffle_together(a, b):
    combined = list(zip(a, b))
    random.shuffle(combined)
    a_shuffled, b_shuffled = zip(*combined)
    return list(a_shuffled), list(b_shuffled)

# 主函数
def split_and_shuffle_files(chinese_file, english_file):
    chinese_lines = read_lines(chinese_file)
    english_lines = read_lines(english_file)

    # 确保两个文件行数相同
    assert len(chinese_lines) == len(english_lines), "Files must have the same number of lines."

    # 计算每份文件应该包含的行数
    total_lines = len(chinese_lines)
    train_size = 80000
    val_test_size = (total_lines - train_size) // 2

    # 打乱所有行
    chinese_lines, english_lines = shuffle_together(chinese_lines, english_lines)

    # 分割文件
    train_chinese = chinese_lines[:train_size]
    train_english = english_lines[:train_size]
    val_chinese = chinese_lines[train_size:train_size + val_test_size]
    val_english = english_lines[train_size:train_size + val_test_size]
    test_chinese = chinese_lines[train_size + val_test_size:]
    test_english = english_lines[train_size + val_test_size:]

    # 保存文件
    save_lines('train.zh', train_chinese)
    save_lines('train.en', train_english)
    save_lines('val.zh', val_chinese)
    save_lines('val.en', val_english)
    save_lines('test.zh', test_chinese)
    save_lines('test.en', test_english)


# 调用主函数
split_and_shuffle_files('train.zh', 'train.en')
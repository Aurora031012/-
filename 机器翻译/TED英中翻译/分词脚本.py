
from sacremoses import MosesTokenizer
from pathlib import Path
import argparse


def moses_cut(in_file, out_file, lang):
    mt = MosesTokenizer(lang=lang) # 初始化分词器
    out_f = open(out_file, "w", encoding="utf8")
    with open(in_file, "r", encoding="utf8") as f:
        for line in f.readlines():#每读取一行，进行分词，并写入一行到新的文件中
            line = line.strip()
            if not line:
                continue
            cut_line = mt.tokenize(line, return_str=True) # 分词
            out_f.write(cut_line.lower() + "\n") #变为小写，并写入文件
    out_f.close()

if __name__ == '__main__':
    in_files = ['./train.en', './test.en', './val.en', './train.zh', './test.zh', './val.zh']
    out_files = ['./train_cut.en', './test_cut.en', './val_cut.en', './train_cut.zh', './test_cut.zh', './val_cut.zh']

    for in_file, out_file in zip(in_files, out_files):
        print(in_file)
        print(out_file)
        lang = in_file.split('.')[-1]
        moses_cut(in_file, out_file, lang)
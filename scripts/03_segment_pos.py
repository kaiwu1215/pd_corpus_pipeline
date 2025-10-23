import argparse, sys
import jieba
import jieba.posseg as pseg
from tqdm import tqdm
from utils.io_utils import read_lines, write_lines

def seg_line(s: str):
    # 返回 "词/词性" 用空格连接
    words = pseg.cut(s)
    return " ".join(f"{w.word}/{w.flag}" for w in words if w.word.strip())

def main():
    ap = argparse.ArgumentParser(description="分词 + 词性标注（jieba.posseg）")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--user_dict", default=None, help="可选：用户词典")
    args = ap.parse_args()

    if args.user_dict:
        jieba.load_userdict(args.user_dict)

    out = []
    for line in tqdm(read_lines(args.input)):
        out.append(seg_line(line))

    write_lines(args.output, out)

if __name__ == "__main__":
    main()

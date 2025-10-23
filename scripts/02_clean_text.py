import argparse
from utils.io_utils import read_lines, write_lines
from utils.text_utils import normalize_text

def main():
    ap = argparse.ArgumentParser(description="清洗 txt：去噪/规范化")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--only_chinese", type=int, default=1, help="仅保留中文/数字/常见标点(1/0)")
    ap.add_argument("--min_len", type=int, default=10, help="丢弃过短行")
    args = ap.parse_args()

    out = []
    for line in read_lines(args.input):
        # line: "日期\t标题\t正文" 或 纯文本
        if "\t" in line:
            parts = line.split("\t", 2)
            text = parts[-1] if len(parts) == 3 else line
        else:
            text = line
        norm = normalize_text(text, only_chinese=bool(args.only_chinese))
        if len(norm) >= args.min_len:
            out.append(norm)

    write_lines(args.output, out)

if __name__ == "__main__":
    main()

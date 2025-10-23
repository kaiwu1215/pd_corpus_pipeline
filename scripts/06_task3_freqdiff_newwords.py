import argparse, os, math
from collections import Counter
from utils.io_utils import read_lines, ensure_dir
from utils.text_utils import parse_seg_line

def load_words(path):
    cnt = Counter()
    for line in read_lines(path):
        for w, p in parse_seg_line(line):
            # 过滤过短/纯标点的 token
            if len(w.strip()) >= 2:
                cnt[w] += 1
    return cnt

def main():
    ap = argparse.ArgumentParser(description="任务3：1998.01 vs 2025.01 词频差异与新词抽取")
    ap.add_argument("--seg_2025", required=True)
    ap.add_argument("--seg_1998", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--min_count", type=int, default=3, help="新词最小频次（在 2025.01 中）")
    args = ap.parse_args()

    ensure_dir(args.out_dir)

    cnt25 = load_words(args.seg_2025)
    cnt98 = load_words(args.seg_1998)

    total25 = sum(cnt25.values()) or 1
    total98 = sum(cnt98.values()) or 1

    # 频率差异（相对频率）
    vocab = set(cnt25) | set(cnt98)
    rows = []
    new_words = []
    for w in vocab:
        f25 = cnt25.get(w, 0)
        f98 = cnt98.get(w, 0)
        p25 = f25 / total25
        p98 = f98 / total98
        diff = p25 - p98
        rows.append((w, f25, f98, p25, p98, diff))
        if f25 >= args.min_count and f98 == 0:
            new_words.append((w, f25))

    # 输出整体差异
    with open(os.path.join(args.out_dir, "freq_diff.csv"), "w", encoding="utf-8") as f:
        f.write("word,freq_2025,freq_1998,rel_2025,rel_1998,rel_diff\n")
        for w, f25, f98, p25, p98, diff in sorted(rows, key=lambda x: -x[5]):
            f.write(f"{w},{f25},{f98},{p25:.8f},{p98:.8f},{diff:.8f}\n")

    # 输出新词
    with open(os.path.join(args.out_dir, "new_words_2025_only.txt"), "w", encoding="utf-8") as f:
        for w, c in sorted(new_words, key=lambda x: -x[1]):
            f.write(f"{w}\t{c}\n")

    with open(os.path.join(args.out_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"tokens_2025={total25}, vocab_2025={len(cnt25)}\n")
        f.write(f"tokens_1998={total98}, vocab_1998={len(cnt98)}\n")
        f.write(f"new_words_2025_only={len(new_words)} (min_count={args.min_count})\n")
        f.write("Files: freq_diff.csv, new_words_2025_only.txt\n")

if __name__ == "__main__":
    main()

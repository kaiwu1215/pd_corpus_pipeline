import argparse, math, os
from collections import Counter, defaultdict
from tqdm import tqdm
from utils.io_utils import read_lines, ensure_dir
from utils.text_utils import parse_seg_line, strip_pos_from_seg, only_chinese_chars
from utils.stats_utils import calc_pmi

def char_pairs_stats(seg_lines, min_char_count=5):
    # 统计相邻字符对；区分是否在同一词内
    pair_counts = Counter()
    pair_counts_cross = Counter()   # 跨词边界
    left_counts = Counter()
    right_counts = Counter()
    total_pairs = 0

    for line in seg_lines:
        pairs = parse_seg_line(line)

        # 在词内部的相邻二字
        for w, _ in pairs:
            chs = only_chinese_chars(w)
            for i in range(len(chs) - 1):
                a, b = chs[i], chs[i+1]
                pair_counts[(a, b)] += 1
                left_counts[a] += 1
                right_counts[b] += 1
                total_pairs += 1

        # 词与词之间（跨边界）相邻二字
        words = [only_chinese_chars(w) for w, _ in pairs if w]
        for i in range(len(words) - 1):
            left_word = words[i]
            right_word = words[i+1]
            if not left_word or not right_word: 
                continue
            a = left_word[-1]
            b = right_word[0]
            pair_counts_cross[(a, b)] += 1
            left_counts[a] += 1
            right_counts[b] += 1
            total_pairs += 1

    return pair_counts, pair_counts_cross, left_counts, right_counts, total_pairs

def main():
    ap = argparse.ArgumentParser(description="任务1：相邻二字 PMI 与邻近同现概率（区分是否在同一词内）")
    ap.add_argument("--input", required=True, help="已分词+词性 的语料（每行：词/pos 空格分隔）")
    ap.add_argument("--output", required=True, help="输出目录")
    ap.add_argument("--min_count", type=int, default=5, help="最小二字对计数")
    args = ap.parse_args()

    ensure_dir(args.output)

    seg_lines = list(read_lines(args.input))
    pair_in, pair_cross, lc, rc, total = char_pairs_stats(seg_lines, min_char_count=args.min_count)

    # 计算 PMI
    pmi_in   = calc_pmi(pair_in,   lc, rc, total)
    pmi_cross= calc_pmi(pair_cross,lc, rc, total)

    # 邻近同现“概率”：pair_count / total_pairs
    with open(os.path.join(args.output, "adjacent_pairs_in_word.csv"), "w", encoding="utf-8") as f:
        f.write("char1,char2,count,pmi,adj_prob\n")
        for (a,b), c in pair_in.items():
            if c < args.min_count: 
                continue
            pmi = pmi_in.get((a,b), "")
            adjp = c / total if total else 0.0
            f.write(f"{a},{b},{c},{pmi},{adjp}\n")

    with open(os.path.join(args.output, "adjacent_pairs_cross_word.csv"), "w", encoding="utf-8") as f:
        f.write("char1,char2,count,pmi,adj_prob\n")
        for (a,b), c in pair_cross.items():
            if c < args.min_count: 
                continue
            pmi = pmi_cross.get((a,b), "")
            adjp = c / total if total else 0.0
            f.write(f"{a},{b},{c},{pmi},{adjp}\n")

    # 汇总：在词内 vs 跨词边界 的 PMI/概率对比统计（便于分析“成词概率”与 PMI 的关系）
    with open(os.path.join(args.output, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"total_pairs={total}\n")
        f.write(f"in_word_pairs={sum(pair_in.values())}, unique={len(pair_in)}\n")
        f.write(f"cross_word_pairs={sum(pair_cross.values())}, unique={len(pair_cross)}\n")
        f.write("Files: adjacent_pairs_in_word.csv, adjacent_pairs_cross_word.csv\n")

if __name__ == "__main__":
    main()

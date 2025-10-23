import argparse, os
from collections import Counter, defaultdict
from tqdm import tqdm
from utils.io_utils import read_lines, ensure_dir
from utils.text_utils import parse_seg_line
from utils.stats_utils import mutual_information_from_joint

def main():
    ap = argparse.ArgumentParser(description="任务2：任意两类词性之间的互信息（相邻词性对）")
    ap.add_argument("--input", required=True, help="已分词+词性 的语料（每行：词/pos 空格分隔）")
    ap.add_argument("--output", required=True, help="输出目录")
    ap.add_argument("--min_count", type=int, default=5, help="最小词性对计数")
    args = ap.parse_args()

    ensure_dir(args.output)

    joint = Counter()  # (pos_i, pos_{i+1}) -> count
    for line in read_lines(args.input):
        pairs = parse_seg_line(line)
        for i in range(len(pairs) - 1):
            _, p1 = pairs[i]
            _, p2 = pairs[i+1]
            if not p1 or not p2:
                continue
            joint[(p1, p2)] += 1

    # 计算互信息（逐对）
    mi = mutual_information_from_joint(joint)

    with open(os.path.join(args.output, "pos_pair_mi.csv"), "w", encoding="utf-8") as f:
        f.write("pos1,pos2,count,mi\n")
        for (p1, p2), c in sorted(joint.items(), key=lambda x: -x[1]):
            if c < args.min_count:
                continue
            f.write(f"{p1},{p2},{c},{mi.get((p1,p2), '')}\n")

    with open(os.path.join(args.output, "summary.txt"), "w", encoding="utf-8") as f:
        total_pairs = sum(joint.values())
        f.write(f"total_pos_pairs={total_pairs}\n")
        f.write(f"unique_pos_pairs={len(joint)}\n")
        f.write("File: pos_pair_mi.csv\n")

if __name__ == "__main__":
    main()

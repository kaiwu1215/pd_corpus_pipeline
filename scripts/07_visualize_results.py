
import argparse, os
import pandas as pd
import matplotlib.pyplot as plt

def _ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def _set_cn_font():
    import matplotlib
    for f in ["SimHei", "Microsoft YaHei", "Noto Sans CJK SC", "Arial Unicode MS", "PingFang SC", "WenQuanYi Zen Hei", "Source Han Sans CN", "Sarasa UI SC", "Heiti SC"]:
        try:
            matplotlib.rcParams["font.sans-serif"] = [f, "DejaVu Sans"]
            matplotlib.rcParams["axes.unicode_minus"] = False
            return
        except Exception:
            pass
    matplotlib.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False

def viz_task1(task_dir, topn=30):
    in_csv = os.path.join(task_dir, "adjacent_pairs_in_word.csv")
    cr_csv = os.path.join(task_dir, "adjacent_pairs_cross_word.csv")
    outd   = os.path.join(task_dir, "charts")
    _ensure_dir(outd)
    _set_cn_font()

    if os.path.exists(in_csv):
        df_in = pd.read_csv(in_csv)
        plt.figure()
        df_in["pmi"].dropna().hist(bins=50)
        plt.title("任务1：词内相邻二字 PMI 分布")
        plt.xlabel("PMI"); plt.ylabel("频数")
        plt.tight_layout(); plt.savefig(os.path.join(outd, "task1_inword_pmi_hist.png")); plt.close()

        plt.figure()
        plt.scatter(df_in["pmi"], df_in["adj_prob"])
        plt.title("任务1：词内相邻二字 PMI vs 邻近同现概率")
        plt.xlabel("PMI"); plt.ylabel("邻近同现概率")
        plt.tight_layout(); plt.savefig(os.path.join(outd, "task1_inword_pmi_vs_adjprob.png")); plt.close()

        top = df_in.dropna().sort_values("pmi", ascending=False).head(topn)
        plt.figure()
        plt.bar([f"{a}{b}" for a,b in zip(top["char1"], top["char2"])], top["pmi"])
        plt.title(f"任务1：词内 PMI Top{topn}")
        plt.xlabel("二字对"); plt.ylabel("PMI")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(outd, f"task1_inword_pmi_top{topn}.png")); plt.close()

    if os.path.exists(cr_csv):
        df_cr = pd.read_csv(cr_csv)
        plt.figure()
        df_cr["pmi"].dropna().hist(bins=50)
        plt.title("任务1：跨词相邻二字 PMI 分布")
        plt.xlabel("PMI"); plt.ylabel("频数")
        plt.tight_layout(); plt.savefig(os.path.join(outd, "task1_crossword_pmi_hist.png")); plt.close()

        plt.figure()
        plt.scatter(df_cr["pmi"], df_cr["adj_prob"])
        plt.title("任务1：跨词相邻二字 PMI vs 邻近同现概率")
        plt.xlabel("PMI"); plt.ylabel("邻近同现概率")
        plt.tight_layout(); plt.savefig(os.path.join(outd, "task1_crossword_pmi_vs_adjprob.png")); plt.close()

        top = df_cr.dropna().sort_values("pmi", ascending=False).head(topn)
        plt.figure()
        plt.bar([f"{a}{b}" for a,b in zip(top["char1"], top["char2"])], top["pmi"])
        plt.title(f"任务1：跨词 PMI Top{topn}")
        plt.xlabel("二字对"); plt.ylabel("PMI")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(outd, f"task1_crossword_pmi_top{topn}.png")); plt.close()

def viz_task2(task_dir, topn=30):
    csvp = os.path.join(task_dir, "pos_pair_mi.csv")
    outd = os.path.join(task_dir, "charts")
    _ensure_dir(outd); _set_cn_font()
    if not os.path.exists(csvp): return
    df = pd.read_csv(csvp)

    plt.figure()
    df["mi"].dropna().hist(bins=50)
    plt.title("任务2：相邻词性对 MI 分布")
    plt.xlabel("MI"); plt.ylabel("频数")
    plt.tight_layout(); plt.savefig(os.path.join(outd, "task2_pos_mi_hist.png")); plt.close()

    top_mi = df.dropna().sort_values("mi", ascending=False).head(topn)
    plt.figure()
    plt.bar([f"{a}-{b}" for a,b in zip(top_mi["pos1"], top_mi["pos2"])], top_mi["mi"])
    plt.title(f"任务2：词性对 MI Top{topn}")
    plt.xlabel("词性对"); plt.ylabel("MI")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout(); plt.savefig(os.path.join(outd, f"task2_pos_mi_top{topn}.png")); plt.close()

    top_ct = df.sort_values("count", ascending=False).head(topn)
    plt.figure()
    plt.bar([f"{a}-{b}" for a,b in zip(top_ct["pos1"], top_ct["pos2"])], top_ct["count"])
    plt.title(f"任务2：词性对 频数 Top{topn}")
    plt.xlabel("词性对"); plt.ylabel("频数")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout(); plt.savefig(os.path.join(outd, f"task2_pos_count_top{topn}.png")); plt.close()

def viz_task3(task_dir, topn=30):
    diff_csv = os.path.join(task_dir, "freq_diff.csv")
    new_txt  = os.path.join(task_dir, "new_words_2025_only.txt")
    outd = os.path.join(task_dir, "charts")
    _ensure_dir(outd); _set_cn_font()

    if os.path.exists(diff_csv):
        df = pd.read_csv(diff_csv)
        inc = df.sort_values("rel_diff", ascending=False).head(topn)
        dec = df.sort_values("rel_diff", ascending=True).head(topn)

        plt.figure()
        plt.bar(inc["word"], inc["rel_diff"])
        plt.title(f"任务3：相对频率增幅 Top{topn}（2025.01 vs 1998.01）")
        plt.xlabel("词"); plt.ylabel("相对频率差")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(outd, f"task3_rel_increase_top{topn}.png")); plt.close()

        plt.figure()
        plt.bar(dec["word"], dec["rel_diff"])
        plt.title(f"任务3：相对频率降幅 Top{topn}（2025.01 vs 1998.01）")
        plt.xlabel("词"); plt.ylabel("相对频率差")
        plt.xticks(rotation=60, ha="right")
        plt.tight_layout(); plt.savefig(os.path.join(outd, f"task3_rel_decrease_top{topn}.png")); plt.close()

    if os.path.exists(new_txt):
        words, counts = [], []
        with open(new_txt, "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line: continue
                sp = line.split("\t")
                if len(sp)!=2: continue
                words.append(sp[0]); counts.append(int(sp[1]))
        if words:
            s = pd.Series(counts, index=words).sort_values(ascending=False).head(topn)
            plt.figure()
            plt.bar(s.index.tolist(), s.values.tolist())
            plt.title(f"任务3：疑似新词 Top{topn}（2025.01 仅出现）")
            plt.xlabel("词"); plt.ylabel("频次")
            plt.xticks(rotation=60, ha="right")
            plt.tight_layout(); plt.savefig(os.path.join(outd, f"task3_newwords_top{topn}.png")); plt.close()

def main():
    ap = argparse.ArgumentParser(description="将任务1/2/3的计算结果转换为图表")
    ap.add_argument("--task1_dir", nargs="*", default=[], help="任务1输出目录（可多选）")
    ap.add_argument("--task2_dir", nargs="*", default=[], help="任务2输出目录（可多选）")
    ap.add_argument("--task3_dir", nargs="*", default=[], help="任务3输出目录（可多选）")
    ap.add_argument("--topn", type=int, default=30)
    args = ap.parse_args()

    for d in args.task1_dir: viz_task1(d, args.topn)
    for d in args.task2_dir: viz_task2(d, args.topn)
    for d in args.task3_dir: viz_task3(d, args.topn)

if __name__ == "__main__":
    main()

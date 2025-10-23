import argparse
import pandas as pd
from utils.io_utils import ensure_dir

def to_txt(df: pd.DataFrame, title_col: str, content_col: str, date_col: str):
    rows = []
    for _, r in df.iterrows():
        title = str(r.get(title_col, "")).strip() if title_col in df.columns else ""
        body  = str(r.get(content_col, "")).strip() if content_col in df.columns else ""
        date  = str(r.get(date_col, "")).strip() if date_col in df.columns else ""
        # 每行：日期\t标题\t正文
        rows.append(f"{date}\t{title}\t{body}")
    return rows

def main():
    ap = argparse.ArgumentParser(description="Excel -> txt (一行一篇：日期\\t标题\\t正文)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--title_col", default="标题")
    ap.add_argument("--content_col", default="正文")
    ap.add_argument("--date_col", default="发布时间")
    ap.add_argument("--sheet", default=0, help="如需指定工作表名称/索引")
    args = ap.parse_args()

    df = pd.read_excel(args.input, sheet_name=args.sheet)
    rows = to_txt(df, args.title_col, args.content_col, args.date_col)

    ensure_dir(os.path.dirname(args.output) or ".")
    with open(args.output, "w", encoding="utf-8") as f:
        for ln in rows:
            f.write(ln + "\\n")

if __name__ == "__main__":
    import os
    main()

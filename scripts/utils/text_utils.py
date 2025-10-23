import re

# 中文字符范围（含全角标点）
RE_CH = re.compile(r"[\u4e00-\u9fff]")
RE_KEEP = re.compile(
    r"[^\u4e00-\u9fffA-Za-z0-9，。、《》“”‘’：；？！—…·\-（）()、％%￥$：:；;,.!? ]+"
)
RE_MULTI_SPACE = re.compile(r"\s+")

def normalize_text(s: str, only_chinese: bool = True) -> str:
    s = s.strip()
    # 去掉 URL/邮箱/多余空白
    s = re.sub(r"https?://\S+|www\.\S+", " ", s)
    s = re.sub(r"\S+@\S+", " ", s)
    s = s.replace("\\t", " ").replace("\\r", " ")
    # 可选：仅保留中/英/数和常见中文标点
    if only_chinese:
        s = RE_KEEP.sub(" ", s)
    s = RE_MULTI_SPACE.sub(" ", s).strip()
    return s

def only_chinese_chars(s: str) -> str:
    return "".join(ch for ch in s if RE_CH.match(ch))

def parse_seg_line(line: str):
    # 将 "词/词性" 空格分隔的一行解析为 [(word, pos), ...]
    pairs = []
    for tok in line.strip().split():
        if "/" in tok:
            w, p = tok.rsplit("/", 1)
            if w:
                pairs.append((w, p))
        else:
            if tok:
                pairs.append((tok, ""))
    return pairs

def strip_pos_from_seg(line: str):
    # "词/pos 词/pos" -> "词 词"
    return " ".join(t.split("/")[0] if "/" in t else t for t in line.strip().split())

import os
from typing import Iterable

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def read_lines(path: str):
    # 尝试多种编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
    last_error = None
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                for line in f:
                    yield line.rstrip('\n')
            return
        except UnicodeDecodeError as e:
            last_error = e
            continue
    
    # 如果所有编码都失败，抛出最后一个错误
    raise last_error

def write_lines(path: str, lines: Iterable[str]):
    ensure_dir(os.path.dirname(path) or '.')
    with open(path, 'w', encoding='utf-8') as f:
        for ln in lines:
            f.write(ln + '\n')

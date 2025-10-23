import math
from collections import Counter
from typing import Dict, Tuple

def calc_pmi(pair_counts: Dict[Tuple[str, str], int],
             left_counts: Dict[str, int],
             right_counts: Dict[str, int],
             total_pairs: int):
    results = {}
    for (a, b), c in pair_counts.items():
        if c == 0: 
            continue
        pa = left_counts.get(a, 0) / total_pairs if total_pairs else 0
        pb = right_counts.get(b, 0) / total_pairs if total_pairs else 0
        pab = c / total_pairs if total_pairs else 0
        if pa > 0 and pb > 0 and pab > 0:
            pmi = math.log2(pab / (pa * pb))
            results[(a, b)] = pmi
    return results

def mutual_information_from_joint(joint: Dict[Tuple[str, str], int]):
    # MI(X;Y) = sum p(x,y) log(p(x,y) / (p(x)p(y)))
    total = sum(joint.values())
    if total == 0:
        return {}
    x_counts = Counter()
    y_counts = Counter()
    for (x, y), c in joint.items():
        x_counts[x] += c
        y_counts[y] += c
    res = {}
    for (x, y), c in joint.items():
        pxy = c / total
        px = x_counts[x] / total
        py = y_counts[y] / total
        if pxy > 0 and px > 0 and py > 0:
            res[(x, y)] = math.log2(pxy / (px * py))
    return res

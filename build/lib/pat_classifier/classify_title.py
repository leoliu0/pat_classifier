from . import split_words
from . import w_proc_re, w_prod_re, split_words
from collections import namedtuple
import re

re_imp = re.compile("(improvement|enhancement)\s+(in|on|of|for)")
re_w_and = re.compile(r" \w+ing,?\s+and")
re_ww = re.compile(r" (\w+ing) (and|or) (\w+ing)")
re_split = re.compile(split_words)

wplus = re.compile(r"[\w-]+")
w_proc_re = re.compile(w_proc_re)
w_prod_re = re.compile(w_prod_re)

Classification = namedtuple("Classification", "i, part, process")


def classify_partition(a):
    if a.endswith("production line"):
        return 1
    if w_prod_re.search(a):
        return 0
    try:
        a = wplus.findall(a)[-1].strip()
    except:
        return
    if w_proc_re.search(a):
        return 1
    return 0


def classify_title(s):
    result = []
    s = s.lower()
    s = re_imp.sub("", s)
    # print(s)
    s = re_ww.sub(r" \1 \3", s)
    s = re_w_and.sub("", s)
    for i, part in enumerate(s.split(" and "), start=1):
        part = re_split.split(part)[0]
        result.append(Classification._make([i, part, classify_partition(part)]))
    return result

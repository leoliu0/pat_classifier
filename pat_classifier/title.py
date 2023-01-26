from .common import split_words, w_proc_re, w_proc, w_proc_more, w_prod_re, split_words
from collections import namedtuple
import re
from typing import List, Dict
from nltk import pos_tag, word_tokenize

re_imp = re.compile("(improvement|enhancement)\s+(in|on|of|for)")
re_w_and = re.compile(r" \w+ing,?\s+and")
re_ww = re.compile(r" (\w+ing) (and|or) (\w+ing)")
re_split = re.compile(split_words)

wplus = re.compile(r"[\w-]+")
w_proc_re = re.compile(w_proc_re)
w_prod_re = re.compile(w_prod_re)

Classification = namedtuple("Classification", "i, part, process")


def classify_partition(a: str, dbg) -> int:
    if (
        "method and system" in a
        or "methods and system" in a
        or "system and method" in a
    ):
        return 1

    a = " ".join(
        [x for x, p in pos_tag(word_tokenize(a)) if p != "RB" and wplus.search(x)]
    ).strip()
    if dbg:
        print(a)
    try:
        first_word = wplus.findall(a)[0].strip()
        last_word = wplus.findall(a)[-1].strip()
    except:
        return

    if w_prod_re.search(a):
        return 0

    if w_proc_re.search(first_word):
        if dbg:
            print(f"first word process", w_proc_re.search(first_word))
        return 1

    if w_proc_re.search(last_word):
        if dbg:
            print(f"last word process", w_proc_re.search(last_word))
        return 1

    # for w in w_proc + w_proc_more:  # first tier of process words
    #     if a.endswith(w):
    #         if dbg:
    #             print(f"last word is process {w}")
    #         return 1
    return 0


def classify_title(s: str, dbg=0) -> List:
    result = []
    s = s.lower()
    s = re_imp.sub("", s)
    # print(s)
    s = re_ww.sub(r" \1 \3", s)
    s = re_w_and.sub("", s)
    for i, part in enumerate(s.split(" and "), start=1):
        part = re_split.split(part)[0]
        result.append(Classification._make([i, part, classify_partition(part, dbg)]))
    return result

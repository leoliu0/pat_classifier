import re
from nltk import word_tokenize, pos_tag
from .common import w_proc_re, w_prod_re, split_words

wplus = re.compile(r"[\w-]+")
w_proc_re = re.compile(w_proc_re)
w_prod_re = re.compile(w_prod_re)

split_by = re.compile(split_words)
mp_re = re.compile(r"\bprocess\b|\bmethod\b")
bracket_re = re.compile(r"\(.{,10}?\)")


def classify_claim(s, dbg=0):
    if dbg:
        print(s[:100])

    s = bracket_re.sub("", s)
    a = (
        s.split(".")[1]
        .strip()
        .lower()
        .replace(" improvement ", "")
        .replace(" combination of", "")
        .replace(" combination with", "")
    )
    if "by a process " in a or "by a method " in a:
        return 2
    # if "a process" in a[:20] or "a method" in a[:20]:
    if mp_re.search(a[:20]):
        return 1

    # n = 0
    # words = pos_tag(word_tokenize(a))
    # if dbg:
    #     print(words)
    # for i, (_, tag) in enumerate(words):
    #     if tag == "NN":
    #         n = i + 1
    #     if tag == "IN" and n > 0:
    #         break
    # if dbg:
    #     print("getting ", n)
    # a = " ".join([w for w, _ in words[:n]])

    a = split_by.split(a)[0].strip()
    # some bi-grams handled here
    if dbg:
        print(a, "==========")
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

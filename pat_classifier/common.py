from wordcloud import STOPWORDS
from importlib import resources
import pandas as pd
import re
from ._word_list import w_proc, w_prod

split_words = "of | for | or | having | derived from | from | combined with | with | using | used | as | to | on | in | based | via | prepared by | performed by | by | characterized | selected | exhibiting | compris.| containing | including | comprising | comprised | consisting | provide | provided | providing | produce | producing | define. | storing | allowing | enabling | adapted | which | that | where..| there..| according to | particular |\.|:"

stopwords = set(STOPWORDS) | set(["there\w+", "the"])
stopwords_regex = r"\b" + r"\b|\b".join(stopwords) + r"\b"

more_proc_words = resources.open_text("pat_classifier", "more_proc_words.txt")

w_proc_more = list(
    pd.read_csv(more_proc_words, sep=" ", names=["w", "n"]).w.str.lower()
)

w_proc2 = r"|".join(list(map(lambda s: r"\b" + str(s) + r"\b", w_proc_more)))

w_proc_re = "|".join(w_proc) + "|" + w_proc2
# w_proc_re = re.compile(w_proc + '|' + w_proc2)

product_words_list = resources.open_text("pat_classifier", "product_words_list.txt")
w_prod_re = (
    w_prod
    # + "|"
    # + r"|".join(
    #     list(
    #         pd.read_csv(product_words_list, sep=" ", names=["w", "n"])
    #         .w.str.lower()
    #         .str.replace("_", " ")
    #         .map(lambda s: r"\b" + str(s) + r"s?$")
    #     )
    # )
).strip("|")

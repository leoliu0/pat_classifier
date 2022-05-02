from pyspark import *
from pyspark.sql import *
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from wordcloud import STOPWORDS
from importlib import resources
import pandas as pd
import re
from ._word_list import w_proc

stopwords = set(STOPWORDS) | set(["there\w+", "the"])
stopwords_regex = r"\b" + r"\b|\b".join(stopwords) + r"\b"

additional_proc_words = resources.open_text("pat_classifier", "more_proc_words.txt")
w_proc2 = r"|".join(
    list(
        pd.read_csv(additional_proc_words, sep=" ", names=["w", "n"])
        .w.str.lower()
        .map(lambda s: str(s))
    )
)

w_proc_re = w_proc + "|" + w_proc2
# w_proc_re = re.compile(w_proc + '|' + w_proc2)

wl_proc = [
    x.replace("\\b", "").replace("$", "").replace("s?", "").replace("^", "")
    for x in (w_proc + "|" + w_proc2).split("|")
]

product_words_list = resources.open_text("pat_classifier", "product_words_list.txt")
w_prod_re = r"|".join(
    list(
        pd.read_csv(product_words_list, sep=" ", names=["w", "n"])
        .w.str.lower().str.replace('_',' ')
        .map(lambda s: r"\b" + str(s) + r"s?$")
    )
)

def pre_process(pat, strcolumn):
    pat = pat.withColumn(strcolumn, F.lower(strcolumn))  # lower case
    pat = pat.withColumn(  # remove improvement related phrase
        strcolumn,
        F.regexp_replace(
            F.col(strcolumn), "(improvement|enhancement) (in|on|of|for)", ""
        ),
    )
    pat = pat.withColumn(  # remove and between verbs so "and" can split correctly
        strcolumn,
        F.regexp_replace(F.col(strcolumn), r"(\w+ing) and (\w+ing)", r"\1 \2"),
    )
    pat = pat.withColumn(  # split by comma and "and" to get partitions
        strcolumn, F.split(strcolumn, "(?!.*ing),| and ")
    )
    pat = pat.withColumn(  # remove part after prepositions
        strcolumn, F.explode(strcolumn)
    )

    split_by = " of | for | having | with | using | used | to | on | in | based | via | by | including | comprising | comprised | provide | provided | providing | produce | producing | which | that "

    pat = pat.withColumn(  # split by conjection words
        strcolumn, F.split(strcolumn, split_by).getItem(0)
    )
    pat = pat.withColumn(  # remove stopwords
        strcolumn, F.regexp_replace(F.col(strcolumn), stopwords_regex, "")
    )
    pat = pat.withColumn(strcolumn, F.trim(strcolumn))  # additional cleanup
    pat = pat.withColumn(
        strcolumn, F.regexp_replace(F.col(strcolumn), r"\.|,|produced$", "")
    )
    pat = pat.dropna()
    return pat


def classify(df, strcolumn, debug=False):
    df = pre_process(df, strcolumn)
    df = df.withColumn("process_word", F.regexp_extract(strcolumn, w_proc_re, 0))
    df = df.withColumn("product_word", F.regexp_extract(strcolumn, w_prod_re, 0))

    df = df.withColumn("product", F.when(F.col("product_word") != "", 1).otherwise(0))
    df = df.withColumn(
        "process",
        F.when(
            (F.col("product_word") == "") & (F.col("process_word") != ""), 1
        ).otherwise(0),
    )
    df = df.withColumn("product", F.when(F.col("process") == 0, 1).otherwise(0))

    return df

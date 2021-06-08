from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from wordcloud import STOPWORDS
from importlib import resources
import pandas as pd
import re
from ._word_list import w_proc

stopwords = set(STOPWORDS) | set(['there\w+', 'the'])
stopwords_regex = r'\b' + r'\b|\b'.join(stopwords) + r'\b'

additional_proc_words = resources.open_text('pat_classifier',
                                            'additional_proc_words.txt')
w_proc2 = r'|'.join(
    list(
        pd.read_csv(additional_proc_words, sep=' ',
                    names=['w', 'n']).w.str.lower().map(lambda s: str(s))))

w_proc_re = re.compile(w_proc + '|' + w_proc2)

wl_proc = [
    x.replace('\\b', '').replace('$', '').replace('s?', '').replace('^', '')
    for x in (w_proc + '|' + w_proc2).split('|')
]

product_words_list = resources.open_text('pat_classifier',
                                         'product_words_list.txt')
w_prod_re = re.compile(r'\b' + r'|\b'.join(
    list(
        pd.read_csv(product_words_list, sep=' ', names=['w', 'n']).w.str.lower(
        ).map(lambda s: str(s) + r's?$'))))


def pre_process(pat):
    pat = pat.withColumn("title", F.lower("title"))  # lower case
    pat = pat.withColumn(  # remove improvement related phrase
        "title",
        F.regexp_replace(F.col("title"),
                         "(improvement|enhancement) (in|on|of|for)", ""))
    pat = pat.withColumn(  # remove and between verbs so "and" can split correctly
        "title",
        F.regexp_replace(F.col("title"), r"(\w+ing) and (\w+ing)", r"\1 \2"))
    pat = pat.withColumn(  # split by comma and "and" to get partitions
        'title', F.split('title', ',| and '))
    pat = pat.withColumn(  # remove part after prepositions
        'title', F.explode('title'))

    split_by = ' of | for | having | with | using | used | to | on | in | based | via | by | including | comprising | comprised | provide | provided | providing | produce | producing | which | that '

    pat = pat.withColumn(  # split by conjection words
        'title',
        F.split('title', split_by).getItem(0))
    pat = pat.withColumn(  # remove stopwords
        'title', F.regexp_replace(F.col('title'), stopwords_regex, ''))
    pat = pat.withColumn(  # additional cleanup
        'title', F.trim('title'))
    pat = pat.withColumn(
        'title', F.regexp_replace(F.col('title'), r'\.|,|produced$', ''))
    pat = pat.dropna().toPandas()
    return pat

# ----------------------------------------------------------------------
# Information
# ----------------------------------------------------------------------
#
# Pre-processing ECB introduction statements
#
# (Author) Hans-Peter Höllwirth
# (Date)   06.2017

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import pandas as pd
import numpy as np
import nltk
import re
import matplotlib.pyplot as plt
import datetime
import os

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
#nltk.download('all')
from textblob import TextBlob
from collections import Counter
from copy import deepcopy

os.chdir("/Users/Hans-Peter/Documents/Masters/14D010/project/code")


# ----------------------------------------------------------------------
# Pre-processing steps
# ----------------------------------------------------------------------
def split_into_tokens(text):
    # function splits a text string into its individual words/tokens
    # text = unicode(text, 'utf8') - convert bytes into proper unicode (text already unicode)
    return TextBlob(text).words

def alpha_numeric(text):
    # function removes non-alphanumeric characters using regular expressions
    alpha_clean = [re.sub("[^a-zA-Z]+", "", item) for item in text]
    return [item for item in alpha_clean if item != ""]

def remove_stop_words(text):
    # function removes stop words from strings
    stop = stopwords.words('english')
    filtered_words = [item for item in text if item not in stop]
    return filtered_words

def stemming_words(text):
    # function stems words using the Porter Stemmer
    p_stemmer = PorterStemmer()
    return [p_stemmer.stem(i) for i in text]

def clean_text(text):
    # function combines all of the previous text-cleaning functions
    df_tokens = text.apply(split_into_tokens)          # (1) tokenize text
    df_tokens_lower = df_tokens.str.lower()            # (2) case folding
    df_alpha = df_tokens_lower.apply(alpha_numeric)    # (3) remove non-alphanumeric characters
    df_stop = df_alpha.apply(remove_stop_words)        # (4) remove stop words
    df_stem = df_stop.apply(stemming_words)            # (5) stemming
    return df_stem                                     # (6) return array of tokens per document

def remove_topic_stop_words(text, threshold = 0.1):
    # remove topic stop words from grouped text
    D = text.size

    # form vocabulary list
    voc = list()
    for i in range(text.size):
        voc.extend(text.values[i])
    voc = list(set(voc))

    # compute tf-idf term for each vocabulary word and form stopword list
    cnt_tf = Counter(text.sum())
    cnt_idf = Counter(text.apply(lambda x: list(set(x))).sum())
    stop = [w for w in voc if ((1 + np.log(cnt_tf[w])) * np.log(D / cnt_idf[w])) < threshold]
    print(sorted(stop))

    # filter stopwords from text
    return text.apply(lambda d: [w for w in d if w not in stop])


# ----------------------------------------------------------------------
# Run text pre-processing
# ----------------------------------------------------------------------

# read data file
data = pd.read_table('../data/combined.csv', sep=',', encoding='utf-8')
text_raw = data['Text']
date_raw = data['Date']

len(text_raw)

# text pre-processing
text_cleaned = clean_text(text_raw)
text_process = remove_topic_stop_words(text_cleaned, threshold=1.0)

# ----------------------------------------------------------------------
# Information
# ----------------------------------------------------------------------
#
# Latent Dirichlet Allocation (LDA) analysis
#
# (Author) Hans-Peter Höllwirth
# (Date)   06.2017

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import pandas as pd
import lda
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.feature_extraction.text import CountVectorizer

os.chdir("/Users/Hans-Peter/Documents/Masters/14D010/project/code")


# ----------------------------------------------------------------------
# Form document-term matrix
# ----------------------------------------------------------------------
def form_docterm_matrix(text_terms):
    # form document-term matrix from grouped list of text terms
    text_joined = text_terms.copy()
    count = 0
    for i in text_joined:
        text_joined[text_terms.index[count]] = " ".join(i)
        count += 1

    countvec = CountVectorizer()
    dtm = countvec.fit_transform(text_joined)
    return dtm
    #vocab = countvec.get_feature_names()
    #years = text_grouped_unlisted.index
    #D = len(years)

# ----------------------------------------------------------------------
# Plotting functions
# ----------------------------------------------------------------------
def plot_topic_distr(doc_topics, dates):
    # function plots topic distribution (doc_topoics) over time (dates)
    T3 = pd.DataFrame(doc_topics)
    T3.index = list(pd.to_datetime(dates))
    fig,ax = plt.subplots()
    T3.plot(x_compat=True,ax=ax)
    ax.xaxis.set_tick_params(reset=True)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.format_xdata = mdates.DateFormatter('%Y')
    ax.grid(True)
    plt.title('Topic distribution over years')
    plt.xlabel('year')
    plt.ylabel('topic distribution')
    plt.legend()
    fig.autofmt_xdate()
    plt.show()
    plt.close()

# ----------------------------------------------------------------------
# Run LDA analysis
# ----------------------------------------------------------------------

text_dtm = form_docterm_matrix(text_process)

# fit LDA model
model = lda.LDA(n_topics=3, n_iter=1000, alpha=0.1, eta=0.1, random_state=1)
model.fit(text_dtm)

# store result
doc_topics = model.doc_topic_
topic_words = model.topic_word_
log_likelihoods = model.loglikelihoods_

# plot topic distributions over time
plot_topic_distr(doc_topics, date_raw)

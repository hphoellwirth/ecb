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
import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

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

def get_vocabulary(text_terms):
    # get vocabulary list from text-term list
    text_joined = text_terms.copy()
    count = 0
    for i in text_joined:
        text_joined[text_terms.index[count]] = " ".join(i)
        count += 1

    countvec = CountVectorizer()
    dtm = countvec.fit_transform(text_joined)
    voc = countvec.get_feature_names()
    return voc



# ----------------------------------------------------------------------
# Plotting functions
# ----------------------------------------------------------------------
def plot_topic_distr(doc_topics, dates, file_name=None):
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
    if not file_name:
        plt.show()
    else:
        plt.savefig('../images/'+ file_name +'.png', dpi=300)
    plt.close()

# ----------------------------------------------------------------------
# Run LDA analysis
# ----------------------------------------------------------------------
def topic_distribution_plot(text, K):
    # fit LDA model for K topics and plot (+ save) result
    text_dtm = form_docterm_matrix(text)
    model = lda.LDA(n_topics=K, n_iter=1000, alpha=0.1, eta=0.1, random_state=1)
    model.fit(text_dtm)
    doc_topics = model.doc_topic_
    plot_topic_distr(doc_topics, date_raw, file_name='topicDistr_K'+str(K))

# create topic distribution plots for various K
topic_distribution_plot(text_process, 2)
topic_distribution_plot(text_process, 3)
topic_distribution_plot(text_process, 4)

# fit LDA model
K=3
text_dtm = form_docterm_matrix(text_process)
model = lda.LDA(n_topics=K, n_iter=1000, alpha=0.1, eta=0.1, random_state=1)
model.fit(text_dtm)

# plot topic distributions over time
plot_topic_distr(model.doc_topic_, date_raw)

# most common words in each topic
voc = get_vocabulary(text_process)
for k in range(K):
    wl = [voc[n] for n in np.argpartition(model.nzw_[k], -10)[-10:]]
    print(k,':',wl)

help(WordCloud().fit_words)

wl = [voc[n] for n in np.argpartition(model.nzw_[0], -10)[-10:]]
wl = [model.nzw_[0,n] for n in np.argpartition(model.nzw_[0], -10)[-10:]]
wl = [(voc[n], model.nzw_[0,n]) for n in np.argpartition(model.nzw_[0], -10)[-10:]]

dict(wl)

# plot word clouds
for k in range(K):
    wl = [(voc[n], model.nzw_[k,n]) for n in np.argpartition(model.nzw_[k], -10)[-10:]]
    plt.figure()
    plt.imshow(WordCloud().fit_words(dict(wl)))
    plt.axis("off")
    plt.title("Topic #" + str(k))
    plt.show()

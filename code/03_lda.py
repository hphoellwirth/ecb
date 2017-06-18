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
#import Image
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
def plot_topic_distr(doc_topics, dates, K, file_name=None):
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
    plt.legend([str(i+1) for i in list(range(K))])
    fig.autofmt_xdate()
    if not file_name:
        plt.show()
    else:
        plt.savefig('../images/'+ file_name +'.png', dpi=300)
    plt.close()

def plot_wordcloud(voc, freq_matrix, k, n_words=25, file_name=None):
    # plot word cloud for topic k with n_words
    word_freq = [(voc[n], freq_matrix[k,n]) for n in np.argpartition(freq_matrix[k], -n_words)[-n_words:]]
    word_cloud = WordCloud(background_color='white',width=1200,height=1000,margin=0).fit_words(dict(word_freq))
    plt.figure()
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.title('Topic ' + str(k+1))
    if not file_name:
        plt.show()
    else:
        plt.savefig('../images/'+ file_name +'.png', dpi=150)

# ----------------------------------------------------------------------
# Run LDA analysis
# ----------------------------------------------------------------------
def topic_distribution_plot(text, K):
    # fit LDA model for K topics and plot (+ save) result
    text_dtm = form_docterm_matrix(text)
    model = lda.LDA(n_topics=K, n_iter=1000, alpha=0.1, eta=0.1, random_state=1)
    model.fit(text_dtm)
    doc_topics = model.doc_topic_
    plot_topic_distr(doc_topics, date_raw, K, file_name='topicDistr_K'+str(K))

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
plot_topic_distr(model.doc_topic_, date_raw, K)

# find most common words in each topic
voc = get_vocabulary(text_process)
topic_word = model.topic_word_
n_top_words = 10
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(voc)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i+1, ' '.join(topic_words)))

# plot word clouds
for k in range(K):
    plot_wordcloud(voc, model.nzw_, k, n_words=50, file_name='wordCloud_K3_'+str(k+1))

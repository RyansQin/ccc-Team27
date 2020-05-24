from textblob import TextBlob
import requests
import json
import time
import numpy as np
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models


db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']

headers = {'content-type': 'application/json'}



def updateResult(database, content, docID):
    url = 'http://localhost:5000/cluster/update'
    payload = {'database': database, 'docID': docID, 'content': content}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)

def fetchText(database):
    url = 'http://localhost:5000/cluster/text/' + database
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

def getViewResult(database, task):
    url = 'http://localhost:5000/view/result/' + task + '/' + database
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


def cluestering(db_name):
    print("Start analyze on the database: ", db_name)
    result = []

    print('[===== Get Twitter Data =====]')
    data = fetchText(db_name)
    doc_set = data[db_name]

    print('[===== Delete Stop words =====]')
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    search_words = ['lockdown', 'stay', 'home', 'stayhome']
    useless_words = ['s', 'm', 't', 'w', 'can', 'go', 'peopl', 'just', 'like', 'will', 've', 'd', 'may', 'wa', 'thi',
                     'start', 'even', 'ha', 'start', 'now', 'get', 're', 'onli', 'don', 'victoria', 'time', 'day',
                     'still',
                     'one', 'ye', 'pleas']
    stop_words = en_stop + search_words + useless_words
    p_stemmer = PorterStemmer()

    print('[===== Create text list =====]')
    texts = []
    for doc in doc_set:
        raw = doc.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [i for i in tokens if i not in stop_words]
        text = [p_stemmer.stem(i) for i in stopped_tokens]
        stopped_text = [i for i in text if i not in useless_words]
        useful_text = [i for i in stopped_text if len(i) >= 2]
        texts.append(useful_text)
    M = len(texts)
    # print(texts)

    print('[===== Create dictionary =====]')
    dictionary = corpora.Dictionary(texts)

    print('[===== Calculate text vectors] =====')
    corpus = [dictionary.doc2bow(text) for text in texts]

    print('[===== Calculate TF-IDF =====]')
    t_start = time.time()
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    # print('Time used is %.3f sec.' % (time.time() - t_start))

    print('[===== Create LDA model =====]')
    num_topics = 5
    t_start = time.time()
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, alpha=0.01, eta=0.01,
                          minimum_probability=0.001, update_every=1, chunksize=100, passes=50)
    # print('Time used for creating model is %.3f' % (time.time() - t_start))

    print('[===== Result, topic of each documents =====]')
    num_show_topics = 5
    doc_topics = lda.get_document_topics(corpus_tfidf)
    idx = np.arange(M)
    np.random.shuffle(idx)
    for i in idx:
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        topic_idx = topic_distribute.argsort()[:-num_show_topics - 1:-1]
        # print("Top %d topics of No.%d document: " % (i, num_show_topics), topic_idx)
        # print(topic_distribute[topic_idx])

    print('[===== Result, word distribution of each topic =====]')
    num_show_term = 5
    for topic_id in range(num_topics):
        cluster_text = ""
        print('Topic %d: \t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id)
        term_distribute = term_distribute_all[:num_show_term]
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        print('word: \t', )
        for t in term_id:
            cluster_text = cluster_text + dictionary.id2token[t] + " "
            print(dictionary.id2token[t], end=" ")
        print('\nprobability: \t', term_distribute[:, 1])
        result.append(cluster_text)

    res = []
    res.append('cluserRes')
    res.append(result)
    return res

    # ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=50)
    # print(ldamodel.print_topics(num_topics=8, num_words=3))
    # name = db_name.split("_")[1]
    # updateResult('nlp_res', {'clusterRes': result}, name)


def sentimentAnalyze(database):
    sentiment_results = {}
    print("Start analyze on the database: ", database)
    twiiter_count = 0
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    textData = fetchText(database)
    textSet = textData[database]

    for text in textSet:
        twiiter_count += 1

        blob = TextBlob(text)
        if blob.sentiment.polarity >= 0.1:
            positive_count += 1
        elif blob.sentiment.polarity <= -0.1:
            negative_count += 1
        else:
            neutral_count += 1

    positive_proportion = positive_count / twiiter_count
    negative_proportion = negative_count / twiiter_count
    neutral_proportion = neutral_count / twiiter_count

    sentiment_results['positive_proportion'] = round(positive_proportion, 3)
    sentiment_results['negative_proportion'] = round(negative_proportion, 3)
    sentiment_results['neutral_proportion'] = round(neutral_proportion, 3)

    res = []
    res.append('sentimentRes')
    res.append(sentiment_results)
    return res

def updateNLPResult(database):
    res1 = cluestering(database)
    res2 = sentimentAnalyze(database)
    res = []
    res.append(res1)
    res.append(res2)
    name = database.split('_')[1]
    updateResult('analysis_res', {'lockdownRank':res}, name)

def updateView(location, task):
    newestData = getViewResult(location, task)
    updateResult('analysis_res', newestData, location)

locLst = ['ade', 'nsw', 'per', 'nor', 'can', 'tas', 'vic', 'que']
task = ['covidRate', 'curve']



for db in db_list:
    updateNLPResult(db)
for t in task:
    for loc in locLst:
        updateView(loc, t)

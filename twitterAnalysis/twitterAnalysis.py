'''

@Author: XinKai Luo, Tai Qin

This file is for updating twiiter analysis result.
'''


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


# Send a http requset with the POST method
# update specific document in the given database
def updateResult(database, content, docID):
    url = 'http://172.26.131.203:8000/analysis/result'
    payload = {'database': database, 'docID': docID, 'content': content}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)


# For the given database, get the content of test field of all documents
def fetchText(database):
    url = 'http://172.26.131.203:8000/analysis/text/' + database
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

# Access the latest result of the views from CouchDB
def getViewResult(database, task):
    url = 'http://172.26.131.203:8000/view/result/' + task + '/' + database
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

# For the given database, fetch all text and use the LDA model to analysis what people concern during lockdown
def cluestering(db_name):
    print("Start analyze on the database: ", db_name)
    result = []

    # fetch text
    print('[===== Get Twitter Data =====]')
    data = fetchText(db_name)
    doc_set = data[db_name]

    # Delete useless words, including stop words and some words we believe are useless
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

    # create the LDA model, the top 5 topic will be return in a list

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


# For the given database, get all text and do sentiment analysis.
# The proportion of positive, negetive and neutral attitude will be returned
def sentimentAnalyze(database):
    sentiment_results = {}
    print("Start analyze on the database: ", database)
    twiiter_count = 0
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # fetch text
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


# update the result of clustering and sentiment analysis
def updateNLPResult(database):
    res1 = cluestering(database)
    res2 = sentimentAnalyze(database)
    res = []
    res.append(res1)
    res.append(res2)
    name = database.split('_')[1]
    print(res)
    updateResult('analysis_res', {'lockdownRank':res}, name)


# update the result of mapreduce function that we defined in the couchdb
def updateView(location, task):
    newestData = getViewResult(location, task)
    updateResult('analysis_res', newestData, location)

locLst = ['ade', 'nsw', 'per', 'nor', 'can', 'tas', 'vic', 'que']
task = ['covidRate', 'curve']


# update all result of twitter analysis
curTask = 'NLP Task'
curDatabae = 'ade'
try:
    for db in db_list:
        curDatabae = db
        updateNLPResult(db)
    curTask = 'covidRate'
    for t in task:
        curTask = t
        for loc in locLst:
            curDatabae = loc
            updateView(loc, t)
except:
    error_str = 'error occurs while updating ' + curTask + ' in ' + curDatabae
    print(error_str)


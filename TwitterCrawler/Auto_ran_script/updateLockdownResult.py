import time
import numpy as np
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import json
import requests

db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']
headers = {'content-type':'application/json'}

def updateResult(database, content, docID):
    url = 'http://172.26.131.203:8000/cluster/update'
    payload = {'database': database, 'docID': docID, 'content': content}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)

def fetchText(database):
    url = 'http://172.26.131.203:8000/cluster/text'
    payload= {'database': database}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)
    return data

for db_name in db_list:

    print("Start analyze on the database: ", db_name)
    result = []

    print('[===== Get Twitter Data =====]')
    data= fetchText(db_name)
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

    # ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=50)
    # print(ldamodel.print_topics(num_topics=8, num_words=3))
    name = db_name.split("_")[1]
    updateResult('nlp_res', {'clusterRes':result}, name)

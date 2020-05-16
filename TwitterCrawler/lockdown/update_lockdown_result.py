import couchdb
import time
import numpy as np
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models

# db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']
# db_list = ['lockdown_ade','lockdown_can','lockdown_nor']
db_list = ['lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']

server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
db_result = server['lockdown_results']
# update_results = db_result.get("a3edfd4621f8934dd0d658d0e3b13028")
for db_name in db_list:
    update_results = db_result.get("a3edfd4621f8934dd0d658d0e3b13028")
    print("Start analyze on the database: ", db_name)
    update_results[db_name]=[]


    print('[===== Get Twitter Data =====]')
    db = server[db_name]

    i = 0
    doc_set = []
    for id in db:
        i += 1
        # print(i, '  ', db[id]['text'])
        doc_set.append(db[id]['text'])

        # if i == 1000:
        #     break

    print('[===== Delete Stop words =====]')
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    search_words = ['lockdown', 'stay', 'home', 'stayhome']
    useless_words = ['s', 'm', 't', 'w', 'can', 'go', 'peopl', 'just', 'like', 'will', 've', 'd', 'may', 'wa', 'thi',
                     'start', 'even', 'ha', 'start', 'now', 'get', 're', 'onli', 'don', 'victoria', 'time', 'day', 'still',
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
        useful_text = [i for i in stopped_text if len(i)>=2]
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
    num_topics = 3
    t_start = time.time()
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, alpha=0.01, eta=0.01,
                          minimum_probability=0.001, update_every=1, chunksize=100, passes=50)
    # print('Time used for creating model is %.3f' % (time.time() - t_start))

    print('[===== Result, topic of each documents =====]')
    num_show_topics = 3
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
        print('word: \t',)
        for t in term_id:
            cluster_text = cluster_text + dictionary.id2token[t] + " "
            print(dictionary.id2token[t], end=" ")
        print('\nprobability: \t', term_distribute[:, 1])
        update_results[db_name].append(cluster_text)


    # ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=50)
    # print(ldamodel.print_topics(num_topics=8, num_words=3))
    db_result.save(update_results)
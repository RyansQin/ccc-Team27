import couchdb

server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
db = server['tweet_test']

i = 0
for id in db:
    i+=1

    print(i,'  ',db[id]['text'])
import tweepy
import couchdb
import re

server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
# db = server.create('lockdown_nsw')
db = server['lockdown_nsw']

# # Kevin
# consumer_key = "v918I7H2QJsIkYymHo5khE74f"
# consumer_secret = "5VcGYE1TUDx7i5aE2onTpWKcTPgJBx3U3LqybbE7kOu133l3z1"
# access_token = "1251803998555762693-eO27dyOYtNlfEMguCnPA2YHtvsYauA"
# access_token_secret = "jfckecjtPbaXoKU5LjFxL8NUSvOtxXrtqRCsfaycXrgiV"

# 理查德老师
consumer_key = "Rz89nxFrVyhZTUX3eoBi05m6j"
consumer_secret = "o9Cdfk7W6qfpTDYTx4tHFW2FQxEkALvIu2VSCPbbNVkyTniVjf"
access_token = "1251802835177504770-VEcU0oHI2Kx0BTPv3MEKgpMarQcUqG"
access_token_secret = "iyhMSbmY5xm2w3BZEVvgZ1Y6TUwJcgKmSIniBGMi4oEyL"

# 泰霸
# consumer_key = "n0FRrHfmZImwPiuzPQ5CGmFiI"
# consumer_secret = "BFUOm6PuPBAY5jzi4CvIsfwk97dwtpdmRlEmWCCkOF1IlsQ9dj"
# access_token = "1251879426746277889-dp7UT86bYaxB9dYZ1SR9i4LlPLHcwY"
# access_token_secret = "cC9zCNr7Awqvra8DtZkQl8TaYPAMNLGikKrpDJI4UGUSx"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

maxId = '1259739535451160576'
batch = 0
n = 0
last_hash = ''
last_id = ''
last_time = ''
while True:

    # search_results = api.search(q='lockdown', count=100, geocode='-33.8688,151.2093,100km',lang='en', max_id=maxId, since_id=1257837905860419584)
    # search_results = api.search(q='lockdown', count=100, geocode='-33.8688,151.2093,100km', lang='en')
    # search_results = api.search(q='#stayhome', count=100, geocode='-33.8688,151.2093,100km', lang='en', max_id=maxId, since_id=1257834836758163456)
    # search_results = api.search(q='#stayhome', count=100, geocode='-33.8688,151.2093,100km', lang='en')
    search_results = api.search(q='stay home', count=100, geocode='-33.8688,151.2093,100km', lang='en', max_id=maxId, since_id=1257834949068992512)
    # search_results = api.search(q='stay home', count=100, geocode='-33.8688,151.2093,100km', lang='en')

    for tweet in search_results:
        maxId = tweet._json['id']

        # 这里是检测消息是否含有'text'键,并不是所有TWitter返回的所有对象都是消息(有些可能是用来删除消息或者其他内容的动作--这个没有确认),区别就是消息对象中是否含有'text'键
        if 'text' in tweet._json and tweet._json['text'][0:2] != 'RT':
            # 去网址，很多text内容一样仅网址不同
            remove_url = re.compile(r'(https|http)://[a-zA-Z0-9.?/&=:]*', re.S)
            tweet._json['text'] = remove_url.sub('', tweet._json['text'])
            remove_atname = re.compile(r'@[a-zA-Z0-9.?/&=:_]*', re.S)
            tweet._json['text'] = remove_atname.sub('', tweet._json['text']).strip()
            tweet._json['text'] = tweet._json['text'].replace('\n', '')

            # print(tweet._json['text'])
            # print(tweet._json['created_at'])
            # print(tweet._json['id'])
            # print()

            tweets = {}
            tweets['id'] = tweet._json['id']
            tweets['time'] = tweet._json['created_at']
            tweets['text'] = tweet._json['text']
            tweets['language_code'] = tweet._json['metadata']['iso_language_code']
            tweets['user_location'] = tweet._json['user']['location']
            tweets['geo'] = tweet._json['geo']
            tweets['coordinates'] = tweet._json['coordinates']
            tweets['lang'] = tweet._json['lang']

            last_id = tweet._json['id']
            last_time = tweet._json['created_at']

            if hash(tweet._json['text']) == last_hash:
                continue

            last_hash = hash(tweet._json['text'])
            n += 1
            # db.save(tweets)

    batch += 1
    print(batch, '  ', n, '  ', last_id, '  ', last_time)
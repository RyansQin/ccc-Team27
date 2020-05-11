import tweepy
import couchdb
import re

server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
# db = server.create('lockdown_per')
db = server['lockdown_per']

# # Kevin
# consumer_key = "v918I7H2QJsIkYymHo5khE74f"
# consumer_secret = "5VcGYE1TUDx7i5aE2onTpWKcTPgJBx3U3LqybbE7kOu133l3z1"
# access_token = "1251803998555762693-eO27dyOYtNlfEMguCnPA2YHtvsYauA"
# access_token_secret = "jfckecjtPbaXoKU5LjFxL8NUSvOtxXrtqRCsfaycXrgiV"

# 理查德老师
# consumer_key = "Rz89nxFrVyhZTUX3eoBi05m6j"
# consumer_secret = "o9Cdfk7W6qfpTDYTx4tHFW2FQxEkALvIu2VSCPbbNVkyTniVjf"
# access_token = "1251802835177504770-VEcU0oHI2Kx0BTPv3MEKgpMarQcUqG"
# access_token_secret = "iyhMSbmY5xm2w3BZEVvgZ1Y6TUwJcgKmSIniBGMi4oEyL"

# # 泰霸
# consumer_key = "n0FRrHfmZImwPiuzPQ5CGmFiI"
# consumer_secret = "BFUOm6PuPBAY5jzi4CvIsfwk97dwtpdmRlEmWCCkOF1IlsQ9dj"
# access_token = "1251879426746277889-dp7UT86bYaxB9dYZ1SR9i4LlPLHcwY"
# access_token_secret = "cC9zCNr7Awqvra8DtZkQl8TaYPAMNLGikKrpDJI4UGUSx"

# 钟人杰
# consumer_key = "wRsKRDZJfHdKy1akuqNxDGPXF"
# consumer_secret = "waPP63h05QzOpCnrDtQTqqHVf5PMwIJ2LsX19zz1h0ADgn2PlU"
# access_token = "1251803713183739904-AHBkqtmTzOZldsrVk7vn06e1Q2czh5"
# access_token_secret = "Jho2DSbkYK7A7umkxQiK5PXT7sBbLPYLkLEXGPFWFBBaQ"

# 国内哥
consumer_key = "WFkwOMzzK6fCrObMnYld8tYqv"
consumer_secret = "lG5lKsbo5OzL0u3zqKrWLyoQfAR9u0ezZR5oilNh1IXDIeIeqt"
access_token = "1251807534492479488-1sAAzRfTOCXkpAMX6XovKFtChIcqRR"
access_token_secret = "lJjTiWZjzNRMzJPBTkXxiZ53HDC0wJxrhB9aOpKvgd9ZK"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

maxId = '1259734249101377538'
batch = 0
n = 0
last_hash = ''
last_id = ''
last_time = ''
while True:

    # search_results = api.search(q='lockdown', count=100, geocode='-31.9505,115.8605,100km', lang='en',max_id=maxId, since_id=1257833893509525505)
    # search_results = api.search(q='lockdown', count=100, geocode='-31.9505,115.8605,100km', lang='en')
    # search_results = api.search(q='stayhome', count=100, geocode='-31.9505,115.8605,100km', lang='en', max_id=maxId, since_id=1257600464142680070)
    # search_results = api.search(q='stayhome', count=100, geocode='-31.9505,115.8605,100km', lang='en')
    search_results = api.search(q='stay home', count=100, geocode='-31.9505,115.8605,100km', lang='en', max_id=maxId, since_id=1257837314526441472)
    # search_results = api.search(q='stay home', count=100, geocode='-31.9505,115.8605,100km', lang='en')

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
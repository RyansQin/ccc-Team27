import tweepy
import couchdb
import re
import traceback

consumer_key = "n0FRrHfmZImwPiuzPQ5CGmFiI"
consumer_secret = "BFUOm6PuPBAY5jzi4CvIsfwk97dwtpdmRlEmWCCkOF1IlsQ9dj"
access_token = "1251879426746277889-dp7UT86bYaxB9dYZ1SR9i4LlPLHcwY"
access_token_secret = "cC9zCNr7Awqvra8DtZkQl8TaYPAMNLGikKrpDJI4UGUSx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

search_list = ['lockdown','stayhome','stay home']
db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']
geocode_list = ['-34.9285,138.6007,100km','-35.2809,149.1300,20km','-12.4634,130.84560,200km','-33.8688,151.2093,100km',
                '-31.9505,115.8605,100km','-27.4698,153.0251,50km','-41.4545,145.9707,100km','-37.8136,144.9631,100km']

f = open('lockdown_max_id.txt','r')
sinceId = f.read()
f.close()

first = True

for j in range(8):
    print("Start getting data for ", db_list[j])
    server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
    db = server[db_list[j]]

    for search_word in search_list:
        print("     Start searching for ", search_word,' in ', db_list[j])
        maxId = '12597492028624121883712'
        batch = 0
        n = 0
        last_hash = ''
        last_id = ''
        last_time = ''

        while True:
            try:
                search_results = api.search(q=search_word,count=100, geocode=geocode_list[j],lang='en',max_id=maxId,since_id=1262164012256591877)
                if len(search_results) == 0:
                    print("        No result for ", search_word, 'in ', db_list[j])
                    print()
                    break

                if len(search_results) == 1:
                    print('    ',db_list[j],':',search_word," Search Done!")
                    print()
                    break

                for tweet in search_results:
                    maxId = tweet._json['id']

                    if first:
                        f1 = open('lockdown_max_id.txt', 'w')
                        f1.write(str(tweet._json['id']))
                        f1.close()
                        first = False

                    # Testing if there is a 'text' field in twitter message and if it is a retweet
                    if 'text' in tweet._json and tweet._json['text'][0:2] != 'RT':
                        # 去网址，很多text内容一样仅网址不同
                        remove_url = re.compile(r'(https|http)://[a-zA-Z0-9.?/&=:]*', re.S)
                        tweet._json['text'] = remove_url.sub('', tweet._json['text'])
                        remove_atname = re.compile(r'@[a-zA-Z0-9.?/&=:_]*',re.S)
                        tweet._json['text'] = remove_atname.sub('', tweet._json['text']).strip()
                        tweet._json['text'] = tweet._json['text'].replace('\n', '')

                        # record the useful information for each tweet
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
                print('        ',batch,'  ',n,'  ', last_id,'  ', last_time)
            except Exception as e:
                traceback.print_exc()
                continue

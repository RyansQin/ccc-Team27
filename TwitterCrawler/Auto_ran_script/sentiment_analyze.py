from textblob import TextBlob
import couchdb

db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']
state_list = ['ADE','CAN','NOR','NSW','PER','QUE','TAS','VIC']

server = couchdb.Server('http://admin:qwert12345@172.26.133.41:8082/')
db_result = server['lockdown_results']

for j in range(8):
    sentiment_results = db_result.get("a542f8b73896f94acb6b8c7e1b073b39")
    print("Start analyze on the database: ", db_list[j])
    sentiment_results[state_list[j]]={}

    print('[===== Get Twitter Data =====]')
    db = server[db_list[j]]

    twiiter_count = 0
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for id in db:
        twiiter_count += 1
        text = db[id]['text']
        blob = TextBlob(text)
        if blob.sentiment.polarity >= 0.1:
            positive_count += 1
        elif blob.sentiment.polarity <= -0.1:
            negative_count += 1
        else:
            neutral_count += 1

    positive_proportion = positive_count/twiiter_count
    negative_proportion = negative_count/twiiter_count
    neutral_proportion = neutral_count / twiiter_count

    sentiment_results[state_list[j]]['positive_proportion'] = round(positive_proportion,3)
    sentiment_results[state_list[j]]['negative_proportion'] = round(negative_proportion,3)
    sentiment_results[state_list[j]]['neutral_proportion'] = round(neutral_proportion,3)

    db_result.save(sentiment_results)

    print(state_list[j],' Analyze Done')

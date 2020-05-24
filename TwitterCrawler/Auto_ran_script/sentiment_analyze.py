from textblob import TextBlob
import requests
import json

db_list = ['lockdown_ade','lockdown_can','lockdown_nor','lockdown_nsw','lockdown_per','lockdown_que','lockdown_tas','lockdown_vic']

headers = {'content-type': 'application/json'}



def updateResult(database, content, docID):
    url = 'http://172.26.131.203:8000/cluster/update'
    payload = {'database': database, 'docID': docID, 'content': content}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)

def fetchText(database):
    url = 'http://172.26.131.203:8000/cluster/text/database'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

# def sentimentAnalyze(database):
#     sentiment_results = {}
#     print("Start analyze on the database: ", database)
#     twiiter_count = 0
#     positive_count = 0
#     negative_count = 0
#     neutral_count = 0
#     textData = fetchText(database)
#     textSet = textData[database]
#
#     for text in textSet:
#         twiiter_count += 1
#
#         blob = TextBlob(text)
#         if blob.sentiment.polarity >= 0.1:
#             positive_count += 1
#         elif blob.sentiment.polarity <= -0.1:
#             negative_count += 1
#         else:
#             neutral_count += 1
#
#     positive_proportion = positive_count / twiiter_count
#     negative_proportion = negative_count / twiiter_count
#     neutral_proportion = neutral_count / twiiter_count
#
#     sentiment_results['positive_proportion'] = round(positive_proportion, 3)
#     sentiment_results['negative_proportion'] = round(negative_proportion, 3)
#     sentiment_results['neutral_proportion'] = round(neutral_proportion, 3)
#
#     res = []
#     res.append('sentimentRes')
#     res.append(sentiment_results)
#     return res
#     # name = database.split("_")[1]
#     # updateResult('nlp_res', {'sentimentRes': sentiment_results}, name)

for j in range(8):
    sentiment_results = {}
    print("Start analyze on the database: ", db_list[j])


    print('[===== Get Twitter Data =====]')

    twiiter_count = 0
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    textData = fetchText(db_list[j])
    textSet = textData[db_list[j]]

    for text in textSet:
        twiiter_count += 1

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

    sentiment_results['positive_proportion'] = round(positive_proportion,3)
    sentiment_results['negative_proportion'] = round(negative_proportion,3)
    sentiment_results['neutral_proportion'] = round(neutral_proportion,3)

    name =db_list[j].split("_")[1]
    updateResult('nlp_res', {'sentimentRes': sentiment_results}, name)

    print(state_list[j],' Analyze Done')

import requests

url = 'http://localhost:5000/view/nsw'
payload = {'task':{'location':'nsw', 'covid':True, 'lockdown':False}}
headers = {'content-type':'application/json'}

import json





def sendRequest(twitter):
    r = requests.post(url, data=json.dumps(twitter), headers=headers)
    print(r.json())

sendRequest(payload)
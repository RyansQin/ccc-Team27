import requests

url = 'http://localhost:5000/view/nsw'

headers = {'content-type':'application/json'}

import json


def error404test():
    url = 'http://localhost:5000/errortest'
    payload = {'test': 'errortest'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())

def error400test():
    url = 'http://localhost:5000/spider/test'
    payload = {'test': 'errortest'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())


def testView():
    url = 'http://localhost:5000/view/nsw'
    payload = {'task': {'covid': True, 'lockdown': False}}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())

def testAddTweet():
    url = 'http://localhost:5000/spider/test'
    payload = {'content': 'This is a test tweet'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())

def testFetchText():
    url = 'http://localhost:5000/cluster/text'
    payload= {'database': 'lockdown_ade'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(len(data['lockdown_ade']))
    print(data)

def testCreateDatabase():
    url = 'http://localhost:5000/spider/test3'
    r = requests.get(url, headers=headers)
    print(r.json())


testCreateDatabase()

'''

@Author: Tai Qin

This file provide some test case for the web API.
'''




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


# def testView():
#     url = 'http://localhost:5000/view'
#     payload = {'task': {'location': 'nsw', 'covid':True, 'lockdown': True, 'curve': False}}
#     r = requests.post(url, data=json.dumps(payload), headers=headers)
#     print(r.json())

def testAddTweet(database, content, docID):
    url = 'http://172.26.131.203:8000/spider'
    payload = {'database':database, 'doc': content, 'docID': docID}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.json())

def testFetchText(database):
    url = 'http://172.26.131.203:8000/cluster/text/' + database
    r = requests.get(url,  headers=headers)
    data = r.json()
    print(len(data['lockdown_ade']))
    print(data)

def testCreateDatabase(database):
    url = 'http://172.26.131.203:8000/spider'
    payload = {'dbName': database}
    r = requests.get(url, headers=headers)
    print(r.json())



def testUpdate():
    url = 'http://172.26.131.203:8000/cluster/update'
    payload = {'database': 'test', 'docID': '5ae49d113d4ac0799ae6dfa1b80074cd', 'content': {'content': 'This is the newest test'}}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()
    print(data)

# def testGetAurindata():
#     url = 'http://172.26.131.203:8000/aurin'
#     payload = {'task': ['age_distribution', 'population_density', 'tourism', 'disease'], 'location': ['nor', 'nsw', 'vic', 'can', 'ade', 'que', 'tas', 'per'], 'option': {'age1': 60, 'age2':None}}
#     r = requests.post(url, data=json.dumps(payload), headers=headers)
#     data = r.json()
#     print(data)


# @app.route('/view/<task>/<location>', methods=['GET'])
# The task can be: covidRate, curve, lockdown
def testGetView1():
    url = 'http://172.26.131.203:8000/view/lockdown/ade'
    r = requests.get(url, headers=headers)
    print((r.json()))

# @app.route('/aurin/ageDistribution/<age>', methods=['GET'])
# For the age_distribution data
# return the proportion of people that are equal or larger then <age>
def testGetAgeData():
    url = 'http://172.26.131.203:8000/aurin/ageDistribution/60'
    r = requests.get(url, headers=headers)
    print((r.json()))


# @app.route('/aurin/<task>')
# For other aurin data
# The task field can be: disease, population_density, tourism
def testGetAurinData1():
    url = 'http://172.26.131.203:8000/aurin/disease'
    r = requests.get(url, headers=headers)
    print((r.json()))



testGetView1()


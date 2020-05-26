'''
@Author; Tai Qin

This file contains the API that the client uses to access resource.

'''


from flask import Flask, jsonify, make_response
from flask import request
import couchdbBalancer as ba
import couchDbHandler as ha
import json

app = Flask(__name__)
servers = ['172.26.130.16', '172.26.131.203', '172.26.128.171']
admin = 'admin'
password = 'password'
balancer = ba.couchdbBalancer()


#- - - - - - - - -- - - - - - Common API- - - - - - - - - - - -- - - -- - - - - - - -- - - - - - - - - - - - - - - - - -

# Select a couchdb node to access resource
def selectServer():
    handlers = []
    for s in servers:
        handlers.append(ha.couchDbHandler(s, admin, password))
    couchdb= balancer.getServer(handlers)
    return couchdb

#For the given database, return all text of documents
def getText(server, dbName):
    database = server.getDatabase(dbName)
    view = database.view('_all_docs', include_docs=True)
    text = []
    for item in view:
        text.append(item['doc']['text'])
    return text

# Update specific document in the given database
def updateDoc(server, dbName, docID, content):
    database = server.getDatabase(dbName)
    doc = database.get(docID)
    for conKey in content:
        doc[conKey] = content[conKey]
    if dbName == 'analysis_res':
        doc['version'] += 1
    database.save(doc)

# Handle the bad request error
@app.errorhandler(400)
def badRequest(error):
    try:
        error = str(error)
        return make_response({error:'Bad request'}, 400)
    except:
        return make_response({'error':'Bad request'}, 400)

#Handle the not found error
@app.errorhandler(404)
def notFound(error):
    try:
        error = str(error)
        return make_response({error:'Bad request'}, 404)
    except:
        return make_response({'error':'Bad request'}, 404)








#- - - - - - - - - - - - - - - - - API for crawler- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# The http request contains a json object like {'databased: db, 'doc':{doc dictionary}, 'docID': None/ID}
# db: The database that need to be accessed
# doc: a dictionary, contains data
# docID: if the docID is None, use ramdon ID
# Retrun a json object
@app.route('/spider', methods=['POST'])
def addTwitter():
    try:
        data = json.loads(request.data)
        db = data['database']
        doc = data['doc']
        docID = data['docID']
    except:
        return badRequest('Invalid payload in request')
    try:

        couchdb = selectServer()
        database = couchdb.getDatabase(db)
    except:
        return notFound('No available couchdb nodes')
    try:
        if docID is None:
            database.save(doc)
        else:
            database[docID] = doc
        return jsonify({'database':db, 'Status': "completed"})
    except:
        return notFound('Fail to add new documents')



# create a new database in the couchdb, the payload is like {'dbName': <dbName>}
@app.route('/spider/dbSet', methods=['POST'])
def createDB():
    try:
        data = json.loads(request.data)
        dbName = data['dbName']
    except:
        return badRequest('Invalid payload in request')

    try:
        couchdb = selectServer()
        couchdb.couchdbServer.create(dbName)
        return jsonify({'database': dbName, 'Status': "completed"})
    except:
        return notFound('Unable to create new database')


#- - - - - - - - - - - - - - - API for Twitter analysis- - - - - - -  -  -  - - - - - - - - - - - - - - - - - - - - - - - - -- - -

# Return the total number of documents for the given database
def getTotalRows(database):
    rows = database.view('_all_docs')
    sum = 0
    for item in rows:
        sum += 1
    return sum

# Calculate the proportion of tweets that related to covid19 in specific location
def calCovidRate(server, location):
    dbName = 'tweet_' + location
    print(dbName)
    database = server.getDatabase(dbName)
    view = database.view('covid/covid')
    rate = {}
    res = 0
    for item in view:
        res += item.value
    totalNumber = getTotalRows(database)
    rate['total'] = totalNumber
    rate['covid'] = res
    return rate

# # For the given location, return the most popular activities during lockdown
# def getCluserRes(server, location):
#     dbName = 'nlp_res'
#     docID = location
#     database = server.getDatabase(dbName)
#     doc = database.get(docID)
#     return doc['clusterRes']
#
# def getSentimentRes(server, location):
#     dbName = 'nlp_res'
#     docID = location
#     database = server.getDatabase(dbName)
#     doc = database.get(docID)
#     return doc['sentimentRes']

# Return the number of tweets that related to COVID-19 by date
def getCurve(server, location):
    dbName = 'tweet_'+location
    database = server.getDatabase(dbName)
    view = database.view('covid/covid_time', group=True)
    res = []
    covid = []
    date = []
    for item in view:
        date.append(item.key)
        covid.append(item.value)
    res.append(date)
    res.append(covid)
    return res

# The task can be: covidRate, curve, lockdown
# location can be: nsw, ade, vic, que, nor, per, tas, can
# The client use this API to get the analysis result of tweets
# In order to reduce the response time, it will not return the latest result
@app.route('/view/<task>/<location>', methods=['GET'])
def getView1(task, location):
    try:
        couchdb = selectServer()
        database = couchdb.getDatabase('analysis_res')
        if task == 'lockdown':
            return jsonify({'lockdownRank':database[location]['lockdownRank']})
        else:
            return jsonify({task: database[location][task]})
    except:
        notFound('Unable to get the required view')


# The task can be: covidRate, curve, lockdown
# location can be: nsw, ade, vic, que, nor, per, tas, can
# This API is to get the latest analysis result
# The twiiter analysis module use it to update the result periodically
@app.route('/view/result/<task>/<location>', methods=['GET'])
def getViewResult(task, location):
    couchdb = selectServer()
    try:
        resp = {}
        if task == 'covidRate':
            covidRate = calCovidRate(couchdb, location)
            resp['covidRate'] = covidRate
        else:
            curve = getCurve(couchdb, location)
            resp['curve'] = curve
        return jsonify(resp)
    except:
        return notFound('Unable to get the latest view')


@app.route('/analysis/result', methods=['POST'])
def updateResult():
    try:
        data = json.loads(request.data)
        doc = data['content']
        dbName = data['database']
        docID = data['docID']
    except:
        badRequest('Invalid payload in the request')
    try:
        server = selectServer()
        updateDoc(server, dbName, docID, doc)
        return jsonify({'database': dbName, 'status':'completed'})
    except:
        notFound('Unable to update result')


# This API is designed for the cluster/sentiment analysis module
# For the given database, it will return the content in text filed of all documents
# Retrun a json object
@app.route('/analysis/text/<dbName>', methods=['GET'])
def getAllText(dbName):

    try:
        server = selectServer()
        resp = {}
        resp[dbName] = getText(server, dbName)
        return jsonify(resp)
    except:
        return notFound('Unable to get all text')

# The http request contains a json object like {task:{task dictionary}}
# In the task, there are following keys:
# location: the location that we want to explore, including nsw, ade, vic, nor, per, tas, que, can
# covid: True/False, indicate whether it needs the proportion of tweets that related to covid
# lockdown: True/False, indicate whether it needs the most popular activities during lockdown
# Curve: True/False, indicate whether it needs to calculate the curve
# Retrun a json object
# @app.route('/view', methods=['POST'])
# def getView():
#     print('start')
#     couchdb = selectServer()
#     resp = {}
#     task = json.loads(request.data)['task']
#     covidRate = None
#     lockdown = None
#     curve = None
#     location = task['location']
#     if task['covid'] is True:
#         covidRate = calCovidRate(couchdb, location)
#     if task['lockdown'] is True:
#         lockdown = [['clusterRes', getCluserRes(couchdb, location)], ['sentimentRes', getSentimentRes(couchdb, location)]]
#     if task['curve'] is True:
#         curve = getCurve(couchdb, location)
#     resp['covidRate'] = covidRate
#     resp['lockdownRank'] = lockdown
#     resp['curve'] = curve
#     return jsonify(resp)




#- - - - - - - - - - - - - - - - - - - - - API for aurin- - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - #


#For the given location and age, return the proportion of people that are not less than the given age
def getAgePercent(server, loc, mapLocation, age):
    database = server.getDatabase('aurin_data')
    doc = database['age_distribution']
    res = []
    for l in loc:
        ans = 0
        locRes = []
        locRes.append(l)
        data = doc[mapLocation[l]]
        keySet = data[1]
        valueSet = data[2]
        for i in range(1, len(keySet)):
            tempList = keySet[i].split('_')

            if int(tempList[1]) >= int(age):
                ans += valueSet[i]

        locRes.append(ans)
        res.append(locRes)
    return res



# For the age_distribution data
# return the proportion of people that are equal or larger then <age>
@app.route('/aurin/ageDistribution/<age>', methods=['GET'])
def getAgeData(age):
    mapLocation = {}
    mapLocation['can'] = 'act'
    mapLocation['nor'] = 'nt'
    mapLocation['nsw'] = 'nsw'
    mapLocation['per'] = 'wa'
    mapLocation['ade'] = 'sa'
    mapLocation['tas'] = 'tas'
    mapLocation['vic'] = 'vic'
    mapLocation['que'] = 'qld'
    location = ['nor', 'nsw', 'vic', 'can', 'ade', 'que', 'tas', 'per']
    try:
        server = selectServer()
        resp = []


        resp.append(['age_distribution', getAgePercent(server, location, mapLocation, age)])
        return jsonify({'result': resp})
    except:
        notFound('Unable to find the required age data')


# For other aurin data
# The task field can be: disease, population_density, tourism
@app.route('/aurin/<task>', methods=['GET'])
def getAurinData1(task):
    mapLocation = {}
    mapLocation['can'] = 'act'
    mapLocation['nor'] = 'nt'
    mapLocation['nsw'] = 'nsw'
    mapLocation['per'] = 'wa'
    mapLocation['ade'] = 'sa'
    mapLocation['tas'] = 'tas'
    mapLocation['vic'] = 'vic'
    mapLocation['que'] = 'qld'
    locLst = ['nor', 'nsw', 'vic', 'can', 'ade', 'que', 'tas', 'per']
    try:
        server = selectServer()
        database = server.getDatabase('aurin_data')
    except:
        notFound('No couchdb node available')
    try:
        resp = []
        doc = database.get(task)
        temp = []
        temp.append(task)
        for loc in locLst:
            temp1 = []
            temp1.append(loc)
            if task == 'disease':
                temp1.append(doc[loc])
            else:
                temp1.append(doc[mapLocation[loc]])
            temp.append(temp1)
        resp.append(temp)
        return jsonify({'result': resp})
    except:
        notFound('Unable to get the required AURIN data')










if __name__ == '__main__':
    app.run(host='0.0.0.0')

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
# Select a server to deal with the request
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


@app.errorhandler(400)
def badRequest():
    return make_response({'error':'Bad request'}, 400)

@app.errorhandler(404)
def notFound():

    return make_response({'error': 'Not found'}, 404)








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
        return badRequest()
    try:

        couchdb = selectServer()
        database = couchdb.getDatabase(db)
    except:
        return notFound()
    try:
        if docID is None:
            database.save(doc)
        else:
            database[docID] = doc
        return jsonify({'database':db, 'Status': "completed"})
    except:
        return badRequest()



# create a new database in the couchdb
@app.route('/spider/dbSet', methods=['POST'])
def createDB():
    try:
        data = json.loads(request.data)
        dbName = data['dbName']
    except:
        return badRequest()

    try:
        couchdb = selectServer()
        couchdb.couchdbServer.create(dbName)
        return jsonify({'database': dbName, 'Status': "completed"})
    except:
        return notFound()


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

# For the given location, return the most popular activities during lockdown
def getCluserRes(server, location):
    dbName = 'nlp_res'
    docID = location
    database = server.getDatabase(dbName)
    doc = database.get(docID)
    return doc['clusterRes']

def getSentimentRes(server, location):
    dbName = 'nlp_res'
    docID = location
    database = server.getDatabase(dbName)
    doc = database.get(docID)
    return doc['sentimentRes']

#
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
        notFound()

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
        return notFound()



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



#For the age_distribution data
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
        notFound()


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
        notFound()
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
        notFound()








# Deal with the request of Aurin data
# The http request contains following keys
# task: a list that the data we want to access, ['age_distribution', 'population_density', 'tourism', 'disease']
# location: the location we want to search, ['can', 'nsw', 'vic', 'ade', 'que', 'per', 'nor', 'tas']
# option: used by the age_distribution, if it is not in the task field, option = Mone, else contain following keys
# option: {'age1': age1, 'age2': age2}
# age1, age2: the interval of age that you want to access
# if age1 is None, return proportion of people that is younger than age2
# if age2 is None, return proportion of people that is older than age1
# if both of them are not None, return proportion of people between age1 and age2
# For each task, returns a dictionary that contains data of the given location
@app.route('/aurin', methods=['POST'])
def getAurinData():
    mapLocation = {}
    mapLocation['can'] = 'act'
    mapLocation['nor'] = 'nt'
    mapLocation['nsw'] = 'nsw'
    mapLocation['per'] = 'wa'
    mapLocation['ade'] = 'sa'
    mapLocation['tas'] = 'tas'
    mapLocation['vic'] = 'vic'
    mapLocation['que'] = 'qld'
    try:
        data = json.loads(request.data)
        task = data['task']
        location = data['location']
        option = data['option']
    except:
        return badRequest()

    try:
        server = selectServer()
        database = server.getDatabase('aurin_data')
        resp = []
        for t in task:
            if t=='age_distribution':
                resp.append([t, getAgePercent(server, location, mapLocation, option['age1'], option['age2'])])


            else:
                doc = database.get(t)
                temp = []
                temp.append(t)
                for loc in location:
                    temp1 = []
                    temp1.append(loc)
                    if t == 'disease':
                        temp1.append(doc[loc])
                    else:
                        temp1.append(doc[mapLocation[loc]])
                    temp.append(temp1)

                resp.append(temp)
        return jsonify({'result':resp})
    except:
        return notFound()



#- - - - - - - - - - - - - -- - - - - - - -API for machine learning- - - - - - - - - - - - - - - - - - - - - - - - - - -

# The http request contains a json object like {database:database}
# In the task, there are following keys:
# database: indicates which database we want to access
# Retrun a json object
@app.route('/cluster/text/<dbName>', methods=['GET'])
def getAllText(dbName):

    try:
        server = selectServer()
        resp = {}
        resp[dbName] = getText(server, dbName)
        return jsonify(resp)
    except:
        return notFound()


# Update the result on the couchdb
# The data field of the http request contains a dictionary. including the following key
# database: specify the database that needs to be updated
# docID: specify the document that needs to be updated
# content: a dictionary, specify the key and value that need to be updated
@app.route('/cluster/update', methods=['POST'])
def updateResult():
    try:
        data = json.loads(request.data)
        dbName = data['database']
        docID = data['docID']
        content = data['content']
    except:
        return badRequest('Invalid update request')

    try:
        server = selectServer()
        updateDoc(server, dbName, docID, content)
    except:
        return notFound('Database is unavailable or not exist, fail to update the document')
    return jsonify({'status': 'complete update'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')

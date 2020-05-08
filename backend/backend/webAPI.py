from flask import Flask, jsonify, make_response
from flask import request
import backend.couchdb.couchdbBalancer as ba
import backend.couchdb.couchDbHandler as ha
import requests
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

@app.errorhandler(400)
def badRequest(errorMessage):
    return make_response(jsonify({errorMessage:'Bad request'}), 400)

@app.errorhandler(404)
def notFound(errorMessage):
    return make_response(jsonify({errorMessage: 'Not found'}), 404)






#- - - - - - - - - - - - - - - - - API for crawler- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# The http request contains a json object like {doc dictionary}}
# doc: a dictionary, contains data
# Retrun a json object
@app.route('/spider/<db', methods=['POST'])
def addTwitter(db):
    try:
        doc = json.loads(request.data)
    except:
        return badRequest('Not a valid Json document')
    try:

        couchdb = selectServer()
        database = couchdb.getDatabase(db)
    except:
        return notFound('Required database not found')
    try:
        database.save(doc)
        return jsonify({'database':db, 'Status': "completed"})
    except:
        return badRequest('Fail to add a new document')



# create a new database in the couchdb
@app.route('/spider/<db>', methods=['GET'])
def createDB(db):
    try:
        couchdb = selectServer()
        couchdb.create(db)
        return jsonify({'database': db, 'Status': "completed"})
    except:
        return badRequest('Fail to create the database')


#- - - - - - - - - - - - - - - API for demo - - - - - - -  -  -  - - - - - - - - - - - - - - - - - - - - - - - - -- - -

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
def getLockdownRank(server, location):
    return None



# The http request contains a json object like {task:{task dictionary}}
# In the task, there are following keys:
# covid: True/False, indicate whether it needs the proportion of tweets that related to covid
# lockdown: True/False, indicate whether it needs the most popular activities during lockdown
# Retrun a json object
@app.route('/view/<location>', methods=['POST'])
def getView(location):
    print('start')
    couchdb = selectServer()
    resp = {}
    task = json.loads(request.data)['task']
    covidRate = None
    lockdownRank = None
    if task['covid'] is True:
        covidRate = calCovidRate(couchdb, location)
    if task['lockdown'] is True:
        lockdownRank = getLockdownRank(couchdb, location)
    resp['covidRate'] = covidRate
    resp['lockdownRank'] = lockdownRank
    return jsonify(resp)


#- - - - - - - - - - - - - - - - - - - - - API for aurin- - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - -




#- - - - - - - - - - - - - -- - - - - - - -API for machine learning- - - - - - - - - - - - - - - - - - - - - - - - - - -

# The http request contains a json object like {database:{database dictionary}}
# In the task, there are following keys:
# database: indicates which database we want to access
# Retrun a json object
@app.route('/cluster/text', methods=['POST'])
def getAllText():
    try:
        data = json.loads(request.data)
        database = []
        for db in data['database']:
            database.append(db)
    except:
        return badRequest('Invalid request')

    try:
        server = selectServer()
        resp = {}
        for db in database:
            resp[db] = getText(server, db)
        return jsonify(resp)
    except:
        return notFound('Some databases noy found')


@app.route('/cluster/result', methods=['POST'])
def updateResult():
    return None



if __name__ == '__main__':
    app.run()
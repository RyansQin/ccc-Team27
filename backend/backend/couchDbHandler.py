'''

@Author: Tai Qin

This file is a handler for CouchDB, it uses the python couchdb library and provide some function our system needs
'''

import couchdb

'''
@Parameter: address, the ip address of CouchDB node
@Parameter: state, True/False, indicates whether the node is available
@Parameter: database, a list that contain all databases in this node
@Parameter: couchdbServer, an object to access the CouchDB node.
@Method: updateDatabase, update the self.database
@Method: getDatabase, return specific database object in this node
'''
class couchDbHandler:
    couchdbServer = None
    database = []
    stats = True
    address = None

    # For accessing a CouchDB database, the ip address, port, username and password are required

    def __init__(self, address, user, password, url='http://{admin}:{password}@{address}:{port}', port=5984):
        self.address = address
        try:
            self.couchdbServer = couchdb.Server(url.format(admin=user, password=password, address=address, port=port))
            self.updateDatabase()
        except:
            self.stats=False



    def updateDatabase(self):
        for db in self.couchdbServer:
            if db not in self.database:
                self.database.append(db)
        for db in self.database:
            if db not in self.database:
                self.database.remove(db)

    def getDatabase(self, db):
        self.updateDatabase()
        if db in self.database:
            return self.couchdbServer[db]




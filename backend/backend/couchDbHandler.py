import couchdb



class couchDbHandler:
    couchdbServer = None
    database = []
    stats = True
    address = None


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

    def getDatabase(self, db):
        self.updateDatabase()
        if db in self.database:
            return self.couchdbServer[db]
        return "Invalid database request"



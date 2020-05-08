import couchdb
import couchDbHandler


class couchdbBalancer:
    serversFreq = None
    admin =None
    password = None
    serversStats = None

    def __init__(self):
        self.serversFreq = {'172.26.130.16': 0, '172.26.131.203': 0, '172.26.128.171': 0}
        self.admin = 'admin'
        self.serversStats = {'172.26.130.16':True, '172.26.131.203':True, '172.26.128.171': True}
    
    def getServer(self, servers):
        self.updateState(servers)
        returnServer = servers[0]
        minFreq = self.serversFreq[returnServer.address]
        for s in servers:
            if self.serversFreq[s.address] < minFreq:
                minFreq = self.serversFreq[s.address]
                returnServer = s
        self.serversFreq[returnServer.address] += 1
        return returnServer
            
    
    def updateState(self, servers):
        for s in servers:
            if self.serversStats is True and s.stats is False:
                self.serversStats[s.address] = False
            elif self.serversStats is False and s.stats is True:
                self.serversStats[s.address] = True
                self.serversFreq = {'172.26.130.16': 0, '172.26.131.203': 0, '172.26.128.171': 0}
    
    
        






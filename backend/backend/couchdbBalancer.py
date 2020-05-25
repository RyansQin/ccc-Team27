'''

@Author: Tai Qin

This file is a load balancer for CouchDB cluster, it is based on the polling strategy
'''





'''
@Parameter: serversFreq, a dictionary stores how many times each node has been accessed
@Parameter: serversStats, a dictionary stores whether these nodes are available
@Method: getServer, return a couchDB handler based on the polling strategy
@Method: updateState, check whether the couchdb node is available
'''
class couchdbBalancer:
    serversFreq = None
    serversStats = None

    def __init__(self):
        self.serversFreq = {'172.26.130.16': 0, '172.26.131.203': 0, '172.26.128.171': 0}

        self.serversStats = {'172.26.130.16':True, '172.26.131.203':True, '172.26.128.171': True}


    '''
    Select the CouchDB node that have least accessing times
    @Parameter: servers, a list that contains serveral CouchDB handler
    '''
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

    '''
    Update the state of couchdb nodes. If there are nodes become available from failure, the serverFreq will be reset
    @Parameter: servers, a list that contains serveral CouchDB handler
    '''
    def updateState(self, servers):
        for s in servers:
            if self.serversStats is True and s.stats is False:
                self.serversStats[s.address] = False
            elif self.serversStats is False and s.stats is True:
                self.serversStats[s.address] = True
                self.serversFreq = {'172.26.130.16': 0, '172.26.131.203': 0, '172.26.128.171': 0}
    
    
        






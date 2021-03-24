'''
This will listen to the incoming transfers to temporay deposit addresses
1. using listeners on the main source where the transactions are stored or listening to a message queue where txns are sent through is 
   preferred but don't know how to set up locally
2. making a call to transactions and checking if it changed from the previous stored state. - for test project purposes

'''
import logging
import functools
import requests
import simplejson as json

HOUSE_ACCOUNT = 'houseAccount'
URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'


class DepositListener:
    def __init__(self, refreshFrequency):
        self.refreshFrequency = refreshFrequency
        reactor.callInThread(self.checkForNewTransactions, reactor)

    def transferToHouseAccount(self, reactor, newTransactions):
        print('transferToHouse')
        for txn in newTransactions:
            requestBody = {
                'fromAddress': txn['fromAddress'],
                'toAddress': HOUSE_ACCOUNT,
                'amount' : txn['amount']
            }
            print(f'RequestBody is {requestBody}')
            requests.post(URL, data=requestBody)

    def getNewTransactions(self, reactor, currTxns):
        print('getNewTransactions')
        '''
        get new txns with tempDest as dest and not processed yet, maintain table of processed tempDest
        set self.currTxns to the latest set
        '''
        newTxns = [{
            'fromAddress': 'Alice',
            'toAddress': 'tempDest1',
            'amount': '50',
        }]
        self.currentTransactions = currTxns
        reactor.callFromThread(self.transferToHouseAccount, reactor, newTxns)

    def checkForNewTransactions(self, reactor):
        currTxns = self.getCurrentTransactions(reactor)
        l = len(currTxns)
        print(f'len of curr txns{l}')
        if len(currTxns) >= len(self.currentTransactions):
            reactor.callFromThread(self.getNewTransactions, reactor, currTxns)

        reactor.callLater(5, self.checkForNewTransactions, reactor)

    def getCurrentTransactions(self, reactor):
        #make call to JobCoin API to get txns
        currentTransactions = None
        resp = requests.get(URL)
        if resp.status_code == 200:
            currentTransactions = resp.json()
        else:
            logging.exception('Error getting txns')

        return currentTransactions

    def initialize(self, reactor):
        currTxns = self.getCurrentTransactions(reactor)
        self.currentTransactions = currTxns
        print(currTxns)
        self.initialized = True

    def run(self, reactor):
        if not self.initialized:
            return
        reactor.callLater(5, self.run, reactor)

    def start(self, reactor, runReactor=True):
        self.initialize(reactor)
        if runReactor:
            reactor.run()

if __name__ == '__main__':
        from twisted.internet import reactor
        depositListener = DepositListener(5)
        depositListener.start(reactor)

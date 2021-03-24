
import requests
import logging
import simplejson as json
import functools

URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'


class Mixer:
    def __init__(self, updateFrequency=5):
        self.updateFrequency = updateFrequency
        self.userSourceAddressMap = self.getUserSourceAddressMap()
        self.tempDestToOrigUserMap = self.tempDestToOrigUserMap()
        self.houseAccountAddress = 'houseAccount'
        reactor.callInThread(self.checkForUpdates, reactor)

    def getUserSourceAddressMap(self):
        '''
        reads from where this info is stored by requestProcessor
        dummying for test purposes
        '''
        return {
            'Alice': ['Alice1', 'Alice2', 'Alice3'],
            'Bob': ['Bob1', 'Bob2', 'Bob3']
        }

    def tempDestToOrigUserMap(self):
        '''
        reads from where this info is stored by requestProcessor
        dummying for test purposes
        '''
        return {
            'tempDest1': 'Alice',
            'tempDest2': 'Bob'
        }



    def transferToOriginalAccounts(self, reactor, currTxns):
        '''
        get sourceUser and corr sourceAddress
        amount  /= number of sourceaddress
        use jobcoin api to send money from house account to source address
        '''
        print('transferring to orig accounts')
        for txn in currTxns:
            tempDest = txn['fromAddress']
            origUser = self.tempDestToOrigUserMap.get(tempDest, None)
            print(f'Original User is {origUser}')
            if not origUser:
                logging.info('original User not found')
                return
            sourceAddresses = self.userSourceAddressMap.get(origUser, None)
            print(f'Source Addreses: {sourceAddresses}')
            if not sourceAddresses:
                logging.info('Original User not found')
                return

            amount = int(txn['amount'])
            splits = amount / len(sourceAddresses)

            for sa in sourceAddresses:
                reqBody = {
                    'fromAddress': self.houseAccountAddress,
                    'toAddress': sa,
                    'amount': str(splits)
                }
                print(f'Sending requests {reqBody}')
                requests.post(URL, data=reqBody)

    def getNewTransactions(self, reactor, currTxns):
        print('getNewTransactions')
        '''
        get new txns with houseAccount as dest and not processed yet, maintain table of processed houseAccount
        set self.currTxns to the latest set
        dummying for test
        '''
        newTxns = [{
            'fromAddress': 'tempDest1',
            'toAddress': 'houseAccount',
            'amount': '50',
        }]
        self.currentTransactions = currTxns
        reactor.callFromThread(self.transferToOriginalAccounts, reactor, newTxns)

    def checkForUpdates(self, reactor):
        '''
        query JobCoin API for currTxns and compare with inMem txns
        '''
        currTxns = self.getCurrentTransactions(reactor)
        l = len(currTxns)
        print(f'Length of current txns is {l}')

        if len(currTxns) >= len(self.currentTransactions): ##>= for testing purposes, should be >
            reactor.callFromThread(self.getNewTransactions, reactor, currTxns)
        reactor.callLater(self.updateFrequency, self.checkForUpdates, reactor)

    def getCurrentTransactions(self, reactor):
        '''
        make call to JobCoin API to get txns
        '''
        currentTransactions = None
        resp = requests.get(URL)
        if resp.status_code == 200:
            currentTransactions = resp.json()
        else:
            logging.exception('Error getting txns')

        return currentTransactions

    def initialize(self, reactor):
        '''
        get current transactions
        '''
        currTxns = self.getCurrentTransactions(reactor)
        self.currentTransactions = currTxns
        self.initialized = True

    def run(self, reactor):
        if not self.initialized:
            return
        #reactor.callFromThread(self.checkForUpdates, reactor)
        reactor.callLater(self.updateFrequency, self.run, reactor)

    def start(self, reactor, runReactor=True):
        self.initialize(reactor)
        if runReactor:
            reactor.run()

if __name__ ==  '__main__':
    from twisted.internet import reactor
    m = Mixer()
    m.start(reactor)



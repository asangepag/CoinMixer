'''
This will listen to the incoming transfer to deposit address 
1. using listeners on the main source where the transactions are stored - Preferred but don't know how to set up locally
2. making a call to transactions and checking if it changed from the previous stored state. - for test project purposes

'''
import logging
import functools

HOUSE_ACCOUNT = 'houseAccount'
URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'

class DepositListener:
  def __init__(self):
    self.currentTransactions = functools.partial(self.getCurrentTransactions)
    reactor.callInThread(self.checkForNewTransactions, reactor)
  
  
  def transferToHouseAccount(self, newTransactions, reactor):
    for txn in newTransactions:
      requestBody = {
        'fromAddress' : txn['fromAddress']
        'toAddress' : HOUSE_ACCOUNT'
        'amount' " txn['amount']
      }
      requests.post(URL, body = requestBody)
  
  def getNewTransactions(self, currTxns, reactor):
    ##get new txns with tempDest as dest and not processes yet, maintain table of processed tempDest'
    newtxns =  {
      'fromAddress' : 'Alice'
      'toAddress' : 'tempDest1'
      'amount' :'50'
    }
    reactor.callFromThread(self.transferToHouseAccount, newTxns, reactor)
  
  def checkForNewTransactions(self, reactor):
    currTxns = self.getCurrentTransactions()
    if len(currTxns) > self.currentTransactions:
      reactor.callFromThread(self.getNewTransactions, currTxns, reactor)
  
  def getCurrentTransactions(self, reactor):
    '''
    make call to JobCoin API to get txns
    '''
    
    resp = requests.get(URL)
    if resp.status_code == 200:
      resp = json.loads(resp.transactions)
    else:
      logging.exception('Error getting txns')
    
  def run(self, reactor):
    if not self.initialized:
      return
    reactor.callAfter(5, self.run, reactor)
    
  def start(self, reactor, runReactor=True):
    if runReactor:
      self.run()
  

  def main():
    from twisted import reactor
    depositListener = DepositListener()
    depositListener.start()

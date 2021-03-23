from  twisted.internet.task import LoopingCall
import  requests
import  logging
from  simplejson import json

URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'


class Mixer:
  def __init__(self, updateFrequency=5):
    self.updateFrequency = updateFrequency
    self.initialize()
    self.userSourceAddressMap = self.getUserSourceAddressMap()
    self.tempDestToOrigUserMap = self.tempDestToOrigUserMap()
    self.houseAccountAddress = 'houseAccount'
    
  def getUserSourceAddressMap(self):
    ''' reads from where this info is stored by requestProcessor
        dummying for test
    '''
    return {
      'Alice' : ['Alice1', 'Alice2', 'Alice3'],
      'Bob' : ['Bob1', 'Bob2', 'Bob3']
    }
  
  def tempDestToOrigUserMap(self):
    ''' reads from where this info is stored by requestProcessor
        dummying for test
    '''
    return {
      'tempDest1' : 'Alice'
      'tempDest2' : 'Bob'
    }
 
  
  def onUpdate(self, reactor):
    reactor.callFromThread(self.processUpdate, reactor)
    
  
  def processUpdate(self, currTxns, reactor):
    for txn in currTxns:
      tempDest = txn.fromAddress
      origUser = self.tempDestToOrigUserMap.get(tempDest, None)
      if not origUser:
        logging.exceptions('original User not found'
      sourceAddresses = self.sourceAddressMap.get(origUser, None)
      if not sourceAddresses:
        logging.exception('Original User not found')
      
      amount = int(txn.amount)
      splits = amount/len(sourceAddresses)
      for sa in sourceAddresses:
        reqBody = {
          'fromAddress': self.houseAccountAddress,
          'toAddress' : sa
          'amount' : str(splits)
        }
        requests.post(URL, body=reqBody)
      
       
    
  def checkForUpdates(self, reactor):
    '''
    get sourceUser and corr sourceAddress
    amount /= number of sourceaddress
    use jobcoin api to send money from house_acccout to source address
    '''
    currTxns = self.getCurrentTransactions
    #for txn in currTxns:
      #if txn['new'] == True:
        #reactor.callFromThread(self.processUpdate, currTxns, reactor)
        
    if len(currTxns) > len(self.currentTransactions):
      reactor.callFromThread(self.processUpdate, currTxns, reactor)
   
  
  def getCurrentTransactions(self, reactor):
    resp = requests.get(URL)
    if resp.status_code == 200:
      resp = json.loads(resp)
      self.currentTransactions = resp.transactions
    else:
      logging.exception('Failed to get current transactions')
  
  def initialize(self, reactor):
    ''' get current txns'''
    self.getCurrentTransactions(reactor)
    self.initialized = True
    
  
  def run(self, reactor):
    if not self.initialized:
      return 
    self.checkUpdates(reactor)
    reactor.callLater(self.updateFrequency, functools.partial(self.run, reactor)
    
  
  def start(self, reactor, runReactor=True):
    self.initialize()
    if runReactor:
      self.run()
                      
      
      
      
def main():
  m = Mixer()
  from twisted import reactor
  m.start()
                        
  

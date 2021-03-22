from twisted.internet.task import LoopingCall

class Mixer:
  def __init__(self):
    self.currentTransactions = self.getCurrentTransactions
  
  def onUpdate(self, reactor):
    reactor.callFromThread(self.processUpdate, reactor)
    
    
  def processUpdate(self, reactor):
    '''
    get sourceUser and corr sourceAddress
    amount /= number of sourceaddress
    use jobcoin api to send money from house_acccout to source address
    '''
    pass
  
  def initialize(self, reactor):
    ''' get current txns'''
    pass
  
  def run(self, reactor):
    if not self.initialized:
      return 
    reactor.callLater(self.refreshFrequency, functools.partial(self.start, reactor)
    
  
  def start(self, reactor, runReactor=True):
    self.initialize()
    if runReactor:
      self.run()
                      
      
      
      
def main():
  m = Mixer()
  from twisted import reactor
  m.start()
                        
  

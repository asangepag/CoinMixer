

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
 
def main():
  m = Mixer()
  from twisted import reactor
  

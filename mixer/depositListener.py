'''
This will listen to the incoming transfer to deposit address 
1. using listeners on the main source where the transactions are stored - Preferred but don't know how to set up locally
2. making a call to transactions and checking if it changed from the previous stored state. - for test project purposes

'''

HOUSE_ACCOUNT = 'houseAccount'

class DepositListener:
  def __init__(self):
    self.currentTransactions = self.getCurrentTransactions
  
  
  def transferToHouseAccount(amount):
    pass
  
  def getCurrentTransactions():
    '''
    make call to JobCoin API to get txns
    '''
    pass
  

  def main():
    from twisted import reactor
    reactor.run()

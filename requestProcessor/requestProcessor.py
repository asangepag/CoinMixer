import logging
import datetime
from  flask import Flask
from  flask import request
from  collections import defaultdict

app = Flask(__name__)

JOBCOIN_URL = 'http://jobcoin.gemini.com/'

class RequestProcessor:
  def __init__(self):
    self.addresses = []
    self.userNameAddressMap = defaultdict(list)
    
  
  @app.route('/sendAddresses/<user>/<addresses>')
  def processRequest(self, user, addresses):
    '''
    @param user: string, original user
    @param addresses: list of addresses for the user
    returns address to deposit amount
    '''
    self.userNameAddressMap[user].extend(addresses)
    tempDestAdrress = self.getTempDestAddress()
    return {'tempDestAddress' : tempDestAddress}
    
    
 
  @app.route('/processDeposit')
  def sendCoinsToDestAddress(self, user, destAddress, amount):
    '''
    @param user: string, original user
    @param amount: float ,amount user wishes to deposit
    returns None
    
    
    '''
    url = 'http://jobcoin.gemini.com/todo_my_instance/api/transactions'
    Request.post(url)
    
 

if __name__ == '__main__':
  app.run(debug=True)
  
  
  

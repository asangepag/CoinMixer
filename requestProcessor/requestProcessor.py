import logging
import datetime
from flask import Flask
from flask import request
from collections import defaultdict
import requests
import random

app = Flask(__name__)


class RequestProcessor:
    def __init__(self):
        self.addresses = []
        self.userNameAddressMap = defaultdict(list)
        self.userNameAmountMap = {}
        self.tempDestOrigUserMap = {}

    def getTempDestinationAddress(self):
        r = random.randint()
        tempDestAddress = 'tempDest' + str(r)
        return tempDestAddress

    @app.route('/anonymize/<user>/<sourceAddresses>', methods=['GET'])
    def anonymize(self, user, sourceAddresses):
        '''
        @param user: string, original user
        @param sourceAddresses: list of unused addresses user has
        returns address to deposit amount
        '''
        self.userNameAddressMap[user].extend(sourceAddresses)
        tempDestAddress = self.getTempDestAddress()
        return {
            'sourceUser' : user,
            'tempDestAddress': tempDestAddress}

    @app.route('/processDeposit', methods=['POST'])
    def sendCoinsToDestAddress(self, user, destAddress, amount):
        '''
        @param user: string, original user
        @param destAddress: string, temporary Destination address
        @param amount: float ,amount user wishes to deposit
        returns None
        '''
        self.userNameAmountMap[user] = amount ###TODO: save to db for use by mixer
        self.tempDestOrigUserMap[destAddress] = user
        url = 'http://jobcoin.gemini.com/todo_my_instance/api/transactions'
        requestBody = {
            'fromAddress' : user,
            'toAddress' : destAddress,
            'amount' : str(amount)
        }
        requests.post(url, data=requestBody)


if __name__ == '__main__':
    app.run(debug=True)
  
  
  

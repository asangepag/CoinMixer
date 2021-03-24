
from flask import Flask
from flask_classful import FlaskView, route
from collections import defaultdict
import requests
import random
import logging
import datetime

app = Flask(__name__)


class RequestProcessor(FlaskView):

    def __init__(self):
        self.addresses = []
        self.userNameAddressMap = defaultdict(list)
        self.userNameAmountMap = {}
        self.URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'
        #self.app = Flask(name)


    def getTempDestinationAddress(self):
        r = random.randint(1, 1000) ### fix for real usecases, test range
        tempDestAddress = 'tempDest' + str(r)
        return tempDestAddress

    @route('/anonymize/<origAddress>/<sourceAddresses>', methods=['GET'])
    def anonymize(self, origAddress, sourceAddresses):
        '''
        @param origAddress: string, original user
        @param sourceAddresses: list of unused addresses user has
        returns address to deposit amount
        '''
        sourceAddresses = sourceAddresses.split(',')
        self.userNameAddressMap[origAddress].extend(sourceAddresses)
        print(self.userNameAddressMap)
        tempDestAddress = self.getTempDestinationAddress()
        return {
            'origAddress': origAddress,
            'tempDestAddress': tempDestAddress
        }


    @route('/sendCoinsToDestAddress', methods=['POST'])
    def sendCoinsToDestAddress(self):
        '''
        @param user: string, original user
        @param destinationAddress: string, temporary Destination address
        @param amount: float ,amount user wishes to deposit
        returns None
        '''

        from flask import request
        user = request.form['user']
        destAddress = request.form['destinationAddress']
        amount = request.form['amount']
        self.userNameAmountMap[user] = amount  ###TODO: save to db for use by mixer
        requestBody = {
            'fromAddress' : user,
            'toAddress' : destAddress,
            'amount' : str(amount),
        }
        #print(requestBody, self.URL)
        resp = requests.post(self.URL, data=requestBody)
        return {'status': resp.status_code}

    '''
    def run(self):
        self.register(self.app, route_base='/')
        self.app.run(debug=True)
    '''

RequestProcessor.register(app, route_base='/')

if __name__ == '__main__':
  app.run(debug=True)

'''
def main():
    reqProcessor = RequestProcessor('req')
    reqProcessor.run()
'''



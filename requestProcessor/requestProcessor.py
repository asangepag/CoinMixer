
'''
This part with interface with the user to get the source addresess + send them to a temp account
Would use tornado in real world example to handle request volume
'''

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
        '''
        will return an address like tempDest1, tempDest2 etc
        '''
        r = random.randomint(1, 1000) ### fix for real usecases, test range
        tempDestAddress = 'tempDest' + str(r)
        return tempDestAddress

    @route('/anonymize/<origAddress>/<sourceAddresses>', methods=['GET'])
    def anonymize(self, origAddress, sourceAddresses):
        '''
        @param origAddress: string, original user
        @param sourceAddresses: list of unused addresses user has
        returns address to deposit amount
        '''
        self.userNameAddressMap[origAddress].extend(sourceAddresses)
        tempDestAddress = self.getTempDestinationAddress()
        return {
            'origAddress': origAddress,
            'tempDestAddress': tempDestAddress
        }


    @route('/sendCoinsToDestAddress', methods=['POST'])
    def sendCoinsToDestAddress(self, user, destAddress, amount):
        '''
        @param user: string, original user
        @param destAddress: string, temporary Destination address
        @param amount: float ,amount user wishes to deposit
        returns None
        '''
        self.userNameAmountMap[user] = amount ###TODO: save to db for use by mixer

        requestBody = {
            'fromAddress' : user,
            'toAddress' : destAddress,
            'amount' : amount
        }
        requests.post(self.URL, data=requestBody)

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



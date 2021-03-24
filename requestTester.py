
import requests
import simplejson as json
from pprint import pprint

JOBCOIN_URL = 'http://jobcoin.gemini.com/starlit-synergy/api/transactions'

URL = 'http://localhost:5000'

def testAnonymize(user, sourceAddresses):
    url = URL + f'/anonymize/{user}/{sourceAddresses}'
    print(url)
    r = requests.get(url)
    if r.status_code == 200:
        pprint(r.json())
    else:
        print('fail')

def sendMoneyToTempAccount(user, destAddress, amount):
    reqBody = {
        'user' : user,
        'destinationAddress': destAddress,
        'amount' : amount
    }
    url = URL + '/sendCoinsToDestAddress'
    print(url)
    r = requests.post(url, data=reqBody)
    if r.status_code == 200:
        print(r.json())
    else:
        print('fail')
        print(r.status_code)

def getAllTranscations():
    try:
        r = requests.get(JOBCOIN_URL)
        if r.status_code == 200:
            resp = r.json()
            pprint(resp)
        else:
            pprint(r.status_code)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #testAnonymize('Siri', 'Biri12,Biri14')
    sendMoneyToTempAccount('Bob', 'tempDest314', 2)  ### please pick someone with monies :)


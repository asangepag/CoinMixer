import unittest
from CoinMixer.mixer.mixer import Mixer

class MixerTest(unittest): 

    def setUp(self):
        self.tempDestToOrigUserMap = {'tempDest123': 'Alice'}
        self.userSourceAddressMap = {'Alice' : ['Alice1', 'Alice2', 'Alice3']}
        self.mixer = Mixer()

    def testGetOriginalSourceAddressAndSplits(self):
        txn = {
            'fromAddress' : 'tempDest123',
            'toAddress' :'houseAccount',
            'amount' : '50'
        }
        self.assertEquals(self.mixer.getOriginalSourceAddressAndSplits, (['Alice1', 'Alice2', 'Alcie3'], 16.66666))



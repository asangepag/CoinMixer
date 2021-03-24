# CoinMixer
This is split into 3 compoents:
1. RequestProcessor - interfaces with the user to get the unused source addresses, sending amounts to a temp dest for mixing
2. DepositListener - will listen to the transactions and filter on those going to tempAdresses and send them to the house account to be mixed. Currently will achieve polling behavior by query all Transactions from JobCoinAPI , storing an imMemCopy and comparing the diffs in length.
3. Mixer - listens to updates on the transactions and responsible for the business logic of splitting the amounts and anonymizing. Currently will achieve polling behavior by query all Transactions from JobCoinAPI , storing an imMemCopy and comparing the diffs in length.

Note: 
 1. Would ideally build #2 and #3 leveraging AMPS or similar message queues to acheive real time listening capabilities. Could not setup here due to time    
 constraints.
 Twisted works well with the udpates coming from message queues.

2. Components don't talk to each other now.
3. Need to add test cases


Testing:
1. Use requestTester script to test
2. Run directly and observe logs with dummy data, can also check txns endpoint
3. run directly and observe logs with dummy data, can also check txns endpoint


Installation for MAC OS
pip3 install virtualenv
cd projects
virtual env coinMixer
cd coinMixer

source bin/activate

1. pip3 install Flask
2. pip3 install flask-classful
3. pip3 install requests
4. pip3 install twisted






from client import *
from operator import itemgetter
from math import floor

def buy(sym):
    # Limit based on amonut of stock we have already
    # Find lowest ask price
    o = min(filter(lambda x: x[0] == 'ASK' and x[1] == sym, orders()), 
            key = itemgetter(2))
    n = int(floor(0.2 * balance() / o[2]))
    run(user, password, 'BID {} {} {}'.format(sym, o[2], n))

def sell(sym):
    secs = my_securities()
    if(secs[sym][0] > 0):
        o = max(filter(lambda x: x[0] == 'BID' and x[1] == sym, orders()), 
                key = itemgetter(2))
        n = int(floor(secs[sym][0] / 2))
        run(user, password, 'ASK {} {} {}'.format(sym, o[2], n))

def main():
    print 'Money: ', balance()
    buy('XOM')
    my_orders(True)
    my_securities(True)

main()

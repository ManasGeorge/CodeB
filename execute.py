from client import *
from db import *
from operator import itemgetter
from math import floor

def buy(sym):
    # Limit based on amonut of stock we have already
    # Find lowest ask price
    o = min(filter(lambda x: x[0] == 'ASK' and x[1] == sym, orders()), 
            key = itemgetter(2))
    n = int(floor(0.05 * balance() / o[2]))
    run(user, password, 'BID {} {} {}'.format(sym, o[2], n))

def sell(sym):
    secs = my_securities()
    if(secs[sym][0] > 0):
        o = max(filter(lambda x: x[0] == 'BID' and x[1] == sym, orders()), 
                key = itemgetter(2))
        n = int(floor(secs[sym][0] / 2))
        run(user, password, 'ASK {} {} {}'.format(sym, o[2], n))

def moving_average():
    avgs = []
    prices = retrieve_orders(False) #get bids
    for t in tickers:
        l = prices[t]
        mv3 = reduce(lambda x, y: x + y, l[(len(l) - 3):]) / 3
        mv10 = reduce(lambda x, y: x + y, l[(len(l) - 10):]) / 10
        avgs.append((t, mv3, mv10))
    return avgs

def main():
    for i in range(100):
        print '\nMoney: ', balance()

        sleep(1)
        avgs = sorted(moving_average(), key=lambda tup: (tup[2] - tup[1]))

        j = 0
        while avgs[j][1] > avgs[j][2] and j < len(avgs): # Buy if mv3 > mv10
            j += 1
            buy(avgs[j][0])

        avgs.reverse()
        j = 0
        while avgs[j][1] > avgs[j][2] and j < len(avgs):
            j += 1
            sell(avgs[j][0])

        if i % 10 == 0:
            hd = highest_dividend()
            hd.reverse()
            sold = 0
            for stock in hd:
                if stock in map(itemgetter(1), my_orders()):
                    sell(stock)
                    sold = sold + 1
                    if sold > 3:
                        break

        print 'My Orders: '
        my_orders(True)

        print 'My Portfolio: '
        my_securities(True)

        print 'Best: '

main()

from client import *
import math
from db import *
from operator import itemgetter
from math import floor


def buy(sym):
    # Limit based on amonut of stock we have already
    # Find lowest ask price
    o = min(filter(lambda x: x[0] == 'ASK' and x[1] == sym, orders()),
            key = itemgetter(2))
    n = int(floor(0.20 * balance() / o[2]))
    run(user, password, 'BID {} {} {}'.format(sym, o[2], n))

def average(tckr):
    hash_map = retrieve_orders(True)
    count = 0
    price = 0
    for item in hash_map[tckr]:
        count = count + 1
        price += item
    if count > 0:
        price /= count
    return price

def stdv(tckr):
    ## price == variance, sorry
    curr = 0
    ords = orders()
    count = 0
    price = 0
    avg = average(tckr)
    for item in  ords:
        if item[1] == tckr:
            count = count + 1
            price += float ((item[2] - avg) * (item[2] - avg))
    if count >= 1:
        price /= float ((count - 1))
    return math.sqrt(price)

def alpha(tckr):
    std = stdv(tckr)
    se = stock_exchange()
    rse = (se - 10000000) / 10000000
    count = 0
    price = 0
    ords = orders()
    avg = average(tckr)
    for item in  ords:
        if item[1] == tckr:
            count = count + 1
            price += ((item[2] - avg))
    if count > 0:
        price /= float ((count - 1))
    rstock = 0
    if avg > 0:
        rstock = price - avg/ avg
    alp = 0
    if std > 0:
        alp = (rstock - rse) /  std
    return alp

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
    divMap = dividend_map()
    for t in tickers:
        l = prices[t]
        mv3 = reduce(lambda x, y: x + y, l[(len(l) - 3):]) / 3
        mv10 = reduce(lambda x, y: x + y, l[(len(l) - 10):]) / 10
        mv3n1 = reduce(lambda x, y: x + y, l[(len(l) - 4):(len(l) - 1)]) / 3
        mv10n1 = reduce(lambda x, y: x + y, l[(len(l) - 9):(len(l) - 1)]) / 10
        avgs.append((t, mv3, mv10, divMap[t], (mv3 - mv10) - (mv3n1 - mv10n1) + divMap[t]))
    return avgs

def main():
    for i in range(100):
        print '\nMoney: ', balance()
        hd = highest_dividend()

        sleep(0.1)
        avgs = sorted(moving_average(), key=lambda tup: tup[3])

        j = 0
        while j < 3: # Buy if mv3 > mv10
            j += 1
            buy(avgs[j][0])

        #  j = 0
        #  while j < 7:
            #  j += 1
            #  sell(avgs[j][0])

        #  hd.reverse()
        avgs.reverse()
        for j in range(7):
            sell(avgs[j][0])

        print 'My Orders: '
        my_orders(True)

        print 'My Portfolio: '
        my_securities(True)

        print 'Best: '

main()

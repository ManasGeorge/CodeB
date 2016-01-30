from client import *
import math
from db import retrieve_orders

def buy(sym):
    # Limit based on amonut of stock we have already
    # Find lowest ask price
    o = min(filter(lambda x: x[0] == 'ASK' and x[1] == sym, orders()),
            key = itemgetter(2))
    run(user, password, 'BID')

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
    print alp
    return alp

alpha("GOOGL")

import socket
import sys
from operator import itemgetter
from time import sleep
from collections import defaultdict
from tabulate import tabulate

user = 'Cactus'
password = 'carnot'

# Server connection overhead is low enough that we can afford to use multiple calls
# to run for securities() and order() and stuff.

def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        lines = []
        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            #  print(rline.strip())
            lines.append(rline)
            rline = sfile.readline()
    finally:
        sock.close()
    return lines

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def securities():
    # Ticker, Net Worth, Div. Ratio, Volatility
    secs = run(user,password,'SECURITIES')[0].split()[1:]
    secs = [secs[i:i+4] for i in range(0,len(secs),4)]
    secs = map(lambda x: (x[0], float(x[1]), float(x[2]), float(x[3])), secs)
    return secs

def highest_dividend():
    nshares = defaultdict(lambda: 1)
    for order in orders():
        nshares[order[1]] = nshares[order[1]] + order[3]
    sortsec =  sorted(securities(),
            key=(lambda x: x[1] * x[2] / nshares[x[0]]), 
            reverse=True)
    table = map(lambda sec: 
            [sec[0], sec[1] * sec[2] / nshares[sec[0]], 
                sec[1] * sec[2], 
                nshares[sec[0]]], 
            sortsec)
    print tabulate(table, headers = ["Ticker", "Dividend per Share", "Total Dividend", "Shares being traded"])

def map_tickers(command):
    commands = map(lambda x: command + ' ' + x, tickers)
    return run(user, password, *commands)

# Clears all asks and bids
def clear_all():
    ret = map_tickers('CLEAR_BID')
    ret.extend(map_tickers('CLEAR_BID'))
    return ret

# Return all orders that are out
def orders():
    ords = map_tickers('ORDERS')
    ords = map(lambda x: x.split()[1:], ords) # Remove 'SECURITY_ORDERS_OUT' and split
    ords = map(lambda x: [x[i:i+4] for i in range(0,len(x),4)], ords) # Split each bid/ask into separate list
    ords = [bidask for order in ords for bidask in order]
    ords = map(lambda x: (x[0], x[1], float(x[2]), int(x[3])), ords)
    return ords

# Total value (cash + stocks)
def portfolio():
    return

def order_book():
    print tabulate(orders())

tickers = map(itemgetter(0), securities())

def moving_average():
    avgs = []
    for t in tickers:
        #l = get hist[t]
        l = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6, .65, .7, .75, .8, .85, .9, .95]

        mv3 = reduce(lambda x, y: x + y, l[(len(l) - 3):]) / 3
        mv10 = reduce(lambda x, y: x + y, l[(len(l) - 10):]) / 10
        avgs.append((t, mv3, mv10, (mv3 - mv10)))

    return avgs

print tabulate(moving_average())
    
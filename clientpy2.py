import socket
import sys
from operator import itemgetter

user = 'Cactus'
password = 'carnot'
tickers = ['AAPL', 'C', 'CMG', 'DELL', 'DIS', 'F', 'GM', 'IBM', 'JPY', 'XOM'] 
    
def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    lines = []
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def pull_stocks():
    # Ticker, Net Worth, Div. Ratio, Volatility
    secs = run(user,password,'SECURITIES')[0].split()[1:]
    secs = [secs[i:i+4] for i in range(0,len(secs),4)]
    secs = map(lambda x: (x[0], float(x[1]), float(x[2]), float(x[3])), secs)
    return secs

def highest_dividend():
    return sorted(pull_stocks(),
            key=(lambda x: x[1] * x[2]), 
            reverse=True)

# Clears all asks and bids
def clear_all():
    clears = map(lambda x: 'CLEAR_BID ' + x, tickers)
    clears.extend(map(lambda x: 'CLEAR_ASK ' + x, tickers))
    return run(user, password, *clears)

# Total value (cash + stocks)
def portfolio():
    return

import socket
import sys
from operator import itemgetter
from time import sleep

user = 'Cactus'
password = 'carnot'
tickers = ['AAPL', 'C', 'CMG', 'DELL', 'DIS', 'F', 'GM', 'IBM', 'JPY', 'XOM'] 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    global sock
    HOST, PORT = "codebb.cloudapp.net", 17429
    try:
        sock.connect((HOST, PORT))
        divs = highest_dividend()
        divs = map(lambda x: (x[0], x[1]*x[2]), divs)
        print highest_dividend()
    finally:
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def run(user, password, *commands):
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    lines = []
    sock.sendall(data)
    sfile = sock.makefile()
    rline = sfile.readline()
    while rline:
        lines.append(rline)
        rline = sfile.readline()
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
    return sorted(securities(),
            key=(lambda x: x[1] * x[2]), 
            reverse=True)

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

main()

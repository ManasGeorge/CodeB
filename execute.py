import client
import db

def buy(sym):
    # Limit based on amonut of stock we have already
    # Find lowest ask price
    o = min(filter(lambda x: x[0] == 'ASK' and x[1] == sym, client.orders()), 
            key = client.itemgetter(2))
    client.run(client.user, client.password, 'BID')

def sell(sym):
	return

def moving_average():
    avgs = []
    prices = db.retrieve_orders(False) #get bids
    for t in client.tickers:
        l = prices[t]
        mv3 = reduce(lambda x, y: x + y, l[(len(l) - 3):]) / 3
        mv10 = reduce(lambda x, y: x + y, l[(len(l) - 10):]) / 10
        avgs.append((t, mv3, mv10))
    return avgs

db.make_table()
db.save_orders(10)

for i in range(100):
    client.clear_all()
    avgs = sorted(moving_average(), key=lambda tup: (tup[2] - tup[1]))

    j = 0
    while avgs[j][1] > avgs[j][2]: # Buy if mv3 > mv10
        j += 1
        buy(avgs[j][0])

    avgs.reverse()
    j = 0
    while avgs[j][1] > avgs[j][2]:
        j += 1
        sell(avgs[j][0])

    print i

print client.tabulate(moving_average())
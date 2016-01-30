import sqlite3
import client

dbname = 'orders.db'

def make_table():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('DROP TABLE bids')
    c.execute('DROP TABLE asks')
    c.execute('CREATE TABLE bids (time int, sym text, val real, qty real)')
    c.execute('CREATE TABLE asks (time int, sym text, val real, qty real)')
    conn.commit()
    conn.close()

def save_orders(time):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    try:
        for t in range(time):
            print 'Saving time step', t
            client.sleep(1)
            for o in client.orders():
                if o[0] == 'BID':
                    c.execute("INSERT INTO bids VALUES (?, ?, ?, ?)",
                        [t,o[1],o[2],o[3]])
                elif o[0] == 'ASK':
                    c.execute("INSERT INTO asks VALUES (?, ?, ?, ?)",
                        [t,o[1],o[2],o[3]])
    finally:
        conn.commit()
        conn.close()

def retrieve_orders(asks = True):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    prices = {}
    table = 'asks' if asks else 'bids'
    pricefunc = 'MIN' if asks else 'MAX'
    for sym in client.tickers:
        prices[sym] = c.execute('SELECT {}(val) FROM {} WHERE sym=? GROUP BY time ORDER BY time'
                .format(pricefunc, table), (sym, )).fetchall() 
        prices[sym] = map(client.itemgetter(0), prices[sym])
        conn.commit()
    conn.close()
    return prices

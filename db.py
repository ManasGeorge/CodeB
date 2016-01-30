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

def save_orders():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    t = 0
    try:
        while(1):
            sleep(1)
            for o in orders():
                if o[0] == 'BID':
                    print c.execute("INSERT INTO bids VALUES ({}, '{}', {}, {})"
                            .format(t,o[1],o[2],o[3]))
                elif o[0] == 'ASK':
                    print c.execute("INSERT INTO asks VALUES ({}, '{}', {}, {})"
                            .format(t,o[1],o[2],o[3]))
            t = t + 1
    finally:
        conn.commit()
        conn.close()

def retrieve_orders():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    print c.execute('SELECT * FROM bids').fetchall()
    conn.commit()
    conn.close()

make_table()
save_orders()

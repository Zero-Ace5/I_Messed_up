import time
import requests
import sqlite3
from datetime import datetime, UTC

conn = sqlite3.connect("prices.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS prices (ts TEXT, value REAL)")

while True:
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    ).json()
    print(r)
    if "bitcoin" in r:
        price = r["bitcoin"]["usd"]
        c.execute("INSERT INTO prices VALUES (?, ?)",
                  (datetime.now(UTC), price))
        conn.commit()
        print(f"{datetime.now(UTC)} BTC: ${price}")
    else:
        print("API error, skipping this cycle.")
    time.sleep(60)

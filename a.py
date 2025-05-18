import sqlite3, requests, time

def get_steam_price(market_hash_name):
    url = "https://steamcommunity.com/market/priceoverview/"
    params = {"country": "US", "currency": 1, "appid": 730, "market_hash_name": market_hash_name}
    try:
        res = requests.get(url, params=params, timeout=5).json()
        if res.get("success") and "lowest_price" in res:
            return float(res["lowest_price"].replace("$", "").replace(",", ""))
    except:
        return None
    return None

conn = sqlite3.connect("cs2skins.db")
cur = conn.cursor()
rows = cur.execute("SELECT id, name FROM skins").fetchall()

for id_, name in rows:
    price = get_steam_price(f"{name} (Factory New)")
    if price:
        cur.execute("UPDATE skins SET factory_new = ? WHERE id = ?", (price, id_))
        print(f"Updated {name}: ${price}")
        time.sleep(1.1)

conn.commit()
conn.close()

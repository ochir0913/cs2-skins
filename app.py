import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'cs2skins.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/skins")
def search_skins():
    query = request.args.get("q", "")
    like_query = f"%{query}%"
    conn = get_db_connection()
    cursor = conn.execute("""
        SELECT *,
        ROUND((factory_new + minimal_wear + field_tested + well_worn + battle_scarred)/5.0, 2) AS average_price
        FROM skins
        WHERE name LIKE ? OR weapon LIKE ? OR rarity LIKE ?
    """, (like_query, like_query, like_query))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=False, port=3001)

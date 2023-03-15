from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

URL_PREFIX = 'https://www.buda.com/api/v2'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/max_transactions')
def max_transactions():
    max_transactions = []
    markets = get_markets()
    for each_market in markets:
        timestamp_24hrs_ago = get_timestamp_24hrs_ago()
        trades_for_market = get_trades_for_market(
            each_market["id"],
            timestamp_24hrs_ago
        )

        trade_entries_for_market = trades_for_market["entries"]

        max_transaction_of_market = {
            "market": trades_for_market["market_id"],
            "amount": 0,
            "price": 0,
            "maxTransaction": 0,
            "timestamp": 0,
            "direction": '',
        }

        for entry in trade_entries_for_market:
            transaction = round(float(entry[1]) * float(entry[2]), 2)  # amount * price
            if transaction > max_transaction_of_market["maxTransaction"]:
                max_transaction_of_market["maxTransaction"] = transaction
                max_transaction_of_market["timestamp"] = entry[0]
                max_transaction_of_market["amount"] = round(float(entry[1]), 2)
                max_transaction_of_market["price"] = round(float(entry[2]), 2)
                max_transaction_of_market["direction"] = entry[3]

        max_transactions.append(max_transaction_of_market)

    return jsonify(max_transactions)


def get_markets():
    response = requests.get(f"{URL_PREFIX}/markets")
    response_parsed = response.json()
    markets = response_parsed["markets"]
    return markets


def get_trades_for_market(market_id, timestamp):
    response = requests.get(f"{URL_PREFIX}/markets/{market_id}/trades?timestamp={timestamp}")
    response_parsed = response.json()
    trades = response_parsed["trades"]
    return trades


def get_timestamp_24hrs_ago():
    return int((time.time() - 24 * 60 * 60) * 1000)


if __name__ == '__main__':
    app.run(debug=True)

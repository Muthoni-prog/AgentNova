from dotenv import load_dotenv
import os
import requests
from src.notify_discord import send_alert
from src.analyze import interpret_whale_tx

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
WALLET = "0x28C6c06298d514Db089934071355E5743bf21d60"  # Binance whale example

last_seen_hash = None  # memory of last alert sent


def check_latest_whale_tx():
    global last_seen_hash

    url = (
        "https://api.etherscan.io/v2/api"
        f"?module=account&action=txlist"
        f"&address={WALLET}&startblock=0&endblock=99999999"
        f"&sort=desc&chainid=1&apikey={ETHERSCAN_API_KEY}"
    )

    data = requests.get(url).json()

    if "result" not in data or not isinstance(data["result"], list):
        print("⚠️ API error or no data returned")
        return

    tx = data["result"][0]  # latest transaction

    # ✅ Prevent duplicate notifications
    if last_seen_hash == tx["hash"]:
        print("⏳ No new whale movement.")
        return

    last_seen_hash = tx["hash"]

    value_eth = int(tx["value"]) / 10**18
    insight = interpret_whale_tx(tx)

    message = f"""
🐋 **Whale Movement Detected**
**From:** `{tx['from']}`
**To:** `{tx['to']}`
**Value:** `{value_eth:.4f} ETH`

🧠 **Insight:** {insight}
"""

    send_alert(message)
    print("✅ Alert sent to Discord.")

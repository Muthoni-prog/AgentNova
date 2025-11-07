from dotenv import load_dotenv
load_dotenv()
import time
from src.track_whales import check_latest_whale_tx

print("🚀 AgentNova is now running continuously...")

while True:
    check_latest_whale_tx()  # checks newest tx + sends discord alert
    time.sleep(300)  # wait 5 minutes

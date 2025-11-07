from dotenv import load_dotenv
load_dotenv()  
import os
import requests

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_alert(message):
    if not WEBHOOK_URL:
        print("⚠️ No webhook configured.")
        return
    
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("✅ Alert sent to Discord.")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
if __name__ == "__main__":
    send_alert("✅ Webhook Test — If you see this, webhook is working!")

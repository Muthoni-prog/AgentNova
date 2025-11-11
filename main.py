from dotenv import load_dotenv
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
import os
import uvicorn
from src.track_whales import check_latest_whale_tx

# =========================
# 🌌 Initialize Environment
# =========================
load_dotenv()

# =========================
# 🚀 Continuous Monitoring
# =========================
print("🚀 AgentNova is now running continuously...")

def start_agent():
    """Continuously monitors whale transactions every 5 minutes."""
    while True:
        check_latest_whale_tx()  # checks newest tx + sends discord alert
        time.sleep(300)  # wait 5 minutes


# =========================
# 🌐 FastAPI Web Server
# =========================
app = FastAPI(title="AgentNova", version="1.0.0")

@app.get("/")
def root():
    return {"status": "AgentNova is online and operational"}

@app.get("/.well-known/agent.json")
def agent_card():
    file_path = os.path.join("src", ".well-known", "agent.json")
    return FileResponse(file_path)


# =========================
# ⚙️ App Runner
# =========================
if __name__ == "__main__":
    # Start the FastAPI server
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    # Optionally start the background monitoring
    # Uncomment below line if you want both server and background agent running together
    # start_agent()

from dotenv import load_dotenv
import time
import threading
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from src.track_whales import check_latest_whale_tx

# =========================
# 🌌 Initialize Environment
# =========================
load_dotenv()

print("🚀 AgentNova backend booting...")


# =====================================================
# 🔄 BACKGROUND WHALE MONITOR (runs every 5 minutes)
# =====================================================
def start_agent():
    """Continuously monitors whale transactions every 5 minutes."""
    while True:
        try:
            print("🔍 Checking whale transactions...")
            check_latest_whale_tx()
        except Exception as e:
            print(f"⚠️ Error in whale checker: {e}")
        time.sleep(300)  # 5 minutes


# =========================
# 🌐 FastAPI Web Server
# =========================
app = FastAPI(title="AgentNova", version="1.0.0")

# Serve static files for Verisense agent.json
app.mount(
    "/.well-known",
    StaticFiles(directory="src/.well-known"),
    name="well-known"
)


@app.on_event("startup")
def launch_background():
    """Start whale tracking in a separate thread when app starts."""
    thread = threading.Thread(target=start_agent, daemon=True)
    thread.start()
    print("🚀 Background whale monitor started.")


@app.get("/")
def root():
    return {"status": "AgentNova is online and operational"}


@app.get("/.well-known/agent.json")
def agent_card():
    """Serve AgentNova's metadata for Verisense."""
    file_path = os.path.join("src", ".well-known", "agent.json")

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/json")

    # Fallback JSON if file missing
    data = {
        "name": "AgentNova",
        "description": "An autonomous AI agent that tracks and analyzes whale transactions on Ethereum in real-time.",
        "version": "1.0.0",
        "author": "Muthoni-prog",
        "repository": "https://github.com/Muthoni-prog/AgentNova",
        "deployment": "https://web-production-49b91.up.railway.app",
        "capabilities": [
            "autonomous-analysis",
            "blockchain-monitoring",
            "discord-notifications"
        ],
        "language": "Python",
        "framework": "FastAPI",
        "category": "Analytical Agent",
        "a2a_compatible": True,
        "license": "MIT"
    }
    return JSONResponse(data)


# =========================
# ⚙️ App Runner
# =========================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

from dotenv import load_dotenv
import time
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

# Serve static files for Verisense agent.json
app.mount(
    "/.well-known",
    StaticFiles(directory="src/.well-known"),
    name="well-known"
)


@app.get("/")
def root():
    return {"status": "AgentNova is online and operational"}


@app.get("/.well-known/agent.json")
def agent_card():
    """Serve AgentNova's metadata for Verisense registration."""
    file_path = os.path.join("src", ".well-known", "agent.json")

    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/json")
    else:
        # fallback JSON response (in case file missing)
        data = {
            "name": "AgentNova",
            "description": "An autonomous AI agent that tracks and analyzes whale transactions on Ethereum in real-time.",
            "version": "1.0.0",
            "author": "Muthoni-prog",
            "repository": "https://github.com/Muthoni-prog/AgentNova",
            "deployment": "https://agentnova-production.up.railway.app",
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
    # Start the FastAPI server
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    # Optionally start background monitoring
    # Uncomment below if you want both server and background agent running together
    # start_agent()

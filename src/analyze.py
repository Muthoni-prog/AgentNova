from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

# Load API key securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def interpret_whale_tx(tx):
    value_eth = int(tx["value"]) / 10**18

    prompt = f"""
You are a professional on-chain market analyst who interprets whale movements.
Provide a concise, neutral analysis.
Avoid hype, avoid emojis.

Transaction:
From: {tx['from']}
To: {tx['to']}
Value (ETH): {value_eth:.4f}

Your analysis:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

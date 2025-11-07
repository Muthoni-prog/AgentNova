import os
from dotenv import load_dotenv
import discord

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 AgentNova is online as {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("✅ AgentNova bot is now online!")

client.run(TOKEN)

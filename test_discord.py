from dotenv import load_dotenv
import os
import discord
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("✅ Bot connected!")
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("✅ Test message from AgentNova.")
    await client.close()

client.run(TOKEN)

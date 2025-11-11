import os
import discord
import requests
import time
import sys
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from threading import Thread

print("Python version:", sys.version)

# === Discord Intents ===
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Discord 事件 ===
@bot.event
async def on_ready():
    print(f"✅ Bot 已登入為 {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    current_time = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%H:%M")

    # 找出 guild
    guild = after.channel.guild if after.channel else before.channel.guild

    # 找到目標文字頻道
    text_channel = discord.utils.get(guild.text_channels, name="簽到表")
    if text_channel is None:
        text_channel = guild.text_channels[0]

    # 加入語音頻道
    if before.channel is None and after.channel is not None:
        msg = f"> 🎧 {member.display_name} 在 {current_time} 加入了語音頻道 <#{after.channel.id}>"
        await text_channel.send(msg)

    # 離開語音頻道
    elif before.channel is not None and after.channel is None:
        msg = f"> 👋 {member.display_name} 在 {current_time} 離開了語音頻道 <#{before.channel.id}>"
        await text_channel.send(msg)

    # 在語音頻道之間移動
    elif before.channel != after.channel:
        msg = f"> 🔄 {member.display_name} 在 {current_time} 從 <#{before.channel.id}> 移動到 <#{after.channel.id}>"
        await text_channel.send(msg)

# === 自動 Ping Render 網址 ===
def self_ping():
    url = os.getenv("RENDER_EXTERNAL_URL", "https://bot-1-oxob.onrender.com")
    while True:
        try:
            res = requests.get(url)
            print(f"✅ Ping 成功 ({res.status_code}) → {url}")
        except Exception as e:
            print(f"⚠️ Ping 失敗：{e}")
        time.sleep(300)  # 每 5 分鐘一次

# === Flask 保活伺服器 ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# === 啟動 Flask & 自我 Ping ===
Thread(target=run_flask, daemon=True).start()
Thread(target=self_ping, daemon=True).start()

# === 啟動 Discord Bot ===
bot.run(os.getenv("DISCORD_TOKEN"))


import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from threading import Thread

# ====== Discord Bot 設定 ======
intents = discord.Intents.default()
intents.voice_states = True  # 監聽語音房事件
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== 時區設定 ======
tz = ZoneInfo("Asia/Taipei")

# ====== Discord Webhook 或頻道ID（用來發送通知）=====
NOTIFY_CHANNEL_ID = int(os.environ.get("NOTIFY_CHANNEL_ID", 0))

# ====== 語音狀態事件 ======
@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(NOTIFY_CHANNEL_ID)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    # 加入語音頻道
    if before.channel is None and after.channel is not None:
        await channel.send(f"{member.name} 在 {now} 加入了 {after.channel.name}")
    
    # 離開語音頻道
    elif before.channel is not None and after.channel is None:
        await channel.send(f"{member.name} 在 {now} 離開了 {before.channel.name}")
    
    # 轉移語音頻道
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        await channel.send(f"{member.name} 在 {now} 從 {before.channel.name} 移動到 {after.channel.name}")

# ====== 讓 Render 免費方案保持活躍 ======
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# ====== 啟動 ======
if __name__ == "__main__":
    # Flask server 用於 Ping 保活
    Thread(target=run_flask).start()
    
    # 啟動 Discord Bot
    bot.run(os.environ.get("DISCORD_TOKEN"))

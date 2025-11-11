import os
import discord
import requests
import threading
import time
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

# 啟用必要的 Intents
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot 已登入為 {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    current_time = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%H:%M")

    # 確定哪邊有 guild（因為離開語音頻道時 after.channel 會是 None）
    guild = after.channel.guild if after.channel else before.channel.guild

    # 找到目標文字頻道
    text_channel = discord.utils.get(guild.text_channels, name="簽到表")
    if text_channel is None:
        text_channel = guild.text_channels[0]  # 備用方案：第一個文字頻道

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

# --- Ping 自己的 Render 網址 ---
def self_ping():
    url = "https://bot-1-oxob.onrender.com"  # 改成你的 Render 網址
    while True:
         try:
            res = requests.get(url)
            print(f"✅ Ping 成功 ({res.status_code}) → {url}")
        except Exception as e:
            print(f"⚠️ Ping 失敗：{e}")
        time.sleep(300)  # 每 5 分鐘 ping 一次

# 開啟保活執行緒
threading.Thread(target=keep_alive, daemon=True).start()

# 啟動 Bot（使用環境變數中儲存的 Token）
bot.run("MTQzNzc3OTM5NzQzOTUyNDk0NQ.GGHEwK.qzfKAYl4APf2xEFshgXJ8qS-YUhFDi0oacacps")









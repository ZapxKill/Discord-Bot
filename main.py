import discord
import asyncio
import json
from discord.ext import commands
import os

jsonfile = open("setting.json")  # 開啟Json設定檔
setting = json.load(jsonfile)  # 讀取Json設定檔
intents = discord.Intents.default()  # 取得預設權限
intents.members = True  # 新增成員存取權限
intents.message_content = True  # 新增訊息存取全縣
bot = commands.Bot(intents=intents)  # 建立機器人物件，並以$作為指令前綴


@bot.event
async def on_ready():  # 啟動完畢時，終端機顯示機器人名字
    print("已啟動:", bot.user)


@bot.slash_command(description="載入Cog")
async def load_cog(context, extension):  # 讀取指定Cog
    bot.load_extension(f"cmds.{extension}")
    await context.respond("loaded")  # 讀取完畢，回傳訊息


@bot.slash_command(description="卸載Cog")
async def unload_cog(context, extension):  # 卸載指定Cog
    bot.unload_extension(f"cmds.{extension}")
    await context.respond("unloaded")  # 卸載完畢，回傳訊息


@bot.slash_command(description="重新載入Cog")
async def reload_cog(context, extension):  # 重新讀取指定Cog
    bot.reload_extension(f"cmds.{extension}")
    await context.respond("reloaded")  # 重新讀取完畢，回傳訊息




    
for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            bot.load_extension("cmds." + filename[:-3])

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start(setting["TOKEN"])) # 給予Token，啟動Bot

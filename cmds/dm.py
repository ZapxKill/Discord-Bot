import discord
from discord.ext import commands


class dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="傳送訊息給某人")
    async def send(self, context, target, m):  # 使用機器人發送訊息給指定人
        targetid = int(target)  # 目標id
        channel = context.channel  # 接收指令的頻道
        user = await self.bot.fetch_user(targetid)  # 取得目標的使用者物件
        await user.send((f"{m}\n<@{targetid}>"))  # 發送訊息
        await channel.respond("成功發送")  # 回傳成功訊息

    @discord.slash_command(description="吵某人")
    async def ping(self, context, target, times):
        targetid = int(target)
        channel = context.channel
        user = await self.bot.fetch_user(targetid)
        for i in range(int(times)):
            await user.send(user.mention, delete_after=0.01)
        await channel.respond("成功發送")

    
        

def setup(bot):
    bot.add_cog(dm(bot))

import discord
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):  # 當成員加入伺服器
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"<@{member.id}>歡迎")  # 取得成員名稱並傳送訊息到指定頻道

    @commands.Cog.listener()
    async def on_member_remove(self, member):  # 當成員離開伺服器
        channel = member.guild.system_channel
        if channel:
            await channel.send(f"<@{member.id}>掰掰")  # 取得成員名稱並傳送訊息到指定頻道



def setup(bot):
    bot.add_cog(events(bot))

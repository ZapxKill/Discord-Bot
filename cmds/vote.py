import discord
import asyncio
from discord.ext import commands
from discord.utils import get

class vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command(description="發起投票")
    async def vote(self, context, votequest, timer):
        msg = await context.send(f'```py\n@===投票===@ \n\n"{votequest}"\n\n@-時間:{timer}s-@\n```')    #顯示問題和時間
        await msg.add_reaction('✅')    #增加同意回應
        await msg.add_reaction('❎')    #增加反對回應
        for t in range(int(timer), -1, -1):     #計時器
            await msg.edit(content = f'```py\n@===投票===@ \n\n"{votequest}"\n\n@-時間:{t}s-@\n```')    #時間更新
            await asyncio.sleep(1)
        msg = await msg.channel.fetch_message(msg.id)   #更新機器人訊息緩存
        vote_yes = get(msg.reactions, emoji='✅')  #取得同意回應數量
        vote_no = get(msg.reactions, emoji='❎')   #取得反對回應數量
        await msg.delete()  #刪除投票訊息
        await context.send(f'```py\n@===投票結果===@ \n\n"{votequest}"\n\n@贊成:{vote_yes.count-1}     @反對:{vote_no.count-1}\n```')   #回傳問題和票數

def setup(bot):
    bot.add_cog(vote(bot))


    
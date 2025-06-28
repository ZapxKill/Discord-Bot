
import discord
from discord.ext import commands

import os

class copytext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="sus")
    async def redsus(self, ctx):
        await ctx.respond(
            "឵ ឵឵                             ⬛⬛⬛⬛⬛⬛\n                         ⬛🟥🟥🟥🟥🟥🟥⬛\n                    ⬛🟥🟥🟥🟥🟥🟥🟥🟥⬛\n               ⬛🟥🟥🟥🟥⬛⬛⬛⬛⬛⬛\n               ⬛🟥🟥🟥⬛🟦🟦⬜⬜⬜⬜⬛\n               ⬛🟥🟥⬛🟪🟦🟦🟦⬜⬜⬜🟦⬛\n     ⬛⬛⬛🟥🟥⬛🟪🟦🟦🟦🟦🟦🟦🟦⬛\n⬛🟥🟥⬛🟥🟥⬛🟪🟪🟪🟦🟦🟦🟦🟪⬛\n⬛🟥🟥⬛🟥🟥🟥⬛🟪🟪🟪🟪🟪🟪⬛\n⬛🟥🟥⬛🟥🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛\n⬛🟥🟥⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛\n⬛🟥🟥⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛\n⬛🟥🟥⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛\n⬛🟥🟥⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛\n⬛🟥🟥⬛🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛\n⬛🟥🟥"
        )

    @discord.slash_command(description="现在的孩子冲到机厅就是...以下略")
    async def pan(self, ctx):
        await ctx.defer()
        image = discord.File("./images/pan.gif")
        await ctx.send_followup(
            content="现在的孩子冲到机厅就是把其他人从机上赶下来然后投币扫码上机选中​PANDORA PARADOXX​X开始游戏然后一个大双扫键再来四个长条双押4635交互交互星星错位18星星36tap借5432位移交互一个慢速圈两个绝赞一个快速位移交互一个圈一堆水长条夹一点16分交互散打借三连交互然后绝赞星星tap还有反手交互一个位移交互加延迟星星接tap然后18错位双押星星延迟星星加三连音一点散打和一个大扫键然后双押18到36然后双押扫键双押扫键双押扫键星星双押扫键双押扫键双押扫键星星双押扫键双押扫键扫键扫键扫键扫键星星接着噔噔 噔噔 双押扫键双押扫键扫键扫键一个圈然后星星tap散打一个hold然后快速双扫键到6一个位移交互然后我有抑郁症圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打圈圈圈打然后反手圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打圈圈圈圈打停在8hold接一堆星星一笔画tap三连音双押和连续小扫键抬然后位移交互伪双押绝赞伪双押绝赞伪双押绝赞绝赞折返星星然后一堆星星一笔画tap三连音和双小扫键位移交互小圈接一慢星星tap后一个双押星星然后星星tap上上下下一堆双押然后双押单点单点单点双押单点单点单点双押单点单点单点双押单点单点单点双押单点单点单点双押单点单点单点双押单点单点单点双押单点单点单点然后45，67，81，23双押然后交互交互交互扫键扫键交互交互交互散打双押双押双押双押双押双押双押双押散打散打散打交互交互交互交互交互圈两个慢星星然后噔噔绝赞抬头ALL PREFECT PLUS然后下机",
            file=image,
        )

    @discord.slash_command(description="你應該看得懂")
    async def arigatou(self, ctx):
        await ctx.defer()
        image = discord.File("./images/nina.gif")
        await ctx.send_followup(
            content="",
            file=image,
        )


def setup(bot):
    bot.add_cog(copytext(bot))

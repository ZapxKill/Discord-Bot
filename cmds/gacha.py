import discord
import random
from discord.ext import commands

class gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(description="九藍一金!!!!!")
    async def gacha(self, ctx):
        result = ''
        for i in range(0,9):
            chance = random.random()
            if(i == 5):
                result += '\n'
            if(chance <= 0.03):
                result += '📕'
            elif(chance <=0.185):
                result += '📒'
            else:
                result += '📘'
        chance = random.random()
        if(chance <= 0.03):
            result += '📕'
        else:
            result += '📒'
        await ctx.respond(result, view=rollButton())

class rollButton(discord.ui.View):
    @discord.ui.button(label="再來十抽", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        result = ''
        for i in range(0,9):
            chance = random.random()
            if(i == 5):
                result += '\n'
            if(chance <= 0.03):
                result += '📕'
            elif(chance <=0.185):
                result += '📒'
            else:
                result += '📘'
        chance = random.random()
        if(chance <= 0.03):
            result += '📕'
        else:
            result += '📒'
        await interaction.message.delete()
        await interaction.respond(result, view=rollButton())
        



def setup(bot):
    bot.add_cog(gacha(bot))
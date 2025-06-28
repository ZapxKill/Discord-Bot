import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from PIL import Image
import json
import time
import os


class arcade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="查詢maimai個人資料")
    async def mai_profile(self, context):
        await context.defer()
        setting = json.load(open("./setting.json"))
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(
            "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/"
        )
        driver.find_element(By.ID, "segaid").click()
        driver.find_element(By.ID, "sid").send_keys(setting["Segaid"]["sid"])
        driver.find_element(By.ID, "password").send_keys(setting["Segaid"]["password"])
        driver.find_element(By.ID, "btnSubmit").click()
        driver.find_element(By.CLASS_NAME, "basic_block.p_10.f_0").screenshot(
            "./images/maiPlayer0.png"
        )
        driver.get("https://maimaidx-eng.com/maimai-mobile/friend/")
        playerList = driver.find_elements(By.CLASS_NAME, "basic_block.p_10.f_0")
        bg = Image.new("RGBA", (426, 133 * (len(playerList) + 1)), "#ffffff")
        bg.paste(Image.open("./images/maiPlayer0.png"), (0, 0))
        for i in range(0, len(playerList)):
            playerList[i].screenshot(f"./images/maiPlayer{i+1}.png")
            bg.paste(Image.open(f"./images/maiPlayer{i+1}.png"), (0, 133 * (i + 1)))
        bg.save("./images/maiPlayers.png")
        await context.send_followup(
            content=None, file=discord.File("./images/maiPlayers.png")
        )
        for i in range(0, len(playerList) + 1):
            os.remove(f"./images/maiPlayer{i}.png")
        os.remove(f"./images/maiPlayers.png")
        driver.close()

    @discord.slash_command(description="查詢chunithm個人資料")
    async def chu_profile(self, context):
        await context.defer()
        setting = json.load(open("./setting.json"))
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(
            "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/&back_url=https://chunithm.sega.com/"
        )
        driver.find_element(By.ID, "segaid").click()
        driver.find_element(By.ID, "sid").send_keys(setting["Segaid"]["sid"])
        driver.find_element(By.ID, "password").send_keys(setting["Segaid"]["password"])
        driver.find_element(By.ID, "btnSubmit").click()
        driver.find_element(By.CLASS_NAME, "box_playerprofile").screenshot(
            "./images/chuPlayer0.png"
        )
        driver.get("https://chunithm-net-eng.com/mobile/friend/")
        playerList = driver.find_elements(By.CLASS_NAME, "box_playerprofile")
        bg = Image.new("RGBA", (420, 196 * (len(playerList) + 1)), "#ffffff")
        bg.paste(Image.open("./images/chuPlayer0.png"), (0, 0))
        for i in range(0, len(playerList)):
            playerList[i].screenshot(f"./images/chuPlayer{i+1}.png")
            bg.paste(Image.open(f"./images/chuPlayer{i+1}.png"), (0, 196 * (i + 1)))
        bg.save("./images/chuPlayers.png")
        await context.send_followup(
            content=None, file=discord.File("./images/chuPlayers.png")
        )
        for i in range(0, len(playerList) + 1):
            os.remove(f"./images/chuPlayer{i}.png")
        os.remove(f"./images/chuPlayers.png")
        driver.close()

    @discord.slash_command(description="查詢maimai最近歌曲")
    async def mai_recents(self, context, num=1):
        await context.defer()
        num = int(num)
        if num > 50:
            num = 50
        setting = json.load(open("./setting.json"))
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(
            "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/"
        )
        driver.find_element(By.ID, "segaid").click()
        driver.find_element(By.ID, "sid").send_keys(setting["Segaid"]["sid"])
        driver.find_element(By.ID, "password").send_keys(setting["Segaid"]["password"])
        driver.find_element(By.ID, "btnSubmit").click()
        driver.get("https://maimaidx-eng.com/maimai-mobile/record/")
        songlist = driver.find_elements(By.CLASS_NAME, "p_10.t_l.f_0.v_b")
        bg = Image.new("RGBA", (480, 305 * num), "#ffffff")
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 200):
            driver.execute_script(f"window.scrollTo(0, {i});")
        for i in range(0, num):
            songlist[i].screenshot(f"./images/maiSong{i}.png")
            bg.paste(Image.open(f"./images/maiSong{i}.png"), (0, 305 * i))
        bg.save("./images/maiSongs.png")
        await context.send_followup(
            content=None, file=discord.File("./images/maiSongs.png")
        )
        for i in range(0, num):
            os.remove(f"./images/maiSong{i}.png")
        os.remove("./images/maiSongs.png")
        driver.close()

    @discord.slash_command(description="查詢chunithm最近歌曲")
    async def chu_recents(self, context, num=1):
        await context.defer()
        num = int(num)
        if num > 50:
            num = 50

        setting = json.load(open("./setting.json"))
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(
            "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=chuniex&redirect_url=https://chunithm-net-eng.com/mobile/&back_url=https://chunithm.sega.com/"
        )
        driver.find_element(By.ID, "segaid").click()
        driver.find_element(By.ID, "sid").send_keys(setting["Segaid"]["sid"])
        driver.find_element(By.ID, "password").send_keys(setting["Segaid"]["password"])
        driver.find_element(By.ID, "btnSubmit").click()
        driver.get("https://chunithm-net-eng.com/mobile/record/playlog")
        songlist = driver.find_elements(By.CLASS_NAME, "frame02.w400")
        bg = Image.new("RGBA", (400, 206 * num), "#ffffff")
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 100):
            driver.execute_script(f"window.scrollTo(0, {i});")
        for i in range(0, num):
            songlist[i].screenshot(f"./images/chuSong{i}.png")
            bg.paste(Image.open(f"./images/chuSong{i}.png"), (0, 206 * i))
        bg.save("./images/chuSongs.png")
        await context.send_followup(
            content=None, file=discord.File("./images/chuSongs.png")
        )
        for i in range(0, num):
            os.remove(f"./images/chuSong{i}.png")
        os.remove("./images/chuSongs.png")
        driver.close()


def setup(bot):
    bot.add_cog(arcade(bot))

import discord
import requests
import json
import asyncio
from discord.ext import commands
from discord.utils import get

jsonfile = open("./setting.json")  # 開啟Json設定檔
setting = json.load(jsonfile)  # 讀取Json設定檔
area = [
    5,
    1,
    18,
    13,
    7,
    4,
    3,
    8,
    11,
    20,
    14,
    9,
    0,
    2,
    6,
    15,
    17,
    10,
    12,
    19,
    16,
    21,
]  # 選項對照表
D_area = {
    "台北市": 5,
    "臺北市": 5,
    "新北市": 1,
    "基隆市": 18,
    "桃園市": 13,
    "宜蘭縣": 7,
    "新竹市": 4,
    "新竹縣": 3,
    "苗栗縣": 8,
    "台中市": 11,
    "臺中市": 11,
    "彰化縣": 20,
    "南投縣": 14,
    "雲林縣": 9,
    "嘉義縣": 0,
    "嘉義市": 2,
    "台南市": 6,
    "臺南市": 6,
    "高雄市": 15,
    "屏東縣": 17,
    "花蓮縣": 10,
    "台東縣": 12,
    "臺東縣": 12,
    "澎湖縣": 19,
    "金門縣": 16,
    "連江縣": 21,
}  # 文字對照表


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @discord.slash_command(description="天氣查詢")
    async def weather(self, context):
        await context.respond("```🗺️請選擇要查詢的縣市名稱🗺️```", view=areaOptions())

    @discord.slash_command(description="天氣查詢")
    async def oldweather(self, context, areainput=None):
        data = requests.get(setting["Weather"]["url"]).json()  # 取得中央氣象局資料
        if areainput:  # 如果有輸入地名
            if D_area.get(areainput):
                select = D_area[areainput]  # 搜尋此地名對照表
            else:
                await context.channel.send("```查無此地區```")  # 若無此名稱回傳此訊息
        else:  # 若無輸入地名
            question = await context.channel.send(
                "```🗺️請選擇想要查詢的區域：\n1️⃣北部地區 2️⃣中部地區\n3️⃣南部地區 4️⃣東部地區\n5️⃣外島地區```"
            )  # 回傳此訊息
            select = await userChoice(5, question)  # 使用者選擇
            match select:
                case 0:
                    question = await context.channel.send(
                        "```🗺️請選擇想要查詢的縣市：\n1️⃣台北市 2️⃣新北市\n3️⃣基隆市 4️⃣桃園市\n5️⃣宜蘭縣 6️⃣新竹市\n7️⃣新竹縣\n```"
                    )  # 回傳此訊息
                    select = await userChoice(7, question)  # 使用者選擇
                case 1:
                    question = await context.channel.send(
                        "```🗺️請選擇想要查詢的縣市：\n1️⃣苗栗縣 2️⃣台中市\n3️⃣彰化縣 4️⃣南投縣\n5️⃣雲林縣\n```"
                    )  # 回傳此訊息
                    select = await userChoice(5, question) + 7  # 使用者選擇
                case 2:
                    question = await context.channel.send(
                        "```🗺️請選擇想要查詢的縣市：\n1️⃣嘉義縣 2️⃣嘉義市\n3️⃣台南市 4️⃣高雄市\n5️⃣屏東縣\n```"
                    )  # 回傳此訊息
                    select = await userChoice(5, question) + 12  # 使用者選擇
                case 3:
                    question = await context.channel.send(
                        "```🗺️請選擇想要查詢的縣市：\n1️⃣花蓮縣 2️⃣台東縣\n```"
                    )  # 回傳此訊息
                    select = await userChoice(2, question) + 17  # 使用者選擇
                case 4:
                    question = await context.channel.send(
                        "```🗺️請選擇想要查詢的縣市：\n1️⃣澎湖縣 2️⃣金門縣\n3️⃣連江縣```"
                    )  # 回傳此訊息
                    select = await userChoice(3, question) + 19  # 使用者選擇
            select = area[select]
        if data["success"]:  # 當資料正常時
            dataSelect = data["records"]["location"][select]
            areaName = dataSelect["locationName"]  # 取得地名
            rain = dataSelect["weatherElement"][1]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得降雨率
            weather = dataSelect["weatherElement"][0]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得天氣
            feel = dataSelect["weatherElement"][3]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得感受
            Ltemp = dataSelect["weatherElement"][2]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得最低溫
            Htemp = dataSelect["weatherElement"][4]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得最高溫
            await context.channel.send(
                f"```{areaName}氣象報告\n最近36小時:\n☁️天氣:{weather}\n☂️降雨機率:{rain}%\n🌡️溫度:{Ltemp}~{Htemp}度\n🧑🏻感受:{feel}```"
            )  # 回傳上述資料
        else:
            await context.channel.send("天氣取得失敗")  # 資料不正常時，回傳此訊息
        
class areaOptions(discord.ui.View):
    @discord.ui.select(
        placeholder="選擇一個縣市",
        min_values=1,
        max_values=1,
        options = [
            discord.SelectOption(
                label="基隆市",
                value='18'
            ),
            discord.SelectOption(
                label="新北市",
                value='1'
            ),
            discord.SelectOption(
                label="臺北市",
                value='5'
            ),
            discord.SelectOption(
                label="宜蘭縣",
                value='7'
            ),
            discord.SelectOption(
                label="桃園市",
                value='13'
            ),
            discord.SelectOption(
                label="新竹市",
                value='4'
            ),
            discord.SelectOption(
                label="新竹縣",
                value='3'
            ),
            discord.SelectOption(
                label="苗栗縣",
                value='8'
            ),
            discord.SelectOption(
                label="臺中市",
                value='11'
            ),
            discord.SelectOption(
                label="彰化縣",
                value='20'
            ),
            discord.SelectOption(
                label="南投縣",
                value='14'
            ),
            discord.SelectOption(
                label="雲林縣",
                value='9'
            ),
            discord.SelectOption(
                label="嘉義縣",
                value='0'
            ),
            discord.SelectOption(
                label="嘉義市",
                value='2'
            ),
            discord.SelectOption(
                label="臺南市",
                value='6'
            ),
            discord.SelectOption(
                label="高雄市",
                value='15'
            ),
            discord.SelectOption(
                label="屏東縣",
                value='17'
            ),
            discord.SelectOption(
                label="花蓮縣",
                value='10'
            ),
            discord.SelectOption(
                label="臺東縣",
                value='12'
            ),
            discord.SelectOption(
                label="澎湖縣",
                value='19'
            ),  
            discord.SelectOption(
                label="金門縣",
                value='16'
            ),  
            discord.SelectOption(
                label="連江縣",
                value='21'
            )          
        ]
    )
    async def select_callback(self, select, interaction):
        data = requests.get(setting["Weather"]["url"]).json()
        if data["success"]:  # 當資料正常時
            dataSelect = data["records"]["location"][int(select.values[0])]
            areaName = dataSelect["locationName"]  # 取得地名
            rain = dataSelect["weatherElement"][1]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得降雨率
            weather = dataSelect["weatherElement"][0]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得天氣
            feel = dataSelect["weatherElement"][3]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得感受
            Ltemp = dataSelect["weatherElement"][2]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得最低溫
            Htemp = dataSelect["weatherElement"][4]["time"][0]["parameter"][
                "parameterName"
            ]  # 取得最高溫
            await interaction.respond(
                f"```{areaName}氣象報告\n最近36小時:\n☁️天氣:{weather}\n☂️降雨機率:{rain}%\n🌡️溫度:{Ltemp}~{Htemp}度\n🧑🏻感受:{feel}```"
            )  # 回傳上述資料
        else:
            await interaction.respond("天氣取得失敗，請稍後再試")  # 資料不正常時，回傳此訊息


async def userChoice(num, question):
    choice = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]  # 選擇用表情符號
    timer = 0  # 新增計時器用於避免使用者不回應導致程式無限迴圈
    for i in range(0, num):
        await question.add_reaction(choice[i])  # 新增回饋表情符號
    selected = False
    while not selected:  # 等待使用者選擇
        question = await question.channel.fetch_message(
            question.id
        )  # 更新訊息在機器人中的緩存
        for i in range(0, num):
            if question.reactions[i].count - 1:
                await question.delete()  # 偵測使用者選擇的選項
                selected = True
                return i
        if timer >= 60:  # 如果使用者一分鐘沒有回應
            await question.delete()  # 刪除此訊息
            return -1
        await asyncio.sleep(1)
        timer += 1
    


def setup(bot):
    bot.add_cog(weather(bot))

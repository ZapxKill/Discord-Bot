import discord
from discord.ext import commands
from discord import FFmpegOpusAudio
import requests
import json
host = "127.0.0.1"
port = "50021"

class voicevox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="虛擬聲音產生器")
    async def vox(self, ctx, voiceline=None, chosenvoice=3, speed=1.0, pitch=0.0, intonation=1.0, volume=1.0):
        if(voiceline == None):
            await ctx.send('```$vox 台詞 角色 速度(0.5~2.0) 音高(-0.15~0.15) 抑揚(0.0~2.0) 音量(0.0~2.0)```')
            return
        if(speed > 2): speed = 2
        elif(speed < 0.5): speed = 0.5
        if(pitch > 0.15): pitch = 0.15
        elif(pitch < -0.15): pitch = -0.15
        if(intonation > 2): intonation = 2
        elif(intonation < 0): intonation = 0.5
        if(volume > 2): volume = 2
        elif(volume < 0): volume = 0.0
        audioQuery = createAudio_query(voiceline, chosenvoice)
        audioQuery["speedScale"] = speed
        audioQuery["pitchScale"] = pitch
        audioQuery["intonationScale"] = intonation
        audioQuery["volumeScale"] = volume
        with open("./sounds/voxVoice.wav", "wb") as f:
            f.write(synthesis(audioQuery, chosenvoice))
        if(not ctx.voice_client):   #如果機器人不在語音頻道中
            voiceChannel = ctx.author.voice.channel
            if(voiceChannel == None):
                await ctx.send("What are you doing? You are not in channel")    #如果指令發送者不在語音頻道，發送此訊息
                return
            await voiceChannel.connect()   #進入指令發送者的語音頻道
        source = FFmpegOpusAudio('./sounds/voxVoice.wav') #利用FFmpeg產生聲音源
        ctx.voice_client.play(source)   #將聲音源播放至語音中
        ctx.respond("succeed")

    @discord.slash_command(description="展示可用聲線")
    async def speaker_list(self, ctx):
        res = requests.get(f"http://{host}:{port}/speakers")
        speakerList = res.json()
        speakers = ""
        for i in range(0,len(speakerList)):
            speakers += f"{speakerList[i]['name']}\n"
            for j in range(0,len(speakerList[i]['styles'])):
                speakers += f"  {speakerList[i]['styles'][j]['name']}:{speakerList[i]['styles'][j]['id']}\n"
        await ctx.respond(f"```{speakers}```")

def createAudio_query(text, speaker) -> dict:
    params = {"text": text, "speaker": speaker}
    res = requests.post(f"http://{host}:{port}/audio_query", params=params)
    data = res.json()
    return data
    
def synthesis(audioQuery, speaker) -> bytes:
    params = {"speaker": speaker}
    headers = {"content-type": "application/json"}
    res = requests.post(f"http://{host}:{port}/synthesis", data=json.dumps(audioQuery), params=params, headers=headers) 
    return res.content

    
def setup(bot):
    bot.add_cog(voicevox(bot))
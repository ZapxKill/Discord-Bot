import discord
import asyncio
from typing import Optional
from pytubefix import YouTube
from pytubefix import Playlist
import os
from discord.ext import commands
from discord import FFmpegOpusAudio

musicPlaylist = []  # 待播放的網址
nowPlaying = False  # 現在播放的網址
filename = []


class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="加入語音頻道")
    async def join(self, ctx):  # 加入指令發送者的語音頻道
        voice = ctx.author.voice
        if voice == None:
            await ctx.respond(
                "What are you doing? You are not in channel"
            )  # 如果指令發送者不在語音頻道，發送此訊息
            return
        await voice.channel.connect()  # 進入指令發送者語音頻道
        await ctx.respond("Joined!")

    @discord.slash_command(description="播放youtube URL或檔案")
    async def play(self, ctx, path=None):  # 撥放sounds資料夾內的指定檔案
        global nowPlaying
        global musicPlaylist
        if not ctx.voice_client:  # 如果機器人不在語音頻道中
            voice = ctx.author.voice
            if voice == None:
                await ctx.respond(
                    "What are you doing? You are not in channel"
                )  # 如果指令發送者不在語音頻道，發送此訊息
                return
            await voice.channel.connect()  # 進入指令發送者的語音頻道
        if await isYoutubeVideo(path) == 2:
            try:
                musicPlaylist.extend(
                    Playlist(path).videos
                )  # 如果網址是Youtube播放清單，將其播放清單輸入至待播放的網址
                await ctx.respond(f"{path} has Added to playlist")
            except:
                musicPlaylist.append(
                    YouTube(path, use_oauth=True, allow_oauth_cache=True)
                )  # 如果網址是Youtube影片，將其輸入至待播放的網址
                await ctx.respond(f"{path} has Added to playlist")
            if not ctx.voice_client.is_playing():  # 如果目前沒有播放聲音源
                nowPlaying = musicPlaylist.pop(0)  # 將播放清單第一首取出
                await getYoutubeSource(nowPlaying)  # 下載mp3檔案
                source = FFmpegOpusAudio(f"./sounds/temp.mp3")  # 利用FFmpeg產生聲音源
                ctx.voice_client.play(
                    source, after=lambda _: asyncio.run_coroutine_threadsafe(playNext(ctx), ctx.voice_client.loop)
                )  # 將聲音源播放至語音中
                return
            return
        if await isYoutubeVideo(path) == 1:
            await ctx.respond("Can't find the video")  # 如果找不到此影片，顯示此訊息
            return
        if os.path.isfile(f"./sounds/{path}"):
            source = FFmpegOpusAudio(f"./sounds/{path}")  # 利用FFmpeg產生聲音源
            ctx.voice_client.play(source)  # 將聲音源播放至語音中
            await ctx.respond("played")
            return
        await ctx.respond("This is not a URL or FileName")

    @discord.slash_command(description="停止播放")
    async def stop(self, ctx):  # 停止播放
        global nowPlaying
        global musicPlaylist
        if ctx.voice_client:
            musicPlaylist.clear()  # 清空播放清單
            ctx.voice_client.stop()  # 停止播放
            await ctx.respond("stopped")
            return
        await ctx.respond("Not playing music")

    @discord.slash_command(description="暫停播放")
    async def pause(self, ctx):  # 暫停播放
        if ctx.voice_client:
            ctx.voice_client.pause()
            await ctx.respond("paused")
            return
        await ctx.respond("Not playing music")

    @discord.slash_command(description="繼續撥放")
    async def resume(self, ctx):  # 回復播放
        if ctx.voice_client:
            ctx.voice_client.resume()
            ctx.respond("resumed")
            return
        ctx.respond("Not playing music")

    @discord.slash_command(description="離開語音頻道")
    async def leave(self, ctx):  # 離開語音頻道
        global musicPlaylist
        musicPlaylist.clear()  # 清空播放清單
        await ctx.voice_client.disconnect()  # 離開語音頻道
        await ctx.respond("left")

    @discord.slash_command(description="下一首")
    async def next(self, ctx):  # 下一首
        if ctx.voice_client:
            ctx.voice_client.stop()  # 停止播放當下的聲音源
            await ctx.respond("next")
            return
        await ctx.respond("Not playing music")

    @discord.slash_command(description="展示播放清單")
    async def playlist(self, ctx):  # 顯示播放清單
        global nowPlaying
        global musicPlaylist
        if nowPlaying:
            playlistStr = f"```Now. {nowPlaying.title} \n"  # 當下播放的影片名稱
            for i in range(len(musicPlaylist)):
                playlistStr += (
                    f"{i+1}. {musicPlaylist[i].title} \n"  # 播放清單中的影片名稱
                )
            playlistStr += "```"
            await ctx.respond(playlistStr)  # 將上述結合，一起回傳
        else:
            await ctx.respond("```Empty```")  # 如果播放清單為空，顯示此訊息

    @discord.slash_command(description="ni...?")
    async def nika(self, ctx):
        voice = ctx.author.voice
        if not ctx.voice_client:
            await voice.channel.connect()
        source = FFmpegOpusAudio(f"./sounds/nika.mp3")  # 利用FFmpeg產生聲音源
        image = discord.File("./images/nika.gif")
        await ctx.respond(file=image)
        ctx.voice_client.play(
            source, after=lambda _: asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), ctx.voice_client.loop)
        )  # 將聲音源播放至語音中


async def getYoutubeSource(video):  # 取得mp3檔案   #建立Youtube物件
    if video.check_availability():  # 確認是否可存取影片
        return 0
    video.streams.filter().get_audio_only().download(
        output_path="./sounds", filename="temp.mp3"
    )  # 下載影片mp3音檔
    return 1


async def isYoutubeVideo(url):  # 確認是否為Youtube影片
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)  # 建立Youtube物件
    except:
        return 0  # 如果無法建立代表url不是網址
    else:
        if yt.check_availability() == None:
            return 2  # 可存取
        return 1  # 不可存取


async def playNext(ctx):  # 播放程式
    global nowPlaying
    if len(musicPlaylist) >= 1:  # 如果播放清單有影片
        nowPlaying = musicPlaylist.pop(0)  # 取出播放清單第一首
        await getYoutubeSource(nowPlaying)  # 下載mp3檔案
        source = FFmpegOpusAudio(f"./sounds/temp.mp3")  # 利用FFmpeg產生聲音源
        ctx.voice_client.play(
            source, after=lambda _: asyncio.run_coroutine_threadsafe(playNext(ctx), ctx.voice_client.loop)
        )  # 將聲音源播放至語音中，播放完畢時重新執行此函式
        return
    nowPlaying = False  # 如果播放清單已空，清除現在播放的網址
    ctx.send("Playlist is empty. Leaving voice channel")
    await ctx.voice_client.disconnect()  # 離開語音頻道





def setup(bot):
    bot.add_cog(voice(bot))

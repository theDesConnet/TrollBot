import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import os
import youtube_dl

prefix = '>'

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print('Бот готов к издевательсву над другими людьми (C0d9d by DesConnet)')

@client.command(pass_content=True)

async def whoami(ctx):
    await ctx.send('Тебе это не обязательно знать')


@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@client.command()
async def leave(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()

@client.command(pass_content=True)
async def tts(ctx,*args):
    mess = ' '.join(args)
    await ctx.send(mess,tts=True)

@client.command(pass_content=True)
async def spam(ctx,*args):
    mess = ' '.join(args)
    num = 1
    while num < 10:
        await ctx.send(mess,tts=True)

@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

client.run('NjA2NDU1MTI4NjA1ODUxNjYx.XzveeQ.8tJefpCnHLeao1ZYVMzqF9Ty-6o', bot=False)

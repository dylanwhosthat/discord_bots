import discord
from discord.ext import commands, tasks
import os
import youtube_dl
import asyncio

import ytdl
from ytdl import YTDLSource

# Get API token
TOKEN = os.getenv("token")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        
        # Remove file after bot leaves
        try:
            path = os.listdir(os.getenv('file_path'))
            print(path)
            for item in path:
                if item.endswith(".webm"):
                    print(item)
                    os.remove(os.path.join(os.getenv('file_path'), item))
        except:
            print("Error deleting files")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                video_title = await YTDLSource.get_title(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegOpusAudio(executable='ffmpeg', source=(os.getenv('file_path') + filename)))
            await ctx.send('**Now Playing:** {}'.format(video_title))
    else:
        print("Bot is not connected to channel.")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything currently.")

@bot.command(name='resume', help='This command resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything. Use /play.")


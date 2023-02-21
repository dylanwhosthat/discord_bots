import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl
import asyncio

import ytdl
from bots import bot

load_dotenv()

TOKEN = os.getenv("token")
if __name__ =="__main__":
    bot.run(TOKEN)

import yt_dlp as youtube_dl
import asyncio
import discord
import lxml
from lxml import etree 
import urllib.request

# Supresses noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True, 
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url= data.get('url')

    # Downloads link and returns downloaded file name 
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() # Gets current event loop
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries'in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return filename

    # Gets and returns video title
    @classmethod
    async def get_title(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() # Gets current event loop
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        video_title = data['title']

        return video_title

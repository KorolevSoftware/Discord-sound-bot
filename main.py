import asyncio

from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get
from discord import VoiceClient, FFmpegOpusAudio
from discord_components import DiscordComponents, ComponentsBot, Button, Interaction, ButtonStyle
import yt_dlp
import glob
from os import walk, rmdir
from FileQueueByTime import *

file_queue = FileQueueByTime()
bot = commands.Bot(command_prefix="!")
voice: VoiceClient = None
DiscordComponents(bot)

@bot.event
async def on_ready():
    print("on_ready")


@bot.command()
async def button(ctx: Interaction):
    await ctx.send(
        "Hello, World!",
        components=[[
            Button(label="Back", custom_id="back"),
            Button(label="Stop", custom_id="stop"),
            Button(label="Next", custom_id="next"),
        ]
        ]
    )


@bot.event
async def on_button_click(interaction: Interaction):
    global file_queue
    if interaction.custom_id == "next":
        play_sound(None)

    if interaction.custom_id == "back":
        file_queue.last()
        play_sound(None)
    await interaction.message.edit(
        components=[[
            Button(label="Back", custom_id="back"),
            Button(label="Play", custom_id="play"),
            Button(label="Next", custom_id="button3"),
        ]
        ])
    await interaction.send(content="Button Clicked", delete_after=1, ephemeral=False)



def play_sound(error):
    if error:
        return
    global voice, file_queue
    current_track = file_queue.next()
    if not current_track or voice == None:
        return
    print(current_track)
    voice.stop()
    voice.play(FFmpegOpusAudio(current_track), after=play_sound)


@bot.command()
async def leave(ctx: Context):
    global voice
    voice.stop()
    await voice.disconnect()
    voice = None
    await asyncio.sleep(3)
    files = glob.glob('sounds/*')
    for f in files:
        os.remove(f)


@bot.command()
async def play(ctx: Context, url: str):
    global voice, file_queue
    # Check connect to voice chat
    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        voiceChannel = ctx.author.voice.channel
        voice = await voiceChannel.connect()
    # Youtube setting
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '256',
        }],
        'outtmpl': "sounds" + '/%(title)s.%(ext)s',
        'nooverwrites': True
    }
    # Download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        file_queue.scan("sounds")
        if not voice.is_playing():
            play_sound(None)


if __name__ == "__main__":
    bot.run("ODg4ODUyMjc3Nzk5MDU1NDEw.YUYuMQ.S0_A_3jvOcdxjf0QgdOzAm7oMCI")

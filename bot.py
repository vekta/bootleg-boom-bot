import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import asyncio

TOKEN = 'MTEzOTA0Mzc5ODQ3NTg4NjcwMw.GvEPCS.5PJFTLW5C481m9q5x6q0IK3EFQE2b2khkCR4OU'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

FFMPEG_PATH = "ffmpeg\\bin\\ffmpeg.exe"

# The song queues for each server
song_queues = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the bot left a voice channel
    if before.channel and not after.channel and member == bot.user:
        # Delete the downloaded files
        for file in os.listdir(DOWNLOAD_FOLDER):
            os.remove(os.path.join(DOWNLOAD_FOLDER, file))

def play_next(ctx):
    """Play the next song in the queue, if available."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice and not voice.is_playing():
        if not song_queues.get(ctx.guild.id):  # If no more songs in the queue
            asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), bot.loop)
        else:
            url = song_queues[ctx.guild.id].pop(0)
            play_song(ctx, url)


def play_song(ctx, url_or_query):
    """Play a song from the provided URL or search query."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'extract-audio': True,
        'audio-format': 'mp3'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_or_query, download=True)
            
            # Check if 'entries' key exists in the info dictionary (which indicates it's a search result)
            if 'entries' in info:
                info = info['entries'][0]  # Take the first search result
                # Notify the chat about the found video
                asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {info['title']}"), bot.loop)
            
            file_name = ydl.prepare_filename(info)
            
        except youtube_dl.utils.DownloadError:
            try:
                # If the initial URL extraction fails, search YouTube for the query
                info = ydl.extract_info(f"ytsearch:{url_or_query}", download=True)
                
                # Again, check for 'entries' key and update info if necessary
                if 'entries' in info:
                    info = info['entries'][0]
                    # Notify the chat about the found video
                    asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {info['title']}"), bot.loop)
                
                file_name = ydl.prepare_filename(info)
                
            except youtube_dl.utils.DownloadError as e:
                asyncio.run_coroutine_threadsafe(ctx.send(f"Error: {str(e)}"), bot.loop)
                return
    
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=file_name), after=lambda x: play_next(ctx))

@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if not voice:
            await channel.connect()
            play_song(ctx, query)
        else:
            if not song_queues.get(ctx.guild.id):
                song_queues[ctx.guild.id] = []
            song_queues[ctx.guild.id].append(query)
            await ctx.send(f"Song added to the queue! Position: {len(song_queues[ctx.guild.id])}")
    else:
        await ctx.send("You are not connected to a voice channel!")


@bot.command()
async def skip(ctx):
    """Skip the currently playing song."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice.is_playing() or voice.is_paused():
        voice.stop()
        await ctx.send("Skipped the current song.")
    else:
        await ctx.send("No song is currently playing.")


@bot.command()
async def list(ctx):
    """List all songs in the queue."""
    queue = song_queues.get(ctx.guild.id)
    
    if not queue:
        await ctx.send("The song queue is currently empty!")
        return
    
    msg = "Songs in the queue:\n"
    for idx, song_url in enumerate(queue, 1):
        msg += f"{idx}. {song_url}\n"
    await ctx.send(msg)


@bot.command()
async def remove(ctx, position: int):
    """Remove a song from the queue at the specified position."""
    queue = song_queues.get(ctx.guild.id)
    
    if not queue:
        await ctx.send("The song queue is currently empty!")
        return

    if position < 1 or position > len(queue):
        await ctx.send(f"Invalid position! Please choose a number between 1 and {len(queue)}.")
        return

    removed_url = queue.pop(position - 1)  # Adjust for 0-based index
    await ctx.send(f"Removed {removed_url} from the queue.")


@bot.command()
async def clear(ctx):
    """Clear all songs from the queue."""
    song_queues[ctx.guild.id] = []
    await ctx.send("Cleared the song queue.")


@bot.command()
async def help(ctx):
    """Display available commands."""
    commands_list = [
        "💀 Sean's Bootleg Boom Bot Commands 💀",
        "",
        "```!play [youtube_url or search term] - Play a song from the given YouTube URL or search term.```",
        "```!list - List all songs in the queue.```",
        "```!remove [position] - Remove a song from the queue at the specified position.```",
        "```!clear - Clear all songs from the queue.```",
        "```!skip - Skip the currently playing song.```",
        "```!pause - Pause the currently playing song.```",
        "```!unpause - Unpause the song.```",
        "```!help - Display this message.```"
    ]
    await ctx.send("\n".join(commands_list))


@bot.command()
async def pause(ctx):
    """Pause the currently playing song."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused the song.")
    else:
        await ctx.send("No song is playing.")


@bot.command()
async def unpause(ctx):
    """Unpause the song."""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resumed the song.")
    else:
        await ctx.send("The song is not paused.")

bot.run(TOKEN)

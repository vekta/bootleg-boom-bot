
# 💀 Bootleg Boom Bot

This bot allows users to play music from YouTube directly into Discord voice channels. It supports a variety of commands, including play, pause, skip, and queue management.

## Features

- Play music from a YouTube URL or search term.
- Queue songs to play them one after another.
- View, manage, and clear the song queue.
- Pause, unpause, and skip songs.
- Automatic deletion of downloaded audio files after playback.

## Commands

- `!play [YouTube URL or search term]` - Plays the audio from the provided YouTube URL or searches YouTube and plays the top result.
- `!pause` - Pauses the currently playing song.
- `!unpause` - Resumes the paused song.
- `!skip` - Skips the currently playing song.
- `!list` - Lists the songs in the queue.
- `!remove [number]` - Removes a song from the queue.
- `!clear` - Clears the song queue.

## Installation

### Dependencies

The bot depends on several Python libraries and tools:

- `discord.py` - The main library to interact with Discord.
- `yt-dlp` - A tool for downloading and extracting video and audio from YouTube.
- `ffmpeg` - A software suite to handle multimedia data.

### Steps to Install Dependencies

#### Python Libraries

Use pip to install the required Python libraries:

```bash
pip install discord.py yt-dlp
```

#### FFmpeg

- **General**: Replace the `ffmpeg` executable located in the `/ffmpeg` directory with the one appropriate for your operating system.

- **Windows**:
  - Download FFmpeg from the official website.
  - Extract the zip file and replace the `ffmpeg.exe` in the `/ffmpeg` directory with the one you downloaded.

- **Linux**:

```bash
sudo apt update
sudo apt install ffmpeg
```

Copy the `ffmpeg` binary to the `/ffmpeg` directory of the bot.

- **MacOS (using Homebrew)**:

```bash
brew install ffmpeg
```

Copy the `ffmpeg` binary to the `/ffmpeg` directory of the bot.

### Running the Bot

- Replace `YOUR_TOKEN_HERE` in the script with your Discord bot token.
  
- Run the bot script:

```bash
python bot.py
```

- Invite the bot to your server and join a voice channel.

- Use any of the commands listed above to interact with the bot and play music.

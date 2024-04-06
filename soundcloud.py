import yt_dlp as youtube_dl
import argparse


def get(s: str):
    options = {
        'format': 'bestaudio',
        # "quiet": True,
        'keepvideo': False,
        'prefer_ffmpeg': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        filename = ydl.extract_info(s)["requested_downloads"][0]["_filename"]
        filename = ".".join(filename.split(".")[:-1]) + ".mp3"
    options = {
        'format': 'bestaudio',
        # "quiet": True,
        'keepvideo': False,
        'outtmpl': filename,
        'prefer_ffmpeg': True,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(s)
    return filename


print(get("https://www.tiktok.com/t/ZTLSyRNT9/"))

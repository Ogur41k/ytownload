import subprocess
import argparse


def video(url: str) -> str:
    try:
        if "you" in url:
            s = subprocess.check_output(
                ["yt-dlp", "-f", "bestaudio+bestvideo", "--merge-output-format", "mp4", "--no-part", "--print",
                 "filename",
                 "--no-simulate", "--no-warnings",
                 url]).decode("utf-8")
            return ".".join(s.split("\n")[0].split(".")[:-1]) + ".mp4"
        else:
            s = subprocess.check_output(
                ["yt-dlp", "-f", "best", "--merge-output-format", "mp4", "--no-part", "--print", "filename",
                 "--no-simulate", "--no-warnings",
                 url]).decode("utf-8")
            return ".".join(s.split("\n")[0].split(".")[:-1]) + ".mp4"
    except:
        return "404"


def audio(url: str) -> str:
    try:
        s = subprocess.check_output(
            ["yt-dlp", "-x", "-f", "bestaudio", "--audio-format", "mp3", "--print", "filename", "--no-simulate",
             "--no-warnings",
             url]).decode("utf-8")
        return ".".join(s.split("\n")[0].split(".")[:-1]) + ".mp3"
    except:
        return "404"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("format")
    parser.add_argument("url")
    args = parser.parse_args()
    print(audio(args.url) if args.format == "mp3" else video(args.url))

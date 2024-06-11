import asyncio


async def video(url: str) -> str:
    try:
        if "you" in url:
            proc = await asyncio.create_subprocess_exec("yt-dlp", "-f", "bestaudio+bestvideo",
                                                        "--merge-output-format", "mp4", "--no-part", "--print",
                                                        "filename",
                                                        "--no-simulate", "--no-warnings",
                                                        url, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            return ".".join(stdout.decode().split("\n")[0].split(".")[:-1]) + ".mp4"
        else:
            proc = await asyncio.create_subprocess_exec("yt-dlp", "-f", "best", "--merge-output-format", "mp4",
                                                        "--no-part", "--print", "filename",
                                                        "--no-simulate", "--no-warnings",
                                                        url, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            return ".".join(stdout.decode().split("\n")[0].split(".")[:-1]) + ".mp4"
    except:
        return "404"


async def audio(url: str) -> str:
    try:
        proc = await asyncio.create_subprocess_exec("yt-dlp", "-x", "-f", "bestaudio", "--audio-format", "mp3",
                                                    "--print", "filename", "--no-simulate",
                                                    "--no-warnings",
                                                    url, stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        return ".".join(stdout.decode().split("\n")[0].split(".")[:-1]) + ".mp3"
    except:
        return "404"

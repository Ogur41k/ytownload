from aiogram import Bot, Dispatcher, executor, types
import os
import yt_dlp as youtube_dl
import DB


async def get(s: str):
    options = {
        'format': 'bestaudio/best',
        "quiet": True,
        'keepvideo': False,
        'prefer_ffmpeg': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        filename = ydl.extract_info(s)["requested_downloads"][0]["_filename"]
        filename = ".".join(filename.split(".")[:-1]) + ".mp3"
    options = {
        'format': 'bestaudio',
        "quiet": True,
        'keepvideo': False,
        'outtmpl': filename,
        'prefer_ffmpeg': True,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(s)
    return filename

API_TOKEN = "6129793474:AAEFl_nY33P9wj8jXZnniZxzqnomiwH6Ma4"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
bd = DB.DataBase()


async def unsub(message: types.Message):
    channels = ["https://t.me/endelneuro"]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[types.InlineKeyboardButton("Наш канал", url=url) for url in channels])
    await message.answer("Подпишитесь на наши каналы чтобы пользоваться ботом", reply_markup=keyboard)


async def check(message):
    channel_ids = [-1001950205471]
    sub = []
    for my_channel_id in channel_ids:
        user = await bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id)
        tmp = []
        for i in [types.ChatMemberMember, types.ChatMemberAdministrator, types.ChatMemberOwner]:
            tmp.append(isinstance(user, i))
        sub.append(any(tmp))
    return all(sub)


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer(
        "Hey 👋🏻 I will help you here to download any types of media: music. videos or movies in the best quality. Just send me the link to SoundCloud,  YouTube etc. ")


@dp.message_handler()
async def text_handler(message: types.Message):
    me = await bot.get_me()
    bd.add(message.text, message.from_user.username, str(message.chat.id), me.username)
    if not await check(message):
        await unsub(message)
        return 1
    if "soundcloud.com" in message.text:
        audio = await get("".join(message.text.split("?")[0]))
        with open(audio, mode="rb") as file:
            await bot.send_audio(message.chat.id, file)
        os.remove(audio)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import tl, dl
import DB

vocab_s_i = {"Дом": 1}
vocab_i_s = {1: "Дом"}


def vocab(a):
    if a.isnumeric():
        return vocab_i_s[int(a)]
    if a in vocab_s_i:
        return vocab_s_i[a]
    else:
        t = max(vocab_s_i.values()) + 1
        vocab_s_i[a] = t
        vocab_i_s[t] = a
        return t


API_TOKEN = "6129793474:AAEnQD7jNt5O2okuRRwz2yyjHO1-Km_eDOQ"

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


@dp.message_handler(content_types=['document', "audio", "video"])
async def text_handler1(message: types.Message):
    if message.from_user.username in ["Ogur41kkk"]:
        await bot.copy_message(int(message.caption), message.chat.id, message.message_id, caption="")


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Русский", callback_data=f"lang {message.from_user.username} Русский"))
    markup.add(InlineKeyboardButton("English", callback_data=f"lang {message.from_user.username} English"))
    await message.answer(
        "Выберите язык", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith("lang"))
async def process_callback2(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    _, user, lang = vocab(callback_query.data).split()
    bd.add_lang(user, lang)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Привет 👋🏻  Я помогу скачать тебе почти все что угодно: музыку, видео и фильмы в лучшем качестве! Вставь ссылку из Soundcloud, YouTube и тд" if lang == "Русский" else "Hey 👋🏻 I will help you here to download any types of media: music. videos or movies in the best quality. Just send me the link to SoundCloud,  YouTube etc")


@dp.callback_query_handler(lambda c: vocab(c.data).startswith("a"))
async def process_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    print(vocab(callback_query.data))
    await bot.edit_message_text(text="Подождите пожалуйста", chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)
    audio = dl.audio(vocab(callback_query.data).replace("a ", ""))
    print(audio)
    with open(audio, mode="rb") as file:
        await bot.send_audio(chat_id=callback_query.message.chat.id, audio=file)
    os.remove(audio)
    await bot.edit_message_text(text="Спасибо за использование бота", chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: vocab(c.data).startswith("v"))
async def process_callback1(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    print(vocab(callback_query.data))
    await bot.edit_message_text(text="Подождите пожалуйста", chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)

    video = dl.video(vocab(callback_query.data).replace("v ", ""))
    print(video)
    await tl.send(video, str(callback_query.from_user.id))
    os.remove(video)
    await bot.edit_message_text(text="Спасибо за использование бота", chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)


@dp.message_handler()
async def text_handler(message: types.Message):
    me = await bot.get_me()
    bd.add(message.text, message.from_user.username, str(message.chat.id), me.username)
    if not await check(message):
        await unsub(message)
        return 1
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("audio", callback_data=vocab(f"a {message.text}")))
    markup.add(InlineKeyboardButton("video", callback_data=vocab(f"v {message.text}")))
    await message.answer(
        "Выберите формат файла", reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

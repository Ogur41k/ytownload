from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

import settings
import tl, dl
import DB
import validators

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


API_TOKEN = settings.API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
bd = DB.DataBase()


async def unsub(message: types.Message):
    lang = bd.get_lang(message.from_user.id)
    channels = settings.channels
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if lang == "Русский":
        keyboard.add(*[types.InlineKeyboardButton("Наш канал", url=url) for url in channels])
        keyboard.add(InlineKeyboardButton("Я подписался", callback_data="sub"))
        await message.answer("Подпишитесь на наши каналы чтобы пользоваться ботом", reply_markup=keyboard)
    else:
        keyboard.add(*[types.InlineKeyboardButton("Our channel", url=url) for url in channels])
        keyboard.add(InlineKeyboardButton("Im subscribed", callback_data="sub"))
        await message.answer("Subscribe to our channels to use the bot", reply_markup=keyboard)


async def check(from_id):
    channel_ids = settings.channel_ids
    sub = []
    for my_channel_id in channel_ids:
        user = await bot.get_chat_member(chat_id=my_channel_id, user_id=from_id)
        tmp = []
        for i in [types.ChatMemberMember, types.ChatMemberOwner, types.ChatMemberAdministrator]:
            tmp.append(isinstance(user, i))
        sub.append(any(tmp))
    return all(sub)


@dp.message_handler(content_types=['document', "audio", "video"])
async def text_handler1(message: types.Message):
    if message.from_user.username in settings.senders:
        await bot.copy_message(int(message.caption), message.chat.id, message.message_id, caption="@downloadsome_bot")


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Русский 🇷🇺", callback_data=f"lang {message.from_user.id} Русский"))
    markup.add(InlineKeyboardButton("English 🇺🇸", callback_data=f"lang {message.from_user.id} English"))
    await message.answer(
        "Choice language", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith("lang"))
async def process_callback2(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    _, user, lang = callback_query.data.split()
    bd.add_lang(user, lang)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='''Привет 🍋 
Я помогу скачать тебе почти все что угодно: музыку, видео и фильмы в лучшем качестве! 

Вставь ссылку из Soundcloud, YouTube и тд 👇🏻''' if lang == "Русский" else """Hey 🍋 
I will help you here to download any types of media: music. videos or movies in the best quality. 

Just send me the link to SoundCloud,  YouTube etc 👇🏻""")


@dp.callback_query_handler(lambda c: c.data == "sub")
async def process_callback3(callback_query: types.CallbackQuery):
    lang = bd.get_lang(callback_query.from_user.id)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    if not await check(callback_query.from_user.id):
        await bot.edit_message_text(text="Вы не подписались" if lang == "Русский" else "You didn't subscribe",
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id)
        await unsub(callback_query.message)
        return 1
    await bot.edit_message_text(text="Спасибо за подписку" if lang == "Русский" else "Thanks 🙏 Now send a link here 👇🏻",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: vocab(c.data).startswith("a"))
async def process_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    lang = bd.get_lang(callback_query.from_user.id)
    await bot.edit_message_text(text="Подождите пожалуйста" if lang == "Русский" else "Please wait",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)
    audio = dl.audio(vocab(callback_query.data).replace("a ", ""))
    if audio == "404":
        await bot.edit_message_text(
            text="⚠️Возникла ошибка! Попробуйте ещё раз" if lang == "Русский" else "⚠️Oops! You sent incorrect link or choose incorrect format of file! Try again :)",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id)
    else:
        with open(audio, mode="rb") as file:
            await bot.send_audio(chat_id=callback_query.message.chat.id, audio=file,caption="@downloadsome_bot")
        os.remove(audio)
        await bot.edit_message_text(text="Спасибо за использование бота" if lang == "Русский" else "Thanks for using",
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: vocab(c.data).startswith("v"))
async def process_callback1(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None
    )
    lang = bd.get_lang(callback_query.from_user.id)
    await bot.edit_message_text(text="Подождите пожалуйста" if lang == "Русский" else "Please wait",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)

    video = dl.video(vocab(callback_query.data).replace("v ", ""))
    if video == "404":
        await bot.edit_message_text(
            text="⚠️Возникла ошибка! Попробуйте ещё раз" if lang == "Русский" else "⚠️Oops! You sent incorrect link or choose incorrect format of file! Try again :)",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id)
    else:
        await tl.send(video, str(callback_query.from_user.id))
        os.remove(video)
        await bot.edit_message_text(text="Спасибо за использование бота" if lang == "Русский" else "Thanks for using",
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id)


@dp.message_handler()
async def text_handler(message: types.Message):
    me = await bot.get_me()
    bd.add(message.text, message.from_user.username, str(message.chat.id), me.username)
    if not await check(message.from_user.id):
        await unsub(message)
        return 1
    lang = bd.get_lang(message.from_user.id)
    if validators.url(message.text):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("аудио" if lang == "Русский" else "audio", callback_data=vocab(f"a {message.text}")))
        markup.add(
            InlineKeyboardButton("видео" if lang == "Русский" else "video", callback_data=vocab(f"v {message.text}")))
        await message.answer(
            "Выберите формат файла" if lang == "Русский" else "Choice file format", reply_markup=markup)
    else:
        await message.answer("Неправильная ссылка" if lang == "Русский" else "Invalid url")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

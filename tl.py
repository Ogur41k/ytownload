from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = 23614670
api_hash = 'ef3635ffeccc884bc5b7c9422fb2cc86'
str_ses = '1ApWapzMBu6gmcf6thOkJ89CShAiIRzCWsz4zCi3U03V5tZi-U6_dmznX5ytbiuI-ENd-hGGU9-xYttRY0wIQ1JGXOkGu1uHLwlWzisOkS5YA44-hs8MKJwgkHZZXxfpUkDG6U2hVsmmrNgllnR76T80MYFXehlAb6Oy7nOgrB-B4Fm2vkDMs3bfXNz-0uKV0fjxvQpdyOfqxwnEm68MtHt0iKrqromkzFvmUiZQbC_eJUTxwZseRfUz6Cn2sMG66AF01rpI3lk0G3r5jVRMqCLt7f_eCb4w1D4OlN9CkcaULnGI_MwU65ED1mD7iXXgU-06YH9XluesUI6EF7CV-Ceb9dKAwgtU='

client = TelegramClient(StringSession(str_ses), api_id, api_hash)
client.start()


# date = datetime.datetime(2023, 12, 31, 14, 23, 25, tzinfo=datetime.timezone.utc)
# print(date)
# date =date.replace(minute=date.minute + 1)


# @client.on(events.NewMessage())
# async def handler(message):
#     text = message.message.message.split()
#     chat_id, filename = text
#     filename = "1.mp4"
#     await client.send_file("https://t.me/ytownloadbot", filename, caption=chat_id)

# @client.on(events.NewMessage())
async def send(filename: str, chat_id: str):
    await client.send_file("ytownloadbot", filename, caption=chat_id)


# client.loop.run_until_complete(send("1.mp4", "1150663089"))

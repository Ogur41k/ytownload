from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 20223832
api_hash = '88d449664b91a918ddd9647b072f95e9'
str_ses = '1ApWapzMBuwicbT8UbVI_uScybsNgYeYXsMs7hWDL-4ymW8EoFvWhhZq36XYVcDIB-JZqewTRSWeZbE87PjK1n0XiXYCKa7ADtdxTAcxlsY3QkhcB22rM52LHkFIG_9G_AA8oYo9VNpMg3rAHBKlB-Gji9Ame2m7IbdaICYH3GmQKV00AdRPU3xcVZR_VK8IeGmlVoJriAGOFqqVBpj2iuzEaMwYRhoV-GQ9hoM6xqp1Uq7buBzf6HEfh90VseHT-JnY_WBb0QLwbucxHEGrDOVVxL-p57j1xt-Beklqv28WgWK0uiXoD8pXcU7eQOwvR2-FAuTfsgtEzutCZ9jaEAiVyAzcZvwA='

client = TelegramClient(StringSession(str_ses), api_id, api_hash)
client.start()


async def send(filename: str, chat_id: str):
    await client.send_file("ytownloadbot", filename, caption=chat_id)

from urllib.parse import quote
from cloudscraper import create_scraper
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, DOMAIN1, API2, DOMAIN2, API2
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        await first_message.reply("Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
        continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        await second_message.reply("Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
        continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    short1 = short(link, DOMAIN1, API1)
    short2 = short(link, DOMAIN2, API2)
    await channel_message.reply_text(
        f"<b>Here is your link</b>\n\noriginal link: <code>{link}</code>\n\nfirst short link: <code>{short1}</code>\n\nsecond short link: <code>{short2}</code>",
        quote=True)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        await channel_message.reply("Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
        continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    short1 = short(link, DOMAIN1, API1)
    short2 = short(link, DOMAIN2, API2)
    await channel_message.reply_text(
        f"<b>Here is your link</b>\n\noriginal link: <code>{link}</code>\n\nfirst short link: <code>{short1}</code>\n\nsecond short link: <code>{short2}</code>",
        quote=True)

def short(longurl, a, b):
    try:
        res = create_scraper().get(f'https://{a}/api?api={b}&url={quote(longurl)}').json()
        return res['shortenedUrl']
    except Exception as e:
        return longurl

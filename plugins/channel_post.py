import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from urllib.parse import quote
from cloudscraper import create_scraper

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, DOMAIN1, API1, DOMAIN2, API2
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    short1 = short(link, DOMAIN1, API1)
    short2 = short(link, DOMAIN2, API2)

    await reply_text.edit(
        f"<b>Here is your link</b>\n\noriginal link:\n<blockquote><code>{link}</code></blockquote>\n\nfirst short link:\n<blockquote><code>{short1}</code></blockquote>\n\nsecond short link:\n<blockquote><code>{short2}</code></blockquote>")

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


"""
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
"""


def short(longurl, a, b):
    try:
        res = create_scraper().get(f'https://{a}/api?api={b}&url={quote(longurl)}').json()
        return res['shortenedUrl']
    except Exception as e:
        return longurl
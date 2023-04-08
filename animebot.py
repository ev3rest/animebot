import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import ChatActions
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ParseMode, InlineQuery, InlineQueryResultPhoto
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.executor import start_webhook
import aiohttp
from pybooru import Moebooru, Danbooru
import traceback
from uuid import uuid4
import re
import random
import urllib.request
import os
from random import randint
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
import aiosqlite
from collections import namedtuple
from aiogram.utils.markdown import escape_md
from io import BytesIO

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''
lastcmd = {}
# Replace the allowed_users list with the user IDs that are allowed to execute the restricted commands
allowed_users = [47571378]

# Replace the restricted_commands list with the commands that should be restricted
restricted_commands = ["users", "popular"]


class ImageCache:
    def __init__(self):
        self.cache = {}

    def get(self, channel_id: str) -> dict[str, any]:
        return self.cache.setdefault(channel_id, {'url': [], 'id': [], 'tags': []})

    def remove_first(self, channel_id: str):
        try:
            data = self.get(channel_id)
            data['url'].pop(0)
            data['id'].pop(0)
        except:
            traceback.print_exc()


# ----------------------------------
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = 'https://dev.ev3.me'
WEBHOOK_PATH = '/bot/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3009
# ----------------------------------

stickers = ['CAADBAADJgMAAqKYZgAB0UH2shlpMSsC', 'CAADBAADLAMAAqKYZgABayywIAiqZ0gC', 'CAADBAADOAMAAqKYZgABh5wcd4QnpcwC',
            'CAADBAADPQMAAqKYZgABur46JrhDohYC', 'CAADBAADswMAAqKYZgABVzxxH4lMba0C', 'CAADBAAD3gQAAqKYZgABmxmc1Y3A4xQC',
            'CAADBAADWAUAAqKYZgAB1ia7fuNxpq4C', 'CAADBAADXA4AAh3PuAc4x8-E_-7aygI', 'CAADBAADeg4AAh3PuAe2kQ3GPRO3hwI',
            'CAADBAADkg4AAh3PuAcj4B3CTwjDiQI', 'CAADBAADiwIAAsiLDQhiubnq7ueZrgI', 'CAADBAADmQIAAsiLDQgLP7VMIuZXgAI',
            'CAADBAADmwIAAsiLDQiPkeWZT0jKPQI', 'CAADBAADlQIAAsiLDQhcIu-tSCjcBQI', 'CAADBAADjwIAAsiLDQjYx7KvqxKFMgI',
            'CAADBAADnwIAAsiLDQibN_CcD5zfkQI', 'CAADBAADnQIAAsiLDQihvo41EnrDzAI', 'CAADBAADpQIAAsiLDQjK923PGHm5QQI',
            'CAADBAADowIAAsiLDQgvfkwYeEQ-2QI', 'CAADBAADpwIAAsiLDQizmtsoKxTPggI', 'CAADBAADrQIAAsiLDQgMCsrjsg3v4wI',
            'CAADBAADrwIAAsiLDQjIXFtjd_TqNAI', 'CAADBAADtwIAAsiLDQiBcvZcIdSJGgI', 'CAADBAADsQIAAsiLDQhLpnmM589abAI',
            'CAADBAAD0QIAAsiLDQhh8fBJJVLT8QI', 'CAADBAAD0wIAAsiLDQgkmlDTS1nm7QI', 'CAADBAAD1wIAAsiLDQgNRH763A4EjgI',
            'CAADAQADoQEAArna9gmuB8gVICvS9wI', 'CAADAQADqQEAArna9gnqCzMdDF0lUAI', 'CAADAQADrQEAArna9glHGcsWYKiMRAI',
            'CAADAQADqwEAArna9gkmp05lNiNn9wI', 'CAADAQADtwEAArna9gkDeV746IbSwQI', 'CAADAQADvQEAArna9gnuMPtOZrW1PQI',
            'CAADAQADvwEAArna9glCn8R5s1LbZAI', 'CAADBAADJgEAAqM2qAemZ_YJbuzDJwI', 'CAADBAADOQEAAqM2qAfkrc477ntjIgI',
            'CAADBAADMAEAAqM2qAeX7j7nLeiNFQI', 'CAADBAADVAEAAqM2qAd0tDCJZ3A8ggI', 'CAADBAADUQEAAqM2qAdbGe9WG9EogQI',
            'CAADBAADTAEAAqM2qAd-3A6X_ijf1wI', 'CAADBAADSAEAAqM2qAcAAUws3DcwQdIC', 'CAADBAADRgEAAqM2qAdssyA7IPhymQI',
            'CAADBAADVgEAAqM2qAeDuMRxavg-9gI', 'CAADBAADhAADDvcmBlTiJw2iW3-DAg', 'CAADBAADhgADDvcmBhTDcsXEcO8RAg',
            'CAADBAADiAADDvcmBmtco0ch3eYmAg', 'CAADBAADigADDvcmBsN4in4FXW4aAg', 'CAADBAADoQADDvcmBn7hBgmWUK1xAg',
            'CAADBAADrQADDvcmBpQJ1c4eo8SaAg', 'CAADBAADxQQAAsOSbAP7HMKduOaRDAI', 'CAADBAAD0QQAAsOSbAPzeE-N7Wo1XAI',
            'CAADBAAD1wQAAsOSbAMUAabgPzSUxAI', 'CAADBAAD2QQAAsOSbAM5-ZiM9NwCYQI', 'CAADBAAD3wQAAsOSbAN8cWh9AAGZ4JEC',
            'CAADBAAD7QQAAsOSbAP87mq-1IhdVAI', 'CAADBAADngUAAsOSbAPyZJxHHwABDOsC', 'CAADBAADuwUAAsOSbAPVCu6yVd9AYgI',
            'CAADBAADTwEAAqIkSQOcLYaijPdA9AI', 'CAADBAADewEAAqIkSQOKtlOA7PDVswI', 'CAADBAADfwEAAqIkSQMwmItrQLEAAbQC',
            'CAADBAADigEAAqIkSQNNtoHkx9ztAQI', 'CAADBAADkAEAAqIkSQMLvYm2Z-WYYgI', 'CAADBAADmAEAAqIkSQP6IpIzeuoqdQI',
            'CAADBAADmgEAAqIkSQPznG-Ig4iwAQI', 'CAADBAADogEAAqIkSQMs3FfHKdWVzAI', 'CAADBAADqAEAAqIkSQPH-RWOk7OuDQI',
            'CAADBAADtgEAAqIkSQNaxXsO6qI36gI', 'CAADBAADvwEAAqIkSQOeSXUAAS1PnwsC', 'CAADBAAD8AEAAqIkSQOYAAF3LuxtgicC',
            'CAADBAAD_AEAAqIkSQNHqmcGA9vgeAI', 'CAADBAAD8gEAAqIkSQMqnIXPK9AO4AI', 'CAADBAAD-AEAAqIkSQOST8xeeqZZ_QI',
            'CAADBAADyAUAAuAFHALE9DV1idj8GQI', 'CAADBAAD0AUAAuAFHAKKqQlswE-TxAI', 'CAADBAAD7gUAAuAFHAJt4SYHShUyHQI',
            'CAADBAAD1gUAAuAFHALWRdze8hSGgAI', 'CAADBQADYgAD6NvJAjw6mwsi3ZDcAg', 'CAADBQADawAD6NvJAvSDRGZiKm0-Ag',
            'CAADBAADawYAApesNQABqnPuHOSm_rUC', 'CAADBAADggYAApesNQABY52p_5jYmDAC', 'CAADBAADkgYAApesNQABrWxxAo4i5YIC',
            'CAADBAADlgYAApesNQABAaQoqR18rJcC', 'CAADBAADwAYAApesNQABj-Un4Rf2kAEC', 'CAADBAADpgMAApv7sgABKyxNf3LVHeAC',
            'CAADBAADtAMAApv7sgAB-1esnD-WlHIC', 'CAADBAAD7gMAApv7sgABGCZKqVeej3YC', 'CAADAwADhAAD_ZPKAAGphJ9IUmjqqAI',
            'CAADAgADsgADdqy6ButIWEMMsnSMAg', 'CAADAQADygMAAuJbQAVEJd8sOLqNJwI', 'CAADAQADyAMAAuJbQAU-y13TznSWXwI',
            'CAADAQAD1AMAAuJbQAXPlcSmhmgxOgI', 'CAADBAADfQADylycBfFLFOlpUkSAAg', 'CAADBAADfwADylycBerATexgP5rfAg',
            'CAADBAADgQADylycBRxpx-hgT8dBAg', 'CAADBAADgwADylycBapS4Fz1ozG4Ag', 'CAADBAADhwADylycBUXx92Qbc0HeAg',
            'CAADBAADogADylycBWLXUovOwXa6Ag', 'CAADBAAD3gADylycBS0QiC-O4zvYAg', 'CAADBAADDAUAAspcnAU4aO3nT9quMAI',
            'CAADBAADHgUAAspcnAVLCx1VIZ2laQI', 'CAADBAADOAUAAspcnAV7Wx41DCZINwI', 'CAADBAADaQEAAl7ugQYqaKHrgmb7mgI',
            'CAADBAADOQQAAnZY-wJXL61k-or-uwI', 'CAADBAADQgQAAnZY-wJ2XZvSz11GhQI', 'CAADBAADTgQAAnZY-wK6b_dynGPoTAI',
            'CAADBAADlwMAAspcnAWOVBRIBv3K7QI', 'CAADBAADmwMAAspcnAVYLJLwdXI4twI', 'CAADBAADvwMAAspcnAXh31MvOjw4_wI',
            'CAADBAAD-QMAAspcnAU7QO_IByh3UQI', 'CAADBAAD5QMAAspcnAW5Pl-29Mre9gI', 'CAADBAADBwQAAspcnAUaKvx4Bb99kQI',
            'CAADBAADQwQAAspcnAW3qRleNi9aNQI', 'CAADBAADxQwAAuf7rQZlyZi2n5t29QI', 'CAADBAADzwwAAuf7rQZMLO8dV3dzTAI',
            'CAADBAAD1wwAAuf7rQZvaEDPm8950gI', 'CAADBAAD0wwAAuf7rQZat80CHwABEtcC', 'CAADBAAD0QwAAuf7rQa1vDSzF2iXDAI',
            'CAADBAAD3wwAAuf7rQYE4k-pmuUnIQI', 'CAADBAADYA0AAuf7rQabM1fOJ2yZ1wI', 'CAADBAADYw4AAuf7rQYZUvpBdCk2pgI',
            'CAADBAADhg4AAuf7rQbJl5Bat1xMsgI', 'CAADBAADiA4AAuf7rQb2C3BKd6Z8pgI', 'CAADBAADZg4AAuf7rQbJ4vrW-y-CPAI',
            'CAADBQADKhgAAsZRxhWrNMZW8VO5PwI', 'CAADBQAD_RgAAsZRxhXU78dx1KWHswI', 'CAADBQADqBkAAsZRxhUZNMbd9XQk8gI',
            'CAADBQADExIAAsZRxhVgT_7AMtFGlwI', 'CAADBQADyQ4AAsZRxhULL8-YqNW8hgI']
cache = ImageCache()

CommandData = namedtuple('CommandData', ['command', 'tag', 'ch_id', 'chan', 'item', 'pages'])

parse_data = {
    'Anime': CommandData('/anime', 'rating:s -loli', '1', '@anime_channel', 'anime', 7658),
    'Hentai (18+)': CommandData('/hentai', 'rating:e -loli', '2', '@hentai_channel', 'hentai', 1527),
    'Yuri (18+)': CommandData('/yuri', 'yuri -loli', '4', '@uncensored_channel', 'yuri', 252),
    'Ecchi (18+)': CommandData('/ecchi', 'rating:q -loli', '5', '@uncensored_channel', 'ecchi', 5622),
    'Uncensored (18+)': CommandData('/uncensored', 'uncensored -loli', '7', '@uncensored_channel', 'uncensored', 367),
    'Wallpaper': CommandData('/wallpaper', 'wallpaper -loli', '8', '@anime_channel', 'wallpaper', 523),
    '/anime': CommandData('/anime', 'rating:s -loli', '1', '@anime_channel', 'anime', 7658),
    '/hentai': CommandData('/hentai', 'rating:e -loli', '2', '@hentai_channel', 'hentai', 1527),
    '/yuri': CommandData('/yuri', 'yuri -loli', '4', '@uncensored_channel', 'yuri', 252),
    '/ecchi': CommandData('/ecchi', 'rating:q -loli', '5', '@uncensored_channel', 'ecchi', 5622),
    '/uncensored': CommandData('/uncensored', 'uncensored -loli', '7', '@uncensored_channel', 'uncensored', 367),
    '/wallpaper': CommandData('/wallpaper', 'wallpaper -loli', '8', '@anime_channel', 'wallpaper', 523),
}

itemset = set(parse_data.keys())
callback_cb = CallbackData('post', 'function', 'data')


class SQLiteMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_update(update: types.Update, data: dict):
        chat_id = None
        chat = None
        if update.message:
            chat = update.message
            command = chat.text
        elif update.callback_query:
            chat = update.callback_query.message
            command = update.callback_query.data

        if chat and chat.from_user:
            user_id = chat.from_user.id
            chat_id = chat.chat.id
            first_name = chat.from_user.first_name
            username = chat.from_user.username or ""

            if command != None:
                async with aiosqlite.connect('users.db') as db:
                    query = 'INSERT INTO commands(user_id, chat_id, first_name, username, command) VALUES(%s, %s, "%s", "%s", "%s")' % (
                        user_id, chat_id, first_name, username, command)
                    await db.execute(query)
                    await db.commit()

        return data

class CommandPermissionMiddleware(BaseMiddleware):
    @staticmethod
    async def on_pre_process_message(message: types.Message, data: dict):
        if data.get("handled_by_command_permission_middleware"):
            return

        # Set a key in the message's data dictionary to indicate that the message
        # has already been handled by this middleware
        data["handled_by_command_permission_middleware"] = True
        # Check if message contains a command
        if not message.text or not message.text.startswith("/"):
            return

        # Check if the command is restricted
        command = message.text.split()[0].lstrip("/")
        if command not in restricted_commands:
            return

        # Check if the user is allowed to execute the command
        if message.from_user.id not in allowed_users:
            await message.answer("You are not authorized to execute this command.")
            raise CancelHandler()


@dp.message_handler(commands=['users'])
async def usercount_handler(message: types.Message):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT COUNT(DISTINCT user_id) FROM commands') as cursor:
            result = await cursor.fetchone()
            user_count = result[0]
        async with db.execute('SELECT user_id, first_name, COUNT(*) as command_count FROM commands GROUP BY user_id ORDER BY command_count DESC LIMIT 10') as cursor:
            results = await cursor.fetchall()
    if len(results) == 0:
        await message.answer("No users found in the database.")
        return
    response = f"{user_count} users in the database\.\nTop users by command count:\n"
    for row in results:
        response += f"[{escape_md(row[1])}](tg://user?id={row[0]}): {row[2]} commands\n"
    await message.answer(response, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=["popular"])
async def popularcommands_handler(message: types.Message):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute(
                'SELECT command, COUNT(*) as count FROM commands GROUP BY command ORDER BY count DESC LIMIT 10') as cursor:
            results = await cursor.fetchall()
    output = "Most popular commands:\n"
    for row in results:
        output += f"{row[0]} ({row[1]} uses)\n"
    await message.answer(output)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if len(message.text.split()) == 1:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btns_text = ('Anime', 'Uncensored (18+)', 'Hentai (18+)', 'Wallpaper', 'Ecchi (18+)', 'Yuri (18+)')
        keyboard_markup.add(*(types.KeyboardButton(text) for text in btns_text))
        await message.answer(
            "Yoo!\nMy name is @anime_bot! I am your personal assistant in the anime world! Yoroshiku onegaishimasu!\n\nUse the keyboard below to navigate the menu.\n\nDeveloper: @ev3me",
            reply_markup=keyboard_markup)
        await message.answer_sticker(sticker=random.choice(stickers))
    elif message.text.split()[1] != 'start':
        await idd(message, tags='id:' + message.text.split()[1])
    else:
        await start(message)


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    if message.text in itemset:
        data = parse_data[message.text]
        ch_id = data.ch_id
        lastcmd[message.chat.id] = data.command
        await parser(message, tags=data.tag, pages=100, chat_id=message.chat.id, ch_id=ch_id)
    elif message.text in parse_data.values():
        await commands(message=message)
    elif message.text in ['/anime@anime_bot', '/hentai@anime_bot', '/uncensored@anime_bot', '/ecchi@anime_bot',
                          '/yuri@anime_bot', '/wallpaper@anime_bot']:
        await commands(message=message, tick=1)


async def commands(message=None, chat_id=None, chan=None, data=None, tick=None):
    source = message
    chat_id = source.chat.id
    vtext = message.text
    if tick == 1:
        vtext = message.text.replace('@anime_bot', '')
    if data is None:
        data = vtext
        if '@anime_bot' in data:
            data = data.replace('@anime_bot', '')
        try:
            data = data.split(' ', 1)[0]
        except:
            pass
    c_id = list(parse_data.keys()).index(data)

    lastcmd[chat_id] = parse_data[data].command
    ch_id = parse_data[data].ch_id

    if chan is not None:
        await parser(source, tags=parse_data[data].tag, pages=parse_data[data].pages, chat_id=chat_id,
                     info='Want More? Join %s' % chan, ch_id=str(ch_id))
    else:
        await parser(source, tags=parse_data[data].tag, pages=parse_data[data].pages, chat_id=chat_id, ch_id=str(ch_id))


async def info_post(tags=None):
    client = Moebooru('yandere')
    posts = client.post_list(tags=tags)
    tags = {}
    for post in posts:
        tags = post
    return tags

async def download_image(semaphore, session, url, post_id):
    async with semaphore:
        async with session.get(url) as response:
            image = await response.content.read()
            filename = f'anime_bot_{post_id}.jpg'
            with open(f'tmp/{filename}', 'wb') as f:
                f.write(image)
            return image


async def idd(message, tags=None):
    client = Moebooru('yandere')
    posts = client.post_list(tags=tags)
    semaphore = asyncio.Semaphore(10)  # Limit the number of concurrent downloads to 10

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(download_image(semaphore, session, post['file_url'], post['id'])) for post in posts]
        images = await asyncio.gather(*tasks)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(types.InlineKeyboardButton('➡️ Next', callback_data=callback_cb.new(function='next', data='')))
    reply_markup = keyboard

    for post, image in zip(posts, images):
        with open(f'tmp/anime_bot_{post["id"]}.jpg', 'rb') as photo:
            caption = f'\n<b>ID: </b><a href="https://t.me/anime_bot?start={post["id"]}">{post["id"]}</a>'
            await message.answer_document(photo, reply_markup=reply_markup, caption=caption, parse_mode=ParseMode.HTML)
            os.remove(f'tmp/anime_bot_{post["id"]}.jpg')


async def parser(message, tags, pages, chat_id, info=None, ch_id=None):  # Usual parser for usual commands
    randomint = randint(1000, 10000000)
    await message.bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
    client = Moebooru('yandere')
    try:
        randompage = randint(1, int(pages))
        data = cache.get(ch_id)
        if not data['url']:
            posts = client.post_list(tags=tags, page=random.randint(1, pages), limit=40)
            for post in posts:
                data['url'].append(post['sample_url'])
                data['id'].append(post['id'])
                data['tags'].append(post['tags'])
        else:
            ikeyboard = types.InlineKeyboardMarkup(row_width=1)
            text_and_data = (
                ('ℹ️ Info', data['id'][0]),
                ('➡️ Next', ch_id),
            )
            row_btns = (types.InlineKeyboardButton(text, callback_data=callback_cb.new(function=text, data=data)) for
                        text, data in text_and_data)
            ikeyboard.row(*row_btns)

            row_btns = (types.InlineKeyboardButton(text="More", url="https://t.me/+Q1JW0j2dEqFhN2My"))
            ikeyboard.row(row_btns)

            text_and_data = (
                ('⬇️ Download', data['id'][0]),
            )
            row_btns = (types.InlineKeyboardButton(text, callback_data=callback_cb.new(function=text, data=data)) for
                        text, data in text_and_data)
            ikeyboard.row(*row_btns)

            reply_markup = ikeyboard
            await message.answer_photo(photo=data['url'][0], reply_markup=reply_markup, caption=info,
                                       parse_mode=ParseMode.HTML)
        try:
            cache.remove_first(ch_id)
        except:
            traceback.print_exc()
        try:
            cache.remove_first(ch_id)
        except:
            traceback.print_exc()


    except Exception:
        traceback.print_exc()
        await message.reply('Oops... Something went wrong, please call the command again!')
        try:
            os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
        except:
            pass
        try:
            cache.remove_first(ch_id)
        except:
            traceback.print_exc()
        try:
            cache.remove_first(ch_id)
        except:
            traceback.print_exc()


@dp.callback_query_handler(callback_cb.filter(function='➡️ Next'))
async def callback_more(query: types.CallbackQuery, callback_data: dict):
    try:
        data = parse_data[lastcmd.get(query.message.chat.id)]
        ch_id = int(data.ch_id)
    except:
        ch_id = 1
    await query.message.edit_reply_markup()
    await commands(message=query.message, chan=parse_data[lastcmd.get(query.message.chat.id)][3],
                   data=lastcmd.get(query.message.chat.id))


@dp.callback_query_handler(callback_cb.filter(function='⬇️ Download'))
async def callback_download(query: types.CallbackQuery, callback_data: dict):
    await query.message.edit_reply_markup()
    await idd(message=query.message, tags='id:' + callback_data['data'])


@dp.callback_query_handler(callback_cb.filter(function='ℹ️ Info'))
async def callback_info(query: types.CallbackQuery, callback_data: dict):
    post_task = asyncio.create_task(info_post(tags='id:' + callback_data['data']))
    tag_string_task = asyncio.create_task(get_tag_string(await post_task))
    pic_source_task = asyncio.create_task(get_pic_source(await post_task))
    old_caption_task = asyncio.create_task(get_old_caption(query.message))

    await query.answer()
    post = await post_task
    new_markup = query.message.reply_markup['inline_keyboard'][0].pop(0)
    caption = f"*Tags: *{await tag_string_task}\n" \
              f"*ID:* [{post['id']}](https://t.me/anime_bot?start={post['id']})" \
              f"{await pic_source_task}\n\n{await old_caption_task}"
    await query.message.edit_caption(
        caption=caption,
        reply_markup=query.message.reply_markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def info_post(tags):
    client = Moebooru('yandere')
    post = await asyncio.to_thread(client.post_list, tags=tags, limit=1)
    if not post:
        raise ValueError("No post found for the given tags")
    return post[0]

async def get_tag_string(post):
    tag_list = post['tags'].split(' ')
    tags = [re.sub(r'[^\w\s]', '', tag) for tag in tag_list][:6]
    tags = ' '.join(f"#{tag}" for tag in tags)
    tags = escape_md(tags)
    return tags

async def get_pic_source(post):
    source = post['source']
    return f"\n[Source]({source})" if source else ""

async def get_old_caption(message):
    old_caption = message.caption or ""
    old_caption = escape_md(old_caption)
    return old_caption

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@dp.inline_handler()
async def inline_function(inline_query: InlineQuery):
    query = inline_query.query
    offset = inline_query.offset
    page = 1

    if offset:
        try:
            page = int(offset.split('page=', 1)[1]) + 1
        except ValueError:
            pass

        offset = f' page={page}'
        query = offset.split(' ', 1)[0]

    if not query:
        query = 'rating:s'

    client = Moebooru('yandere')
    posts = client.post_list(tags=query, limit=50, page=page)
    inline_results = []

    for post in posts:
        inline_result = InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url=post['sample_url'],
            photo_width=post['width'],
            photo_height=post['height'],
            thumb_url=post['preview_url'],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔁Repeat",
                            switch_inline_query_current_chat=query
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="⬇️ Download",
                            url=f"https://t.me/anime_bot?start={post['id']}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Join Uncensored Channel",
                            url="https://t.me/uncensored_channel"
                        )
                    ]
                ]
            )
        )
        inline_results.append(inline_result)

    if len(posts) >= 50:
        next_offset = f'{query} page={page}'
        await bot.answer_inline_query(inline_query.id, results=inline_results, next_offset=next_offset)
    else:
        await bot.answer_inline_query(inline_query.id, results=inline_results)


    if len(posts) >= 50:
        next_offset = f'{query} page={offset}'
        await bot.answer_inline_query(inline_query.id, results=inline_results, next_offset=next_offset)
    else:
        await bot.answer_inline_query(inline_query.id, results=inline_results)


    if len(posts) >= 50:
        next_offset = f'{query} page={offset}'
        await bot.answer_inline_query(inline_query.id, results=inline_results, next_offset=next_offset)
    else:
        await bot.answer_inline_query(inline_query.id, results=inline_results)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    dp.middleware.setup(SQLiteMiddleware())
    dp.middleware.setup(CommandPermissionMiddleware())
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    # executor.start_polling(dp, skip_updates=True)

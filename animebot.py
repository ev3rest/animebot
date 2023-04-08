import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import ChatActions
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ParseMode, InlineQuery, InlineQueryResultPhoto
from aiogram.utils.executor import start_webhook
from pybooru import Moebooru, Danbooru
import traceback
from uuid import uuid4
import random
import urllib.request
import os
from random import randint
from aiogram.dispatcher.middlewares import BaseMiddleware
import aiosqlite
from collections import namedtuple

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''
lastcmd = {}

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
#----------------------------------
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = 'https://dev.ev3.me'
WEBHOOK_PATH = '/bot/api'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3009
#----------------------------------

stickers = ['CAADBAADJgMAAqKYZgAB0UH2shlpMSsC', 'CAADBAADLAMAAqKYZgABayywIAiqZ0gC', 'CAADBAADOAMAAqKYZgABh5wcd4QnpcwC', 'CAADBAADPQMAAqKYZgABur46JrhDohYC', 'CAADBAADswMAAqKYZgABVzxxH4lMba0C', 'CAADBAAD3gQAAqKYZgABmxmc1Y3A4xQC', 'CAADBAADWAUAAqKYZgAB1ia7fuNxpq4C', 'CAADBAADXA4AAh3PuAc4x8-E_-7aygI', 'CAADBAADeg4AAh3PuAe2kQ3GPRO3hwI', 'CAADBAADkg4AAh3PuAcj4B3CTwjDiQI', 'CAADBAADiwIAAsiLDQhiubnq7ueZrgI', 'CAADBAADmQIAAsiLDQgLP7VMIuZXgAI', 'CAADBAADmwIAAsiLDQiPkeWZT0jKPQI', 'CAADBAADlQIAAsiLDQhcIu-tSCjcBQI', 'CAADBAADjwIAAsiLDQjYx7KvqxKFMgI', 'CAADBAADnwIAAsiLDQibN_CcD5zfkQI', 'CAADBAADnQIAAsiLDQihvo41EnrDzAI', 'CAADBAADpQIAAsiLDQjK923PGHm5QQI', 'CAADBAADowIAAsiLDQgvfkwYeEQ-2QI', 'CAADBAADpwIAAsiLDQizmtsoKxTPggI', 'CAADBAADrQIAAsiLDQgMCsrjsg3v4wI', 'CAADBAADrwIAAsiLDQjIXFtjd_TqNAI', 'CAADBAADtwIAAsiLDQiBcvZcIdSJGgI', 'CAADBAADsQIAAsiLDQhLpnmM589abAI', 'CAADBAAD0QIAAsiLDQhh8fBJJVLT8QI', 'CAADBAAD0wIAAsiLDQgkmlDTS1nm7QI', 'CAADBAAD1wIAAsiLDQgNRH763A4EjgI', 'CAADAQADoQEAArna9gmuB8gVICvS9wI', 'CAADAQADqQEAArna9gnqCzMdDF0lUAI', 'CAADAQADrQEAArna9glHGcsWYKiMRAI', 'CAADAQADqwEAArna9gkmp05lNiNn9wI', 'CAADAQADtwEAArna9gkDeV746IbSwQI', 'CAADAQADvQEAArna9gnuMPtOZrW1PQI', 'CAADAQADvwEAArna9glCn8R5s1LbZAI', 'CAADBAADJgEAAqM2qAemZ_YJbuzDJwI', 'CAADBAADOQEAAqM2qAfkrc477ntjIgI', 'CAADBAADMAEAAqM2qAeX7j7nLeiNFQI', 'CAADBAADVAEAAqM2qAd0tDCJZ3A8ggI', 'CAADBAADUQEAAqM2qAdbGe9WG9EogQI', 'CAADBAADTAEAAqM2qAd-3A6X_ijf1wI', 'CAADBAADSAEAAqM2qAcAAUws3DcwQdIC', 'CAADBAADRgEAAqM2qAdssyA7IPhymQI', 'CAADBAADVgEAAqM2qAeDuMRxavg-9gI', 'CAADBAADhAADDvcmBlTiJw2iW3-DAg', 'CAADBAADhgADDvcmBhTDcsXEcO8RAg', 'CAADBAADiAADDvcmBmtco0ch3eYmAg', 'CAADBAADigADDvcmBsN4in4FXW4aAg', 'CAADBAADoQADDvcmBn7hBgmWUK1xAg', 'CAADBAADrQADDvcmBpQJ1c4eo8SaAg', 'CAADBAADxQQAAsOSbAP7HMKduOaRDAI', 'CAADBAAD0QQAAsOSbAPzeE-N7Wo1XAI', 'CAADBAAD1wQAAsOSbAMUAabgPzSUxAI', 'CAADBAAD2QQAAsOSbAM5-ZiM9NwCYQI', 'CAADBAAD3wQAAsOSbAN8cWh9AAGZ4JEC', 'CAADBAAD7QQAAsOSbAP87mq-1IhdVAI', 'CAADBAADngUAAsOSbAPyZJxHHwABDOsC', 'CAADBAADuwUAAsOSbAPVCu6yVd9AYgI', 'CAADBAADTwEAAqIkSQOcLYaijPdA9AI', 'CAADBAADewEAAqIkSQOKtlOA7PDVswI', 'CAADBAADfwEAAqIkSQMwmItrQLEAAbQC', 'CAADBAADigEAAqIkSQNNtoHkx9ztAQI', 'CAADBAADkAEAAqIkSQMLvYm2Z-WYYgI', 'CAADBAADmAEAAqIkSQP6IpIzeuoqdQI', 'CAADBAADmgEAAqIkSQPznG-Ig4iwAQI', 'CAADBAADogEAAqIkSQMs3FfHKdWVzAI', 'CAADBAADqAEAAqIkSQPH-RWOk7OuDQI', 'CAADBAADtgEAAqIkSQNaxXsO6qI36gI', 'CAADBAADvwEAAqIkSQOeSXUAAS1PnwsC', 'CAADBAAD8AEAAqIkSQOYAAF3LuxtgicC', 'CAADBAAD_AEAAqIkSQNHqmcGA9vgeAI', 'CAADBAAD8gEAAqIkSQMqnIXPK9AO4AI', 'CAADBAAD-AEAAqIkSQOST8xeeqZZ_QI', 'CAADBAADyAUAAuAFHALE9DV1idj8GQI', 'CAADBAAD0AUAAuAFHAKKqQlswE-TxAI', 'CAADBAAD7gUAAuAFHAJt4SYHShUyHQI', 'CAADBAAD1gUAAuAFHALWRdze8hSGgAI', 'CAADBQADYgAD6NvJAjw6mwsi3ZDcAg', 'CAADBQADawAD6NvJAvSDRGZiKm0-Ag', 'CAADBAADawYAApesNQABqnPuHOSm_rUC', 'CAADBAADggYAApesNQABY52p_5jYmDAC', 'CAADBAADkgYAApesNQABrWxxAo4i5YIC', 'CAADBAADlgYAApesNQABAaQoqR18rJcC', 'CAADBAADwAYAApesNQABj-Un4Rf2kAEC', 'CAADBAADpgMAApv7sgABKyxNf3LVHeAC', 'CAADBAADtAMAApv7sgAB-1esnD-WlHIC', 'CAADBAAD7gMAApv7sgABGCZKqVeej3YC', 'CAADAwADhAAD_ZPKAAGphJ9IUmjqqAI', 'CAADAgADsgADdqy6ButIWEMMsnSMAg', 'CAADAQADygMAAuJbQAVEJd8sOLqNJwI', 'CAADAQADyAMAAuJbQAU-y13TznSWXwI', 'CAADAQAD1AMAAuJbQAXPlcSmhmgxOgI', 'CAADBAADfQADylycBfFLFOlpUkSAAg', 'CAADBAADfwADylycBerATexgP5rfAg', 'CAADBAADgQADylycBRxpx-hgT8dBAg', 'CAADBAADgwADylycBapS4Fz1ozG4Ag', 'CAADBAADhwADylycBUXx92Qbc0HeAg', 'CAADBAADogADylycBWLXUovOwXa6Ag', 'CAADBAAD3gADylycBS0QiC-O4zvYAg', 'CAADBAADDAUAAspcnAU4aO3nT9quMAI', 'CAADBAADHgUAAspcnAVLCx1VIZ2laQI', 'CAADBAADOAUAAspcnAV7Wx41DCZINwI', 'CAADBAADaQEAAl7ugQYqaKHrgmb7mgI', 'CAADBAADOQQAAnZY-wJXL61k-or-uwI', 'CAADBAADQgQAAnZY-wJ2XZvSz11GhQI', 'CAADBAADTgQAAnZY-wK6b_dynGPoTAI', 'CAADBAADlwMAAspcnAWOVBRIBv3K7QI', 'CAADBAADmwMAAspcnAVYLJLwdXI4twI', 'CAADBAADvwMAAspcnAXh31MvOjw4_wI', 'CAADBAAD-QMAAspcnAU7QO_IByh3UQI', 'CAADBAAD5QMAAspcnAW5Pl-29Mre9gI', 'CAADBAADBwQAAspcnAUaKvx4Bb99kQI', 'CAADBAADQwQAAspcnAW3qRleNi9aNQI', 'CAADBAADxQwAAuf7rQZlyZi2n5t29QI', 'CAADBAADzwwAAuf7rQZMLO8dV3dzTAI', 'CAADBAAD1wwAAuf7rQZvaEDPm8950gI', 'CAADBAAD0wwAAuf7rQZat80CHwABEtcC', 'CAADBAAD0QwAAuf7rQa1vDSzF2iXDAI', 'CAADBAAD3wwAAuf7rQYE4k-pmuUnIQI', 'CAADBAADYA0AAuf7rQabM1fOJ2yZ1wI', 'CAADBAADYw4AAuf7rQYZUvpBdCk2pgI', 'CAADBAADhg4AAuf7rQbJl5Bat1xMsgI', 'CAADBAADiA4AAuf7rQb2C3BKd6Z8pgI', 'CAADBAADZg4AAuf7rQbJ4vrW-y-CPAI', 'CAADBQADKhgAAsZRxhWrNMZW8VO5PwI', 'CAADBQAD_RgAAsZRxhXU78dx1KWHswI', 'CAADBQADqBkAAsZRxhUZNMbd9XQk8gI', 'CAADBQADExIAAsZRxhVgT_7AMtFGlwI', 'CAADBQADyQ4AAsZRxhULL8-YqNW8hgI']
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
      if update.message:
        chat = update.message
        command = chat.text
      elif update.callback_query:
        chat = update.callback_query.message
        command = update.callback_query.data
      user_id = chat.from_user.id
      chat_id = chat.chat.id
      first_name = chat.from_user.first_name
      username = chat.from_user.username or ""

      if command!=None:
	      async with aiosqlite.connect('users.db') as db:
	        query = 'INSERT INTO commands(user_id, chat_id, first_name, username, command) VALUES(%s, %s, "%s", "%s", "%s")' % (user_id, chat_id, first_name, username, command)
	        await db.execute(query)
	        await db.commit()

      return data


@dp.message_handler(commands=['users'])
async def usercount_handler(message: types.Message):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT COUNT(DISTINCT user_id) FROM commands') as cursor:
            result = await cursor.fetchone()
    count = result[0]
    await message.answer(f"{count} users in the database.")

@dp.message_handler(commands=["popular"])
async def popularcommands_handler(message: types.Message):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT command, COUNT(*) as count FROM commands GROUP BY command ORDER BY count DESC LIMIT 10') as cursor:
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
        await message.answer("Yoo!\nMy name is @anime_bot! I am your personal assistant in the anime world! Yoroshiku onegaishimasu!\n\nUse the keyboard below to navigate the menu.\n\nDeveloper: @ev3me", reply_markup=keyboard_markup)
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
    elif message.text in ['/anime@anime_bot', '/hentai@anime_bot', '/uncensored@anime_bot', '/ecchi@anime_bot', '/yuri@anime_bot', '/wallpaper@anime_bot']:
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
        await parser(source, tags=parse_data[data].tag, pages=parse_data[data].pages, chat_id=chat_id, info='Want More? Join %s' % chan, ch_id=str(ch_id))
    else:
        await parser(source, tags=parse_data[data].tag, pages=parse_data[data].pages, chat_id=chat_id, ch_id=str(ch_id))

async def info_post(tags=None):
       client = Moebooru('yandere')
       posts = client.post_list(tags=tags)
       tags = {}
       for post in posts:
              tags = post
       return tags

async def idd(message, tags=None):
       randomint = randint(1000, 10000000)
       try:
              client = Moebooru('yandere')
              posts = client.post_list(tags=tags)
              for post in posts:
                     urllib.request.urlretrieve(post['file_url'], "tmp/anime_bot_" + str(randomint) + ".jpg")
              try:
                     c_id = parse_data['commands'].index(lastcmd.get(message.chat.id))
              except:
                     c_id=1  # For when downloading a file from channel without using a bot prior to this, default set to rating:s
              ckeyboard = types.InlineKeyboardMarkup(row_width=1)
              text_and_data = (
                     ('→ Next', c_id),
              )
              row_btns = (types.InlineKeyboardButton(text, callback_data=callback_cb.new(function=text, data=data)) for text, data in text_and_data)
              ckeyboard.row(*row_btns)
              reply_markup = ckeyboard
              photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
              file_caption = '\n<b>ID: </b><a href="https://t.me/anime_bot?start=%s">%s</a>' %(post['id'], post['id'])
              await message.answer_document(photo, reply_markup=reply_markup, caption=file_caption, parse_mode=ParseMode.HTML)
              photo.close()
              os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
       except Exception:
              traceback.print_exc()

async def parser(message, tags, pages, chat_id, info=None, ch_id=None): #Usual parser for usual commands
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
                            ('ⓘ Info', data['id'][0]),
                            ('→ Next', ch_id),
                     )
                     row_btns = (types.InlineKeyboardButton(text, callback_data=callback_cb.new(function=text, data=data)) for text, data in text_and_data)
                     ikeyboard.row(*row_btns)

                     row_btns = (types.InlineKeyboardButton(text="More", url="https://t.me/+Q1JW0j2dEqFhN2My"))
                     ikeyboard.row(row_btns)

                     text_and_data = (
                            ('↧ Download', data['id'][0]),
                     )
                     row_btns = (types.InlineKeyboardButton(text, callback_data=callback_cb.new(function=text, data=data)) for text, data in text_and_data)
                     ikeyboard.row(*row_btns)

                     #row_btns = (types.InlineKeyboardButton(text="🖼️ HARDCORE HENTAI 🖼️", url="https://t.me/+0OzfFvBS7ItmZDE6"))
                     #ikeyboard.row(row_btns)
                     
                     reply_markup = ikeyboard
                     # if info == None:
                     #   info = ''
                     # info = info + "\n" + '<a href="%s">Source</a>' % (x[str(ch_id)]['tags'][0])
                     await message.answer_photo(photo=data['url'][0], reply_markup=reply_markup, caption=info, parse_mode=ParseMode.HTML)
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

@dp.callback_query_handler(callback_cb.filter(function='→ Next'))
async def callback_more(query: types.CallbackQuery, callback_data: dict):
       try:
              c_id = parse_data['commands'].index(lastcmd.get(query.message.chat.id))
       except:
              c_id=1
       await query.message.edit_reply_markup()
       await commands(message=query.message, chan=parse_data['chan'][c_id], data=lastcmd.get(query.message.chat.id))   

@dp.callback_query_handler(callback_cb.filter(function='↧ Download'))
async def callback_download(query: types.CallbackQuery, callback_data: dict):
       await query.message.edit_reply_markup()
       await idd(message=query.message, tags='id:'+callback_data['data'])

@dp.callback_query_handler(callback_cb.filter(function='ⓘ Info'))
async def callback_info(query: types.CallbackQuery, callback_data: dict):
       await info_post(tags='id:'+callback_data['data'])
       new_markup = query.message.reply_markup['inline_keyboard'][0].pop(0)
       if query.message.caption != None:
              old_caption = str(query.message.caption)
       else:
              old_caption = ""
       post = await info_post(tags='id:'+callback_data['data'])
       tags_str = ""
       tags_str = tags_str.join(post['tags'])
       pic_source = '\n<a href="%s"><u>Source</u></a>' % (post['source']) if post['source']!="" else ""
       await query.message.edit_caption(caption = "<b>Tags: </b>" + tags_str + "\n<b>Uploader: </b>%s" % (post['author']) + '\n<b>ID: </b><a href="https://t.me/anime_bot?start=%s">%s</a>' %(post['id'], post['id']) + pic_source + "\n\n%s" % (old_caption), reply_markup=query.message.reply_markup, parse_mode=ParseMode.HTML)


@dp.inline_handler()
async def inline_function(inline_query: InlineQuery):
       query = inline_query.query
       offset = inline_query.offset
       if offset != '':
              query = offset.split(' ', 1)[0]
              offset = int(offset.split('page=', 1)[1])
              offset+=1
              offset = ' page=' + str(offset)
       else:
              offset = ' page=1'
       if query is None:
              query = 'rating:s'
       client = Moebooru('yandere')
       posts = client.post_list(tags=query, limit=50, page=int(offset.split('page=', 1)[1]))
       lposts = len(posts)
       inlinequery = list()
       for post in posts:
              inlinequery.append(InlineQueryResultPhoto(
                            id=str(uuid4()),
                            photo_url=post['sample_url'],
                            photo_width=post['width'],
                            photo_height=post['height'],
                            thumb_url=post['preview_url'],
                            caption='<a href="https://t.me/anime_bot?start=%s">Download</a>' % (post['id']), 
                            parse_mode=ParseMode.HTML),)
       if lposts >=50:
              await bot.answer_inline_query(inline_query.id, results=inlinequery, next_offset=query + offset)
       else:
              await bot.answer_inline_query(inline_query.id, results=inlinequery)
       inlinequery.clear()

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
       executor.start_webhook(
              dispatcher=dp,
              webhook_path=WEBHOOK_PATH,
              on_startup=on_startup,
              on_shutdown=on_shutdown,
              skip_updates=True,
              host=WEBAPP_HOST,
              port=WEBAPP_PORT,
       )
       #executor.start_polling(dp, skip_updates=True)
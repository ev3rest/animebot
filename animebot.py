#----------------------------------
# Developer: Digital Entropy
# Program: Anime Bot for Telegram
# (c) Digital Entropy 2018
# License: Proprietary Software
#-----------------------------------
from __future__ import unicode_literals
import logging
import os
import time
import traceback
from random import randint
import urllib.request
from uuid import uuid4
from time import sleep
from pathlib import Path
import random
import json
from collections import defaultdict
import gc
import sys
import requests
import datetime
import json
from pybooru import Moebooru, Danbooru
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InlineQueryResultPhoto, LabeledPrice
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, Filters, PreCheckoutQueryHandler
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
						   '%(message)s',
					level=logging.WARNING)

gc.enable() #Garbage collector

superusers=[47571378]

bkeyboard = ReplyKeyboardMarkup(
			[[KeyboardButton("Anime"), KeyboardButton("Ecchi (18+)")], [KeyboardButton("Hentai (18+)"), KeyboardButton("Uncensored (18+)")], [KeyboardButton("Yuri (18+)"), KeyboardButton("Loli (18+)"), KeyboardButton("Neko")], [KeyboardButton("Wallpaper"), KeyboardButton("GIF (18+)")]],
			one_time_keyboard=False, resize_keyboard=True)
alkeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Donate", url = 'https://paypal.me/ev3rest')], [InlineKeyboardButton("Developer", url='https://t.me/ev3me')], [InlineKeyboardButton("Music", url='https://t.me/musicave')]])

#VARIABLES

lastcmd = {}
x = {'1':{'url':[], 'id':[]}, '2':{'url':[], 'id':[]}, '3':{'url':[], 'id':[]}, '4':{'url':[], 'id':[]}, '5':{'url':[], 'id':[]}, '6':{'url':[], 'id':[]}, '7':{'url':[], 'id':[]}, '8':{'url':[], 'id':[]}, '9':{'url':[], 'id':[]}}
d = {'1': {'data': '', 'url': ''}, '2': {'data': '', 'url': ''}, '3': {'data': '', 'url': ''}, '4': {'data': '', 'url': ''}, '5': {'data': '', 'url': ''}, '6': {'data': '', 'url': ''}, '7': {'data': '', 'url': ''}, '8': {'data': '', 'url': ''}, '9': {'data': '', 'url': ''}}
parse_data = {'commands':['/anime', '/hentai', '/loli', '/yuri', '/ecchi', '/neko', '/uncensored', '/wallpaper', '/gif'], 'tags':['rating:s', 'rating:e', 'loli', 'yuri', 'rating:q', 'cat_ears', 'uncensored', 'wallpaper', 'animated_gif'], 'ch_id': ['1', '2', '3', '4', '5', '6', '7', '8', '9'], 'chan':['@anime_channel', '@hentai_channel', '@channel_loli', '@yuri_channel', '@channel_ecchi', '@anime_channel', '@uncensored_channel', '@anime_channel', '@uncensored_channel'], 'items':['anime', 'hentai', 'loli', 'yuri', 'ecchi', 'neko', 'uncensored', 'wallpaper', 'gif']}

stickers = ['CAADBAADJgMAAqKYZgAB0UH2shlpMSsC', 'CAADBAADLAMAAqKYZgABayywIAiqZ0gC', 'CAADBAADOAMAAqKYZgABh5wcd4QnpcwC', 'CAADBAADPQMAAqKYZgABur46JrhDohYC', 'CAADBAADswMAAqKYZgABVzxxH4lMba0C', 'CAADBAAD3gQAAqKYZgABmxmc1Y3A4xQC', 'CAADBAADWAUAAqKYZgAB1ia7fuNxpq4C', 'CAADBAADXA4AAh3PuAc4x8-E_-7aygI', 'CAADBAADeg4AAh3PuAe2kQ3GPRO3hwI', 'CAADBAADkg4AAh3PuAcj4B3CTwjDiQI', 'CAADBAADiwIAAsiLDQhiubnq7ueZrgI', 'CAADBAADmQIAAsiLDQgLP7VMIuZXgAI', 'CAADBAADmwIAAsiLDQiPkeWZT0jKPQI', 'CAADBAADlQIAAsiLDQhcIu-tSCjcBQI', 'CAADBAADjwIAAsiLDQjYx7KvqxKFMgI', 'CAADBAADnwIAAsiLDQibN_CcD5zfkQI', 'CAADBAADnQIAAsiLDQihvo41EnrDzAI', 'CAADBAADpQIAAsiLDQjK923PGHm5QQI', 'CAADBAADowIAAsiLDQgvfkwYeEQ-2QI', 'CAADBAADpwIAAsiLDQizmtsoKxTPggI', 'CAADBAADrQIAAsiLDQgMCsrjsg3v4wI', 'CAADBAADrwIAAsiLDQjIXFtjd_TqNAI', 'CAADBAADtwIAAsiLDQiBcvZcIdSJGgI', 'CAADBAADsQIAAsiLDQhLpnmM589abAI', 'CAADBAAD0QIAAsiLDQhh8fBJJVLT8QI', 'CAADBAAD0wIAAsiLDQgkmlDTS1nm7QI', 'CAADBAAD1wIAAsiLDQgNRH763A4EjgI', 'CAADAQADoQEAArna9gmuB8gVICvS9wI', 'CAADAQADqQEAArna9gnqCzMdDF0lUAI', 'CAADAQADrQEAArna9glHGcsWYKiMRAI', 'CAADAQADqwEAArna9gkmp05lNiNn9wI', 'CAADAQADtwEAArna9gkDeV746IbSwQI', 'CAADAQADvQEAArna9gnuMPtOZrW1PQI', 'CAADAQADvwEAArna9glCn8R5s1LbZAI', 'CAADBAADJgEAAqM2qAemZ_YJbuzDJwI', 'CAADBAADOQEAAqM2qAfkrc477ntjIgI', 'CAADBAADMAEAAqM2qAeX7j7nLeiNFQI', 'CAADBAADVAEAAqM2qAd0tDCJZ3A8ggI', 'CAADBAADUQEAAqM2qAdbGe9WG9EogQI', 'CAADBAADTAEAAqM2qAd-3A6X_ijf1wI', 'CAADBAADSAEAAqM2qAcAAUws3DcwQdIC', 'CAADBAADRgEAAqM2qAdssyA7IPhymQI', 'CAADBAADVgEAAqM2qAeDuMRxavg-9gI', 'CAADBAADhAADDvcmBlTiJw2iW3-DAg', 'CAADBAADhgADDvcmBhTDcsXEcO8RAg', 'CAADBAADiAADDvcmBmtco0ch3eYmAg', 'CAADBAADigADDvcmBsN4in4FXW4aAg', 'CAADBAADoQADDvcmBn7hBgmWUK1xAg', 'CAADBAADrQADDvcmBpQJ1c4eo8SaAg', 'CAADBAADxQQAAsOSbAP7HMKduOaRDAI', 'CAADBAAD0QQAAsOSbAPzeE-N7Wo1XAI', 'CAADBAAD1wQAAsOSbAMUAabgPzSUxAI', 'CAADBAAD2QQAAsOSbAM5-ZiM9NwCYQI', 'CAADBAAD3wQAAsOSbAN8cWh9AAGZ4JEC', 'CAADBAAD7QQAAsOSbAP87mq-1IhdVAI', 'CAADBAADngUAAsOSbAPyZJxHHwABDOsC', 'CAADBAADuwUAAsOSbAPVCu6yVd9AYgI', 'CAADBAADTwEAAqIkSQOcLYaijPdA9AI', 'CAADBAADewEAAqIkSQOKtlOA7PDVswI', 'CAADBAADfwEAAqIkSQMwmItrQLEAAbQC', 'CAADBAADigEAAqIkSQNNtoHkx9ztAQI', 'CAADBAADkAEAAqIkSQMLvYm2Z-WYYgI', 'CAADBAADmAEAAqIkSQP6IpIzeuoqdQI', 'CAADBAADmgEAAqIkSQPznG-Ig4iwAQI', 'CAADBAADogEAAqIkSQMs3FfHKdWVzAI', 'CAADBAADqAEAAqIkSQPH-RWOk7OuDQI', 'CAADBAADtgEAAqIkSQNaxXsO6qI36gI', 'CAADBAADvwEAAqIkSQOeSXUAAS1PnwsC', 'CAADBAAD8AEAAqIkSQOYAAF3LuxtgicC', 'CAADBAAD_AEAAqIkSQNHqmcGA9vgeAI', 'CAADBAAD8gEAAqIkSQMqnIXPK9AO4AI', 'CAADBAAD-AEAAqIkSQOST8xeeqZZ_QI', 'CAADBAADyAUAAuAFHALE9DV1idj8GQI', 'CAADBAAD0AUAAuAFHAKKqQlswE-TxAI', 'CAADBAAD7gUAAuAFHAJt4SYHShUyHQI', 'CAADBAAD1gUAAuAFHALWRdze8hSGgAI', 'CAADBQADYgAD6NvJAjw6mwsi3ZDcAg', 'CAADBQADawAD6NvJAvSDRGZiKm0-Ag', 'CAADBAADawYAApesNQABqnPuHOSm_rUC', 'CAADBAADggYAApesNQABY52p_5jYmDAC', 'CAADBAADkgYAApesNQABrWxxAo4i5YIC', 'CAADBAADlgYAApesNQABAaQoqR18rJcC', 'CAADBAADwAYAApesNQABj-Un4Rf2kAEC', 'CAADBAADpgMAApv7sgABKyxNf3LVHeAC', 'CAADBAADtAMAApv7sgAB-1esnD-WlHIC', 'CAADBAAD7gMAApv7sgABGCZKqVeej3YC', 'CAADAwADhAAD_ZPKAAGphJ9IUmjqqAI', 'CAADAgADsgADdqy6ButIWEMMsnSMAg', 'CAADAQADygMAAuJbQAVEJd8sOLqNJwI', 'CAADAQADyAMAAuJbQAU-y13TznSWXwI', 'CAADAQAD1AMAAuJbQAXPlcSmhmgxOgI', 'CAADBAADfQADylycBfFLFOlpUkSAAg', 'CAADBAADfwADylycBerATexgP5rfAg', 'CAADBAADgQADylycBRxpx-hgT8dBAg', 'CAADBAADgwADylycBapS4Fz1ozG4Ag', 'CAADBAADhwADylycBUXx92Qbc0HeAg', 'CAADBAADogADylycBWLXUovOwXa6Ag', 'CAADBAAD3gADylycBS0QiC-O4zvYAg', 'CAADBAADDAUAAspcnAU4aO3nT9quMAI', 'CAADBAADHgUAAspcnAVLCx1VIZ2laQI', 'CAADBAADOAUAAspcnAV7Wx41DCZINwI', 'CAADBAADaQEAAl7ugQYqaKHrgmb7mgI', 'CAADBAADOQQAAnZY-wJXL61k-or-uwI', 'CAADBAADQgQAAnZY-wJ2XZvSz11GhQI', 'CAADBAADTgQAAnZY-wK6b_dynGPoTAI', 'CAADBAADlwMAAspcnAWOVBRIBv3K7QI', 'CAADBAADmwMAAspcnAVYLJLwdXI4twI', 'CAADBAADvwMAAspcnAXh31MvOjw4_wI', 'CAADBAAD-QMAAspcnAU7QO_IByh3UQI', 'CAADBAAD5QMAAspcnAW5Pl-29Mre9gI', 'CAADBAADBwQAAspcnAUaKvx4Bb99kQI', 'CAADBAADQwQAAspcnAW3qRleNi9aNQI', 'CAADBAADxQwAAuf7rQZlyZi2n5t29QI', 'CAADBAADzwwAAuf7rQZMLO8dV3dzTAI', 'CAADBAAD1wwAAuf7rQZvaEDPm8950gI', 'CAADBAAD0wwAAuf7rQZat80CHwABEtcC', 'CAADBAAD0QwAAuf7rQa1vDSzF2iXDAI', 'CAADBAAD3wwAAuf7rQYE4k-pmuUnIQI', 'CAADBAADYA0AAuf7rQabM1fOJ2yZ1wI', 'CAADBAADYw4AAuf7rQYZUvpBdCk2pgI', 'CAADBAADhg4AAuf7rQbJl5Bat1xMsgI', 'CAADBAADiA4AAuf7rQb2C3BKd6Z8pgI', 'CAADBAADZg4AAuf7rQbJ4vrW-y-CPAI', 'CAADBQADKhgAAsZRxhWrNMZW8VO5PwI', 'CAADBQAD_RgAAsZRxhXU78dx1KWHswI', 'CAADBQADqBkAAsZRxhUZNMbd9XQk8gI', 'CAADBQADExIAAsZRxhVgT_7AMtFGlwI', 'CAADBQADyQ4AAsZRxhULL8-YqNW8hgI']

#Tokens
bot_token = 'TOKEN'
danbooru_key = 'DanbooruKEY'

#CODE

@run_async
def start(bot, update):
	s = update.message.text
	if "ihelp" in s:
		ihelp(bot, update)
	else:
		try:
			s = s.split(' ', 1)[1]
			idd(bot, update, chat_id=update.message.chat_id, tags='id:' + s)
		except Exception as e:
			try:
				bot.sendMessage(update.message.chat_id, "Yoo!\nMy name is @uncensored_bot! I am your personal assistant in the anime world! Yoroshiku onegaishimasu!\n\nUse the keyboard below to navigate the menu.\n\nFeeback: /feedback", reply_markup=bkeyboard)
				stick = random.randint(0, len(stickers) - 1)
				bot.sendSticker(update.message.chat_id, sticker = stickers[stick])
			except Exception:
				traceback.print_exc()

@run_async
def messages(bot, update):
	itemlist=['Anime', 'Hentai (18+)', 'Loli (18+)', 'Yuri (18+)', 'Ecchi (18+)', 'Neko', 'Uncensored (18+)', 'Wallpaper', 'GIF (18+)']
	if update.effective_message.text in itemlist:
		ch_id = parse_data['ch_id'][itemlist.index(update.message.text)]
		lastcmd[update.message.chat_id] = parse_data['commands'][itemlist.index(update.message.text)]
		parser(bot, update, tags=parse_data['tags'][itemlist.index(update.message.text)], pages='90', chat_id=update.message.chat_id, ch_id=str(ch_id))

@run_async
def commands(bot, update, chat_id=None, chan=None, data=None):
	if update.message == None:
		source = update.callback_query.message
		c_type='callback'
	else:
		source=update.message
		c_type='command'
	chat_id = source.chat_id
	if data == None:
		data = update.message.text
		if '@uncensored_bot' in data:
			data = data.replace('@uncensored_bot', '')
		try:
			data = data.split(' ', 1)[0]
		except:
			pass
	c_id = parse_data['commands'].index(data)

	lastcmd[chat_id] = parse_data['commands'][c_id]
	ch_id = parse_data['ch_id'][c_id]


	if chan !=None:
		parser(bot, update, tags=parse_data['tags'][c_id], pages='90', chat_id=chat_id, info='Want more? Join %s' % chan, ch_id=str(ch_id))
	else:
		parser(bot, update, tags=parse_data['tags'][c_id], pages='90', chat_id=chat_id, ch_id=str(ch_id))

@run_async
def idd(bot, update, tags=None, chat_id=None):
	randomint = randint(1000, 10000000)
	try:
		bot.sendChatAction(chat_id, "upload_document")
		try:
			client = Moebooru('yandere')
			posts = client.post_list(tags=tags)
			for post in posts:
				urllib.request.urlretrieve(post['file_url'], "tmp/uncensored_bot_" + str(randomint) + ".jpg")
			ckeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Donate", url = 'https://paypal.me/ev3rest')], [InlineKeyboardButton("More", callback_data="{'data':'More'}")]])
			reply_markup = ckeyboard
			photo = open('tmp/uncensored_bot_' + str(randomint) + ".jpg", 'rb')
			bot.sendDocument(chat_id, photo, reply_markup=reply_markup)
			photo.close()
			os.remove('tmp/uncensored_bot_' + str(randomint) + ".jpg")
		except Exception:
			traceback.print_exc()
	except Exception:
		traceback.print_exc()

@run_async
def parser(bot, update, tags, pages, chat_id, info=None, ch_id=None): #Usual parser for usual commands
	global x
	global p_id
	randomint = randint(1000, 10000000)
	if ch_id == '9':
		bot.sendChatAction(chat_id, "upload_document")
		client = Danbooru('danbooru', username='tiny_paw', api_key=danbooru_key)
	else:
		bot.sendChatAction(chat_id, "upload_photo")
		client = Moebooru('yandere')
	try:
		randompage = randint(1, int(pages))
		if len(x[str(ch_id)]['url']) == 0:
			posts = client.post_list(tags=str(tags), page=randompage, limit=40)
			for post in posts:
				if ch_id == '9':
					fileurl = post['file_url']
				else:
					fileurl = post['sample_url']
				x[str(ch_id)]['url'].append(fileurl)
				x[str(ch_id)]['id'].append(post['id'])
		if ch_id == '9':
			ikeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Donate", url = 'https://paypal.me/ev3rest')], [InlineKeyboardButton("Music", url='https://t.me/musicave')], [InlineKeyboardButton("More", callback_data="{'data':'More', 'c_id':%s}"%ch_id)]])
		else:
			ikeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Donate", url = 'https://paypal.me/ev3rest')], [InlineKeyboardButton("Music", url='https://t.me/musicave')], [InlineKeyboardButton("Download", callback_data="{'data':'Download', 'id':%s}"%x[str(ch_id)]['id'][0])], [InlineKeyboardButton("More", callback_data="{'data':'More', 'c_id':%s}"%ch_id)]])
		reply_markup = ikeyboard
		if ch_id != '9':
			bot.sendPhoto(chat_id, photo=x[str(ch_id)]['url'][0], reply_markup=reply_markup, caption=info)
		else:
			bot.sendDocument(chat_id, document=x[str(ch_id)]['url'][0], reply_markup=reply_markup, caption=info)
		try:
			x[str(ch_id)]['url'].pop(0)
		except:
			traceback.print_exc()
		try:
			x[str(ch_id)]['id'].pop(0)
		except:
			traceback.print_exc()
		

	except Exception:
		traceback.print_exc()
		bot.sendMessage(chat_id, 'Oops... Something went wrong, please call the command again!')
		try:
			os.remove('tmp/uncensored_bot_' + str(randomint) + ".jpg")
		except:
			pass
		try:
			x[str(ch_id)]['url'].pop(0)
		except:
			traceback.print_exc()
		try:
			x[str(ch_id)]['id'].pop(0)
		except:
			traceback.print_exc()

@run_async
def callback(bot, update): #Callback handler
	global p_id
	query = update.callback_query
	if json.loads(query.data.replace("'", "\""))['data'] == "More":
		try:
			bot.editMessageReplyMarkup(query.message.chat_id, query.message.message_id)
			c_id = parse_data['commands'].index(lastcmd.get(query.message.chat_id))
			bot.answer_callback_query(query.id, str(parse_data['chan'][c_id]))
			commands(bot, update, chat_id=query.message.chat_id, chan=parse_data['chan'][c_id], data=lastcmd.get(query.message.chat_id))
		except Exception:
			pass
	elif json.loads(query.data.replace("'", "\""))['data'] == "Download":
		bot.editMessageReplyMarkup(query.message.chat_id, query.message.message_id)
		try:
			idd(bot, update, chat_id=query.message.chat_id, tags='id:'+str(json.loads(query.data.replace("'", "\""))['id']))
			bot.answer_callback_query(query.id, text='Downloading')
		except Exception as e:
			traceback.print_exc()

@run_async
def inline(bot, update): #Inline Handler & Parser
	query = update.inline_query.query
	offset = update.inline_query.offset
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
					type='photo',
					id=uuid4(),
					photo_url=post['sample_url'],
					photo_width=post['width']*6,
					photo_height=post['height']*6,
					thumb_url=post['preview_url']),)
		if lposts >=50:
			bot.answerInlineQuery(update.inline_query.id, results=inlinequery, next_offset=query + offset)
		else:
			bot.answerInlineQuery(update.inline_query.id, results=inlinequery)
		inlinequery.clear()
	else:
		client = Moebooru('yandere')
		posts = client.post_list(tags=query, limit=50, page=int(offset.split('page=', 1)[1]))
		lposts = len(posts)
		inlinequery = list()
		for post in posts:
			inlinequery.append(InlineQueryResultPhoto(
					type='photo',
					id=uuid4(),
					photo_url=post['sample_url'],
					photo_width=post['width']*6,
					photo_height=post['height']*6,
					thumb_url=post['preview_url']),)
		if lposts >=50:
			bot.answerInlineQuery(update.inline_query.id, results=inlinequery, next_offset=query + offset)
		else:
			bot.answerInlineQuery(update.inline_query.id, results=inlinequery)
		inlinequery.clear()

def log(bot, name, chat_id, user_id, username, command, c_type):
	bot.sendMessage(chat_id='-57197611', text='#log @anime\_bot #%s\n\n*Command:* %s\n\n*Name:* %s\n*Username:* @%s\n\n*Chat ID:* %s\n*User ID:* %s\n' %(c_type, command, name, username, chat_id, user_id), parse_mode=ParseMode.MARKDOWN)

@run_async
def ping(bot, update):
	bot.sendMessage(update.message.chat_id, text="Pong", reply_to_message_id=update.message.message_id)

@run_async
def info(bot, update, **kwargs):
	if update.message.from_user.id in superusers:
		group = '`Sudo`'
	else:
		group = 'User'
	bot.sendMessage(update.message.chat_id, text='Name: ' + str(update.message.from_user.first_name) + '\nUsername: @' + str(update.message.from_user.username) + '\n\nChat ID: ' + str(update.message.chat.id) + '\nUser ID: ' + str(update.message.from_user.id) + '\nLanguage: ' + str(update.message.from_user.language_code) + "\n\nType: " + str(update.message.chat.type) +'\nGroup: ' + group, reply_to_message_id=update.message.message_id, parse_mode=ParseMode.MARKDOWN)

@run_async
def error(bot, update, error):
	try:
		bot.sendMessage('-57197611', 'Update "%s" caused error "%s"' % (update, error))
	except Exception:
		traceback.print_exc()

def main(bot=None):
	token = bot_token
	updater = Updater(token)
	for item in parse_data['items']:
		updater.dispatcher.add_handler(CommandHandler(item, commands))
	updater.dispatcher.add_handler(CommandHandler('help', start))
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('ping', ping))
	updater.dispatcher.add_handler(CommandHandler('info', info))
	updater.dispatcher.add_handler(MessageHandler(Filters.text, messages))
	updater.dispatcher.add_handler(CallbackQueryHandler(callback))
	updater.dispatcher.add_handler(InlineQueryHandler(inline))

	updater.dispatcher.add_error_handler(error)
	try:
		updater.start_polling(clean=True, timeout=120)

		updater.idle()
	except Exception:
		traceback.print_exc()
	finally:
		sys.exit(1)

if __name__ == '__main__':
	main()

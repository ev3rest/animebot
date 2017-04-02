#----------------------------------
# Developer: Digital Entropy
# Program: Anime Bot 3.0 for Telegram
# (c) Digital Entropy 2017
# License: Proprietary Software
#-----------------------------------
from __future__ import unicode_literals
import logging
import botan
import os
import time
import traceback
from random import randint
import urllib.request
from uuid import uuid4
from time import sleep
import schedule
from pathlib import Path
import random
import json
from collections import defaultdict
import gc
import requests
import datetime
import json
from pybooru import Moebooru, Danbooru
from retrying import retry
from telegram import Emoji, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InlineQueryResultPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, Filters
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
						   '%(message)s',
					level=logging.WARNING)

gc.enable() #Garbage collector

superusers=[47571378]

#ikeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Support Me", url='https://patreon.com/ev3rest')], [InlineKeyboardButton("More", callback_data='More')]])
bkeyboard = ReplyKeyboardMarkup(
			[[KeyboardButton("/anime"), KeyboardButton("/ecchi")], [KeyboardButton("/hentai (18+)"), KeyboardButton("/uncensored (18+)")], [KeyboardButton("/yuri (18+)"), KeyboardButton("/loli (18+)"), KeyboardButton("/neko")], [KeyboardButton("/wallpaper")]], 
			one_time_keyboard=False)

items = ['anime', 'hentai', 'loli', 'yuri', 'ecchi', 'neko', 'uncensored']


#VARIABLES

lastcmd = {}
x = {'1':{'url':[], 'id':[]}, '2':{'url':[], 'id':[]}, '3':{'url':[], 'id':[]}, '4':{'url':[], 'id':[]}, '5':{'url':[], 'id':[]}, '6':{'url':[], 'id':[]}, '7':{'url':[], 'id':[]}, '8':{'url':[], 'id':[]}, '9':{'url':[], 'id':[]}}
d = {'1': {'data': '', 'url': ''}, '2': {'data': '', 'url': ''}, '3': {'data': '', 'url': ''}, '4': {'data': '', 'url': ''}, '5': {'data': '', 'url': ''}, '6': {'data': '', 'url': ''}, '7': {'data': '', 'url': ''}, '8': {'data': '', 'url': ''}, '9': {'data': '', 'url': ''}}
parse_data = {'commands':['/anime', '/hentai', '/loli', '/yuri', '/ecchi', '/neko', '/uncensored', '/gif'], 'tags':['rating:s', 'rating:e', 'loli', 'yuri', 'rating:q', 'cat_ears', 'uncensored', 'animated_gif'], 'ch_id': ['1', '2', '3', '4', '5', '6', '7', '8'], 'chan':['@anime_channel', '@hentai_channel', '@channel_loli', '@yuri_channel', '@ecchi_channel', '@anime_channel', '@uncensored_channel', '@anime_channel']}

#TOKENS


bot_token = 'token'

botan_token = 'token'

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
				bot.sendMessage(update.message.chat_id, "Hey there!\nMy name is @anime_bot! I am your personal assistant in the anime world!\n\nUse the keyboard below to navigate the menu.\n\nFeeback: /feedback", reply_markup=bkeyboard)
			except Exception:
				traceback.print_exc()

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
		try:
			data = data.split(' ', 1)[0]
		except:
			pass
	c_id = parse_data['commands'].index(data)

	lastcmd[chat_id] = parse_data['commands'][c_id]
	ch_id = parse_data['ch_id'][c_id]


	if chan !=None:
		parser(bot, update, tags=parse_data['tags'][c_id], pages='50', chat_id=chat_id, info='Want more? Join %s!' % chan, ch_id=str(ch_id)) 
	else:
		parser(bot, update, tags=parse_data['tags'][c_id], pages='50', chat_id=chat_id, ch_id=str(ch_id))

	log(bot, name=source.from_user.first_name, username=source.from_user.username.replace('_', '\_'), chat_id=source.chat_id, user_id=source.from_user.id, command=data, c_type=c_type)

@run_async
def idd(bot, update, tags=None, chat_id=None):
	randomint = randint(1000, 10000000)
	try:
		bot.sendChatAction(chat_id, "upload_document")
		try:
			#client = Danbooru('danbooru', username='tiny_paw', api_key='5Kerabo7TiwzeHHwqoe0dd3ixrawZM_wWvCNg8Q_gT4')
			client = Moebooru('yandere')
			posts = client.post_list(tags=tags)
			for post in posts:
				urllib.request.urlretrieve(post['file_url'], "tmp/anime_bot_" + str(randomint) + ".jpg")
			ckeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Support Me", url='https://paypal.me/ev3rest')], [InlineKeyboardButton("More", callback_data="{'data':'More'}")]])
			reply_markup = ckeyboard
			photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
			bot.sendDocument(chat_id, photo, reply_markup=reply_markup)
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		except Exception:
			traceback.print_exc()
	except Exception:
		traceback.print_exc()

@run_async
#@retry
def parser(bot, update, tags, pages, chat_id, info=None, ch_id=None): #Usual parser for usual commands
	global x
	global p_id
	randomint = randint(1000, 10000000)
	bot.sendChatAction(chat_id, "upload_photo")
	#client = Danbooru('danbooru', username='tiny_paw', api_key='5Kerabo7TiwzeHHwqoe0dd3ixrawZM_wWvCNg8Q_gT4')
	client = Moebooru('yandere')
	try:
		randompage = randint(1, int(pages))
		if len(x[str(ch_id)]['url']) == 0:
			posts = client.post_list(tags=str(tags), page=randompage, limit=40)
			for post in posts:
				#fileurl = 'http://danbooru.donmai.us' + post['file_url']
				fileurl = post['sample_url']
				x[str(ch_id)]['url'].append(fileurl)
				x[str(ch_id)]['id'].append(post['id'])
		try:
			urllib.request.urlretrieve(x[str(ch_id)]['url'][0], "tmp/anime_bot_" + str(randomint) + ".jpg")
		except Exception:
			traceback.print_exc()
		ikeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Support Me", url='https://paypal.me/ev3rest')], [InlineKeyboardButton("Download", callback_data="{'data':'Download', 'id':%s}"%x[str(ch_id)]['id'][0])], [InlineKeyboardButton("More", callback_data="{'data':'More', 'c_id':%s}"%ch_id)]])
		reply_markup = ikeyboard
		photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
		bot.sendPhoto(chat_id, photo, reply_markup=reply_markup)
		os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		x[str(ch_id)]['url'].pop(0)
		x[str(ch_id)]['id'].pop(0)
		botanio(bot, update, message=update.message, uid=chat_id, event_name=lastcmd[chat_id])

	except Exception:
		traceback.print_exc()
		bot.sendMessage(chat_id, 'Oops... Something went wrong, please call the command again!')
		try:
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		except:
			pass
		x[str(ch_id)]['url'].pop(0)
		x[str(ch_id)]['id'].pop(0)

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
			traceback.print_exc()
	elif json.loads(query.data.replace("'", "\""))['data'] == "Download":
		bot.editMessageReplyMarkup(query.message.chat_id, query.message.message_id)
		try:
			idd(bot, update, chat_id=query.message.chat_id, tags='id:'+str(json.loads(query.data.replace("'", "\""))['id']))
			bot.answer_callback_query(query.id, text='Downloading')
		except Exception as e:
			traceback.print_exc()

def inline(bot, update): #Inline Handler & Parser
	query = update.inline_query.query
	if query is None:
		query = 'rating:s'
		client = Moebooru('yandere')
		posts = client.post_list(tags=query, limit=50)
		lposts = len(posts)
		inlinequery = list()
		reply_markup = InlineKeyboardMarkup([InlineKeyboardButton("More", callback_data='More')])
		for post in posts:
			inlinequery.append(InlineQueryResultPhoto(
					type='photo',
					id=uuid4(),
					photo_url=post['file_url'],
					photo_width=post['preview_width']*6,
					photo_height=post['preview_height']*6,
					#reply_markup=reply_markup,
					thumb_url=post['sample_url']),)
		bot.answerInlineQuery(update.inline_query.id, results=inlinequery)
		inlinequery.clear()
	else:
		client = Moebooru('yandere')
		posts = client.post_list(tags=query, limit=50)
		lposts = len(posts)
		inlinequery = list()
		reply_markup = InlineKeyboardMarkup([InlineKeyboardButton("More", callback_data='More')])
		for post in posts:
			inlinequery.append(InlineQueryResultPhoto(
					type='photo',
					id=uuid4(),
					photo_url=post['file_url'],
					photo_width=post['preview_width']*6,
					photo_height=post['preview_height']*6,
					#reply_markup=reply_markup,
					thumb_url=post['preview_url']),)
		bot.answerInlineQuery(update.inline_query.id, results=inlinequery)
		inlinequery.clear()


def botanio(bot, update, message, event_name, uid):
	try:
		message_dict = update.message.to_dict()
	except:
		message_dict = "{}"
	try:
		print (botan.track(botan_token, uid, message_dict, event_name))
	except Exception as e:
		traceback.print_exc()

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
	bot.sendMessage(update.message.chat_id, text='Name: ' + str(update.message.from_user.first_name) + '\nUsername: @' + str(update.message.from_user.username) + '\n\nChat ID: ' + str(update.message.chat.id) + '\nUser ID: ' + str(update.message.from_user.id) + '\n\nGroup: ' + group, reply_to_message_id=update.message.message_id, parse_mode=ParseMode.MARKDOWN)

@run_async
def feedback(bot, update):
	try:
		s=update.message.text
		s = s.split(' ', 1)[1]
		bot.sendMessage(-2059567, text='Feedback from ' + str(update.message.from_user.first_name) + ' ' + str(update.message.from_user.last_name) + '\n\nUsername: ' + str(update.message.from_user.username) + '\nCID: ' + str(update.message.from_user.id) + '\nUID: ' + str(update.message.chat_id) + '\n\nText: ' + s)
		sleep(2)
		bot.sendMessage(update.message.chat_id, text='Success! Your feedback has been sent!')
	except:
		bot.sendMessage(update.message.chat_id, text='Something went wrong :(\nAre you using /feedback <text>?')

@run_async
def error(bot, update, error):
	try:
		bot.sendMessage('-57197611', 'Update "%s" caused error "%s"' % (update, error))
	except Exception:
		traceback.print_exc()

def main():
	token = bot_token
	updater = Updater(token, workers=20)

	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('ping', ping))
	updater.dispatcher.add_handler(CommandHandler('info', info))
	updater.dispatcher.add_handler(CommandHandler('feedback', feedback))
	updater.dispatcher.add_handler(CallbackQueryHandler(callback))
	#updater.dispatcher.add_handler(InlineQueryHandler(inline))

	for item in items:
		updater.dispatcher.add_handler(CommandHandler(item, commands)) #1

	updater.dispatcher.add_error_handler(error)
	updater.start_polling(bootstrap_retries=1, clean=True)
	
	updater.idle()

if __name__ == '__main__':
	main()

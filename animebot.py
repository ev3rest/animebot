#----------------------------------
# Developer: Digital Entropy
# Program: Anime Bot for telegram
# (c) Digital Entropy 2016
# License: Proprietary Software
#-----------------------------------
from __future__ import unicode_literals
import logging

import botan
import os
import time
from random import randint
import urllib.request
from uuid import uuid4
from time import sleep
import schedule

import gc
import requests
import datetime

from pybooru import Pybooru
from retrying import retry

from telegram import Emoji, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InlineQueryResultPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, Filters
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
						   '%(message)s',
					level=logging.WARNING)

botan_token = '7oTjSCbwN:jplWuB34ASFa-3VIiLSg8m'
gc.enable() #Garbage collector

globalarray = {}

superusers=[47571378]

ikeyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Support Me", url='https://patreon.com/ev3rest')], [InlineKeyboardButton("Download", callback_data='Download')], [InlineKeyboardButton("More", callback_data='More')]])
bkeyboard = ReplyKeyboardMarkup(
			[[KeyboardButton("Anime"), KeyboardButton("Ecchi")], [KeyboardButton("Hentai (18+)"), KeyboardButton("Uncensored (18+)")], [KeyboardButton("Yuri (18+)"), KeyboardButton("Loli (18+)"), KeyboardButton("Neko")], [KeyboardButton("Wallpaper")]], 
			one_time_keyboard=False)

lastcmd = {}

#BLOCK: Commands
@run_async
def start(bot, update, **kwargs):
	s = update.message.text
	if "ihelp" in s:
		ihelp(bot, update)
	else:
		try:
			s = s.split(' ', 1)[1]
			idd(bot, update, chat_id=update.message.chat_id, tags=s)
		except Exception as e:
			try:
				reply_markup = bkeyboard
				photohi = open("/ev3rest/bots/animebot/sys/girl.gif", 'rb')
				bot.sendDocument(update.message.chat_id, photohi, caption="Hey there!\nMy name is @anime_bot! I am your personal assistant in the anime world!\n\nUse the keyboard below to navigate the menu.", reply_markup=reply_markup)
			except Exception as e:
				print (e)

@run_async
def help(bot, update, **kwargs):
	try:
		reply_markup = bkeyboard
		photohi = open("/ev3rest/bots/animebot/sys/girl.gif", 'rb')
		bot.sendDocument(update.message.chat_id, photohi, caption="Hey there!\nMy name is @anime_bot! I am your personal assistant in the anime world!\n\nUse the keyboard below to navigate the menu.", reply_markup=reply_markup)
	except Exception as e:
		print (e)

@run_async
def ihelp(bot, update, **kwargs): #Inline help
	try:
		video = open("sys/inline.mp4", 'rb')
		bot.sendDocument(update.message.chat_id, video, parse_mode=ParseMode.MARKDOWN)
		sleep(1)
		bot.sendMessage(update.message.chat_id, 
'''
*Inline Usage:*
@anime\_bot <tag>

_Example:_
`@anime_bot kantai_collection`
''', parse_mode=ParseMode.MARKDOWN)
	except Exception as e:
		print (e)

@run_async
def anime(bot, update, chat_id=None, chan=None):
	tags = "rating:s"
	pages = "177840"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/anime"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan) 
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/anime")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/anime")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/anime")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/anime")
@run_async
def hentai(bot, update, chat_id=None, chan=None):
	tags = "rating:e"
	pages = "28280"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/hentai"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/hentai")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/hentai")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/hentai")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/hentai")
@run_async
def ecchi(bot, update, chat_id=None, chan=None):
	tags = "rating:q"
	pages = "105600"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/ecchi"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/ecchi")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/ecchi")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/ecchi")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/ecchi")
@run_async
def uncensored(bot, update, chat_id=None, chan=None):
	tags = "uncensored"
	pages = "4080"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/uncensored"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/uncensored")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/uncensored")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/uncensored")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/uncensored")
@run_async
def yuri(bot, update, chat_id=None, chan=None):
	tags = "yuri"
	pages = "4880"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/yuri"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/yuri")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/yuri")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/yuri")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/yuri")
@run_async
def loli(bot, update, chat_id=None, chan=None):
	tags = "loli"
	pages = "14480"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/loli"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/loli")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/loli")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/loli")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/loli")

@run_async
def neko(bot, update, chat_id=None, chan=None):
	tags = "animal_ears"
	pages = "20720"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/neko"
	except:
		pass
	if chan !=None:
		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/anime")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/anime")
	else:

		parser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/neko")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/neko")

@run_async
def wallpaper(bot, update, chat_id=None, chan=None):
	tags = "width:2560 height:1440 rating:s"
	pages = "100"
	if chat_id == None:
		chat_id = update.message.chat_id
	try:
		lastcmd[update.message.chat_id]="/wallpaper"
	except:
		pass
	if chan !=None:
		wallparser(bot, update, tags=tags, pages=pages, chat_id=chat_id, info='Want more? Join %s!' % chan)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/wallpaper")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/wallpaper")
	else:

		wallparser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/wallpaper")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/wallpaper")

### END

@run_async
def tag(bot, update, chat_id=None):
		if chat_id == None:
			chat_id = update.message.chat_id
		else:
			pass
		try:
			tags = update.message.text.split(' ', 1)[1]
		except Exception as e:
			try:
				tags = lastcmd[update.callback_query.message.chat_id].split(' ', 1)[1]
			except:
				bot.sendMessage(chat_id, "Please, use `/tag <tag>` instead.", parse_mode=ParseMode.MARKDOWN)
		pages = "30"

		try:
			lastcmd[update.message.chat_id]=update.message.text
		except Exception as e:
			pass
		noparser(bot, update, tags=tags, pages=pages, chat_id=chat_id)
		if update.message != None:
			botanio(bot, update, message=update.message, uid=chat_id, event_name="/tag")
		else:
			botanio(bot, update, message = None, uid=chat_id, event_name="/tag")

@run_async
@retry
def parser(bot, update, tags, pages, chat_id, info=None): #Usual parser for usual commands
	bot.sendChatAction(chat_id, "upload_photo")
	client = Pybooru('Yandere')
	try:
		randompage = randint(1, int(pages))
		posts = client.posts_list(tags=str(tags), limit=1, page=str(randompage))
		for post in posts:
			tmp_data = "Uploader: " + post['author']  + "\nID: " + str(post['id'])
			globalarray[chat_id] = dict(data=tmp_data)
		photo = post['file_url']
		reply_markup = ikeyboard
		if info != None:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=info + '\n' + tmp_data)
		else:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=tmp_data)
	except Exception as e:
		print(e)
		print("Retrying...")
		print (parser(bot, update, tags, pages, chat_id))

@run_async
def noparser(bot, update, tags, pages, chat_id, info=None): #Parser without retry loop (to prevent infinte exception)
	bot.sendChatAction(chat_id, "upload_photo")
	client = Pybooru('Yandere')
	randomint = randint(1000, 10000000)
	try:
		randompage = randint(1, int(pages))
		posts = client.posts_list(tags=str(tags), limit=1, page=str(randompage))
		for post in posts:
			urllib.request.urlretrieve(post['file_url'], "tmp/anime_bot_" + str(randomint) + ".jpg")
			tmp_data = "Uploader: " + post['author']  + "\nID: " + str(post['id'])
			globalarray[chat_id] = dict(data=tmp_data)
		photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
		reply_markup = ikeyboard
		if info != None:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=info + '\n' + tmp_data)
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		else:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=tmp_data)
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
	except Exception as e:
		print(e)
@retry
@run_async
def wallparser(bot, update, tags, pages, chat_id, info=None): #Wallpaper parser
	bot.sendChatAction(chat_id, "upload_photo")
	client = Pybooru('Yandere')
	try:
		randompage = randint(1, int(pages))
		posts = client.posts_list(tags=str(tags), limit=1, page=str(randompage))
		for post in posts:
			tmp_data = "Uploader: " + post['author']  + "\nID: " + str(post['id'])
			globalarray[chat_id] = dict(data=tmp_data)
		photo = post['file_url']
		reply_markup = ikeyboard
		if info != None:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=info + '\n' + tmp_data)
		else:
			bot.sendPhoto(chat_id, photo, reply_markup=reply_markup, caption=tmp_data)
	except Exception as e:
		print(e)
		print("Retrying...")
		print (wallparser(bot, update, tags, pages, chat_id))

@run_async
def callback(bot, update): #Callback handler
    query = update.callback_query
    if query.data == "Download":
    	bot.editMessageReplyMarkup(query.message.chat_id, query.message.message_id)
    	try:
    		image_id = str(globalarray[query.message.chat_id]).split("ID: ", 1)[1]
    		image_id = image_id.split("\'", 1)[0]
    		idd(bot, update, chat_id=query.message.chat_id, tags=image_id)
    	except Exception as e:
    		print(e)
    elif query.data == "More":
    	bot.editMessageReplyMarkup(query.message.chat_id, query.message.message_id)
    	if lastcmd.get(query.message.chat_id) == '/anime':
    		anime(bot, update, chat_id=query.message.chat_id, chan='@anime_channel')
    	elif lastcmd.get(query.message.chat_id) == '/hentai':
    		hentai(bot, update, chat_id=query.message.chat_id, chan='@hentai_channel')
    	elif lastcmd.get(query.message.chat_id) == '/ecchi':
    		ecchi(bot, update, chat_id=query.message.chat_id, chan='@ecchi_channel')
    	elif lastcmd.get(query.message.chat_id) == '/uncensored':
    		uncensored(bot, update, chat_id=query.message.chat_id, chan='@uncensored_channel')
    	elif lastcmd.get(query.message.chat_id) == '/yuri':
    		yuri(bot, update, chat_id=query.message.chat_id, chan='@yuri_channel')
    	elif lastcmd.get(query.message.chat_id) == '/loli':
    		loli(bot, update, chat_id=query.message.chat_id, chan='@loli_channel')
    	elif lastcmd.get(query.message.chat_id) == '/neko':
    		neko(bot, update, chat_id=query.message.chat_id, chan='@anime_channel')
    	elif lastcmd.get(query.message.chat_id) == '/wallpaper':
    		wallpaper(bot, update, chat_id=query.message.chat_id, chan='@anime_channel')
    	elif str(lastcmd.get(query.message.chat_id)).split(' ', 1)[0] == '/tag':
    		tag(bot, update, chat_id=query.message.chat_id)
    	else:
    		bot.sendMessage(query.message.chat_id, 'Try calling command again!')

@run_async
def text(bot, update):
    if update.message.text == "Anime": #Keyboard handler
    	anime(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Hentai (18+)":
    	hentai(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Uncensored (18+)":
    	uncensored(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Yuri (18+)":
    	yuri(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Loli (18+)":
    	loli(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Ecchi":
    	ecchi(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Neko":
    	neko(bot, update, chat_id=update.message.chat_id)
    elif update.message.text == "Wallpaper":
    	wallpaper(bot, update, chat_id=update.message.chat_id)
    else:
    	pass
    	
def inline(bot, update): #Inline Handler & Parser
	query = update.inline_query.query
	if query is None:
		query = 'rating:s'
		client = Pybooru('Yandere')
		posts = client.posts_list(tags=query, limit=50)
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
		bot.answerInlineQuery(update.inline_query.id, results=inlinequery, switch_pm_text="Help", switch_pm_parameter="ihelp")
		inlinequery.clear()
	else:
		client = Pybooru('Yandere')
		posts = client.posts_list(tags=query, limit=50)
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
		bot.answerInlineQuery(update.inline_query.id, results=inlinequery, switch_pm_text="Help", switch_pm_parameter="ihelp")
		inlinequery.clear()

	
@run_async
def idd(bot, update, tags=None, chat_id=None):
	randomint = randint(1000, 10000000)
	try:
		bot.sendChatAction(chat_id, "upload_document")
		tags = update.message.text.split(' ', 1)[1]
		chat_id = update.message.chat_id
		try:
			client = Pybooru('Yandere')
			posts = client.posts_list(tags="id:"+str(tags), limit=1)
			for post in posts:
				urllib.request.urlretrieve(post['file_url'], "tmp/anime_bot_" + str(randomint) + ".jpg")
				tmp_data = "Uploader: " + post['author']  + "\nID: " + str(post['id'])
				globalarray[chat_id] = dict(data=tmp_data)
			photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
			reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("More", callback_data='More')]])
			bot.sendDocument(chat_id, photo, reply_markup=reply_markup)
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		except Exception as e:
			print(e)
	except:
		bot.sendChatAction(chat_id, "upload_document")
		client = Pybooru('Yandere')
		try:
			posts = client.posts_list(tags="id:"+str(tags), limit=1)
			for post in posts:
				urllib.request.urlretrieve(post['file_url'], "tmp/anime_bot_" + str(randomint) + ".jpg")
				tmp_data = "Uploader: " + post['author']  + "\nID: " + str(post['id'])
				globalarray[chat_id] = dict(data=tmp_data)
			photo = open('tmp/anime_bot_' + str(randomint) + ".jpg", 'rb')
			reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("More", callback_data='More')]])
			bot.sendDocument(chat_id, photo, reply_markup=reply_markup)
			os.remove('tmp/anime_bot_' + str(randomint) + ".jpg")
		except Exception as e:
			print(e)

@run_async
def su(bot, update): #Sudo commands from sudo list
	if update.message.from_user.id in superusers:
		try:
			bot.sendMessage(superusers[0], '''Sudo:
				/ev3start
				/ev3stop
				/mustart
				/mustop
				/clear''')
		except Exception as e:
			print (e)
	else:
		pass
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

#BLOCK: System

@run_async
def ev3rest_start(bot, update):
	if update.message.from_user.id in superusers:
		try:
			os.system("screen -d -m python3 /ev3rest/bots/ev3restbot/ev3rest.py")
			bot.sendMessage(update.message.chat_id, "Success", reply_to_message=update.message.message_id)
		except Exception as e:
			bot.sendMessage(update.message.chat_id, str(e))
	else:
		pass
@run_async
def ev3rest_stop(bot, update):
	if update.message.from_user.id in superusers:
		try:
			os.system("pkill -f /ev3rest/bots/ev3restbot/ev3rest.py")
			bot.sendMessage(update.message.chat_id, "Success", reply_to_message=update.message.message_id)
		except Exception as e:
			bot.sendMessage(update.message.chat_id, str(e))
	else:
		pass
@run_async
def music_start(bot, update):
	if update.message.from_user.id in superusers:
		try:
			os.system("screen -d -m python3 /ev3rest/bots/musicavebot/music.py")
			bot.sendMessage(update.message.chat_id, "Success", reply_to_message=update.message.message_id)
		except Exception as e:
			bot.sendMessage(update.message.chat_id, str(e))
	else:
		pass
@run_async
def music_stop(bot, update):
	if update.message.from_user.id in superusers:
		try:
			os.system("pkill -f /ev3rest/bots/musicavebot/music.py")
			bot.sendMessage(update.message.chat_id, "Success", reply_to_message=update.message.message_id)
		except Exception as e:
			bot.sendMessage(update.message.chat_id, str(e))
	else:
		pass

@run_async
def clear(bot, update):
	if update.message.from_user.id in superusers:
		try:
			os.system("echo 3 > /proc/sys/vm/drop_caches")
			bot.sendMessage(update.message.chat_id, "Success", reply_to_message=update.message.message_id)
		except Exception as e:
			bot.sendMessage(update.message.chat_id, str(e))
	else:
		pass

@run_async
def mes(bot, update):
	if update.message.from_user.id in superusers:
		try:
			s = update.message.text
			raw_text = s.split(' ', 1)[1]
			cid = raw_text.split(' ', 1)[0]
			text = raw_text.split(' ', 1)[1]
			try:
				bot.sendMessage(cid, text)
				bot.sendMessage(superusers[1], "Success")
			except:
				bot.sendMessage(superusers[1], "Error")
		except Exception as e:
			print(e)
			bot.sendMessage(superusers[1], e)


def error(bot, update, error):
	logging.warning('Update "%s" caused error "%s"' % (update, error))

def botanio(bot, update, message, event_name, uid):
	try:
		message_dict = update.message.to_dict()
	except:
		message_dict = "{}"
	try:
		print (botan.track(botan_token, uid, message_dict, event_name))
	except Exception as e:
		print(e)

def main():
	token = "106653739:AAF0TdCoxF3qpfU4RrBJbz6lJFCEMDNAn94"
	updater = Updater(token, workers=20)

	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('help', help))

	updater.dispatcher.add_handler(CommandHandler('anime', anime))
	updater.dispatcher.add_handler(CommandHandler('hentai', hentai))
	updater.dispatcher.add_handler(CommandHandler('ecchi', ecchi))
	updater.dispatcher.add_handler(CommandHandler('uncensored', uncensored))
	updater.dispatcher.add_handler(CommandHandler('yuri', ecchi))
	updater.dispatcher.add_handler(CommandHandler('loli', loli))
	updater.dispatcher.add_handler(CommandHandler('neko', neko))
	updater.dispatcher.add_handler(CommandHandler('wallpaper', wallpaper))

	updater.dispatcher.add_handler(CommandHandler('id', idd))

	updater.dispatcher.add_handler(CommandHandler('tag', tag))

	updater.dispatcher.add_handler(CommandHandler('ping', ping))
	updater.dispatcher.add_handler(CommandHandler('info', info))

	updater.dispatcher.add_handler(CommandHandler('su', su))
	updater.dispatcher.add_handler(CommandHandler('feedback', feedback))

	updater.dispatcher.add_handler(CommandHandler("ev3start", ev3rest_start))
	updater.dispatcher.add_handler(CommandHandler("ev3stop", ev3rest_stop))
	updater.dispatcher.add_handler(CommandHandler("mustart", music_start))
	updater.dispatcher.add_handler(CommandHandler("mustop", music_stop))
	updater.dispatcher.add_handler(CommandHandler("clear", clear))
	updater.dispatcher.add_handler(CommandHandler("mes", mes))

	updater.dispatcher.add_handler(CallbackQueryHandler(callback))
	updater.dispatcher.add_handler(MessageHandler(Filters.text, text))
	updater.dispatcher.add_handler(InlineQueryHandler(inline))

	updater.dispatcher.add_error_handler(error)
	updater.start_polling(bootstrap_retries=4, clean=True)
	


	updater.idle()

if __name__ == '__main__':
	main()
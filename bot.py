import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import ChatActions
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ParseMode
from pybooru import Moebooru, Danbooru
import traceback
import urllib.request
import os
from random import randint
from datatypes import get_commands, connect_object, get_objects
from utils import normalcaption
from keyboardmaker import normalkeyboard, callback_cb
from enums import CallbackCommands
import parser

logging.basicConfig(level=logging.INFO)

API_TOKEN = '192818686:AAFiq8MarYlT2Ztui0qEUb8B0qmkGOAvQYY'
#----------------------------------
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
#----------------------------------

commands = get_commands()

@dp.message_handler(commands=(commands))
async def command_handler(message: types.Message, post=None, container_index = None):
	photo = ''
	request_type = CallbackCommands.NEXT
	channel = None
	if post == None:
		if container_index == None:
			data = await connect_object(1, message.text[1:int(message.entities[0].length)])
			container = data[1]
			container_index = data[0]
		else:
			container = get_objects()[int(container_index)]
		channel = container.channel
		post = parser.get_post(pages = container.pages, tags = container.get_tags())
		photo = post['sample_url']
	else:
		request_type = CallbackCommands.DOWNLOAD
	photo = post['file_url']
	caption = normalcaption(post = post, channel = channel)
	reply_markup = await normalkeyboard(post_id = post['id'], container_index = container_index)
	if request_type == CallbackCommands.DOWNLOAD:
		reply_markup['inline_keyboard'][1].pop(0)
		await message.answer_document(document=photo, reply_markup = reply_markup)
		return
	await message.answer_photo(photo=photo, caption = caption, parse_mode=ParseMode.HTML, reply_markup = reply_markup)
		

@dp.callback_query_handler(callback_cb.filter(function = CallbackCommands.NEXT))
async def callback_next(query: types.CallbackQuery, callback_data: dict):
	await query.message.edit_reply_markup()
	await command_handler(message = query.message, container_index = callback_data['container_index'])

@dp.callback_query_handler(callback_cb.filter(function = CallbackCommands.DOWNLOAD))
async def callback_download(query: types.CallbackQuery, callback_data: dict):
	await query.message.edit_reply_markup()
	post = parser.get_post(post_id=callback_data['value'])
	await command_handler(message = query.message, post = post, container_index = callback_data['container_index'])

# @dp.message_handler()
# async def message_handler(message: types.Message):
# 	container = connect_object(1, message.text[1:int(message.entities[0].length)])
# 	post = parser.get_post(pages = container.pages, tags = container.get_tags())
# 	photo = post['sample_url']
# 	caption = normalcaption(post = post, channel = container.channel)
# 	reply_markup = normalkeyboard()
# 	await message.answer_photo(photo=photo, caption = caption, parse_mode=ParseMode.HTML, reply_markup = reply_markup)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

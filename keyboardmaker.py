from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from enums import CallbackCommands

callback_cb = CallbackData('i', 'function', 'container_index', 'value')

async def normalkeyboard(post_id, container_index):
	reply_markup = InlineKeyboardMarkup()
	text_and_data = (
		('→ Next', container_index),
	)
	row_btns = (InlineKeyboardButton(text, callback_data=callback_cb.new(function=CallbackCommands.NEXT, container_index=container_index, value = container_index)) for text, data in text_and_data)
	reply_markup.row(*row_btns)
	text_and_data = (
		('↧ Download', post_id),
	)
	row_btns = (InlineKeyboardButton(text, callback_data=callback_cb.new(function=CallbackCommands.DOWNLOAD, container_index = container_index, value = data)) for text, data in text_and_data)
	reply_markup.row(*row_btns)
	return reply_markup
from aiogram import types
from misc import dp
from classes.PictureCommands import *

@dp.callback_query_handler()
async def next(query: types.CallbackQuery, callback_data: dict):
	print("callback")
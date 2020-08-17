from aiogram import types
from misc import dp

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.reply('Start')

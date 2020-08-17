from misc import dp
from booru.api import Moebooru
from random import randint
from classes.PictureCommands import *
from keyboardmaker import *

@dp.message_handler(picture_commands)
async def commands(message: types.Message, params: dict):
    client = Moebooru('yande.re')
    page = randint(1, params['pages'])
    post = await client.get_post(page=page, tags=params['tags'])
    reply_markup = normalkeyboard(command_id=params['command_id'], post_id=post['id'])
    await message.answer_photo(photo=post['sample_url'], reply_markup=reply_markup)
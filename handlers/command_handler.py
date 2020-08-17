from misc import dp
from booru.api import MoeBooru
from random import randint
from classes.PictureCommands import *

@dp.message_handler(picture_commands)
async def commands(message: types.Message, params: dict):
    client = MoeBooru('yande.re')
    page = randint(1, params['pages'])
    post = await client.get_post(page=page, tags=params['tags'])
    await message.answer_photo(photo = post['sample_url'])
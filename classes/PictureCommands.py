from aiogram import types
from aiogram.dispatcher.filters import Command, Text, Filter
from typing import List

class PictureCommand(Filter):
    commands_num = 0
    def __new__(cls, *args, **kwargs):
        PictureCommand.commands_num+=1
        return super(PictureCommand, cls).__new__(cls)
    def __init__(self,
                 command: str,
                 text_command: str,
                 tags: List[str],
                 pages: int,
                 channel: str=None):
        self.command = command
        self.command_id = self.commands_num+1
        self.text_command = text_command
        self.channel = channel or 'anime_channel'
        self.tags = tags
        self.pages = pages

    def request_params(self):
        return dict(
            tags=' '.join(self.tags),
            pages=self.pages,
            command_id=self.command_id
        )

    def base_filter(self):
        return Command(commands=self.command) | Text(equals=self.text_command)

    async def check(self, message: types.Message):
        if await self.base_filter().check(message):
            return dict(params=self.request_params())

class PictureCommands(Filter):
    def __init__(self, *args: PictureCommand):
        self.picture_commands = args or []

    def add(self, picture_command: PictureCommand):
        self.picture_commands.append(picture_command)

    def get(self, command) -> PictureCommand:
        for picture_command in self.picture_commands:
            if picture_command.command == command:
                return picture_command

    async def check(self, message: types.Message):
        for picture_command in self.picture_commands:
            check_passed = await picture_command.check(message)
            if check_passed:
                return check_passed


picture_commands = PictureCommands(
    PictureCommand(
        command='anime',
        text_command='Anime',
        channel='anime_channel',
        tags=['rating:s'],
        pages=7658
    ),
    PictureCommand(
        command='hentai',
        text_command='Hentai (18+)',
        channel='hentai_channel',
        tags=['rating:e'],
        pages=1527
    ),
    PictureCommand(
        command='loli',
        text_command='Loli (18+)',
        channel='hentai_channel',
        tags=['loli'],
        pages=635
    ),
    PictureCommand(
        command='yuri',
        text_command='Yuri (18+)',
        channel='yuri_channel',
        tags=['yuri'],
        pages=252
    ),
    PictureCommand(
        command='ecchi',
        text_command='Ecchi (18+)',
        channel='channel_ecchi',
        tags=['rating:q'],
        pages=5622
    ),
    PictureCommand(
        command='neko',
        text_command='Neko',
        tags=['cat_ears'],
        pages=402
    ),
    PictureCommand(
        command='uncensored',
        text_command='Uncensored (18+)',
        channel='uncensored_channel',
        tags=['uncensored'],
        pages=367
    ),
    PictureCommand(
        command='wallpaper',
        text_command='Wallpaper',
        tags=['wallpaper'],
        pages=523
    ),
)
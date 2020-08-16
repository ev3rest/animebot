class Container:
	def __init__(self, type_id, tags, command_keys, message_keys, pages, channel=None):
		if channel == None:
			channel = 'anime_channel'
		self.type_id = type_id
		self.tags = tags
		self.command_keys = command_keys
		self.message_keys = message_keys
		self.channel = channel
		self.pages = pages

	def get_tags(self):
		return ' '.join(self.tags)
def get_objects():
	return [anime, hentai, loli, yuri, ecchi, neko, uncensored, wallpaper]

def get_commands():
	commands = []
	for i in get_objects():
		for j in i.command_keys:
			commands.append(j)
	return commands

async def get_messages():
	messages = []
	for i in get_objects():
		for j in i.message_keys:
			messages.append(j)
	return messages

async def connect_object(kind, key):
	if kind == 1:
		object_index = get_commands().index(key)
		objects = get_objects()
		return (object_index, objects[object_index])
	object_index = await get_messages().index(key)
	objects = get_objects()
	return (object_index, objects[object_index])

anime = Container(type_id = 1, tags = ['rating:s'], command_keys = ['anime'], message_keys = ['Anime'], pages = 7658)
hentai = Container(type_id = 2, tags = ['rating:e'], command_keys = ['hentai'], message_keys = ['Hentai (18+)'], channel = 'hentai_channel', pages = 1527)
loli = Container(type_id = 3, tags = ['loli'], command_keys = ['loli'], message_keys = ['Loli (18+)'], channel = 'hentai_channel', pages = 635)
yuri = Container(type_id = 4, tags = ['yuri'], command_keys = ['yuri'], message_keys = ['Yuri (18+)'], channel = 'yuri_channel', pages = 252)
ecchi = Container(type_id = 5, tags = ['rating:q'], command_keys = ['ecchi'], message_keys = ['Ecchi (18+)'], channel = 'channel_ecchi', pages = 5622)
neko = Container(type_id = 6, tags = ['cat_ears'], command_keys = ['neko'], message_keys = ['Neko (18+)'], channel = 'hentai_channel', pages = 402)
uncensored = Container(type_id = 7, tags = ['uncensored'], command_keys = ['uncensored'], message_keys = ['Uncensored (18+)'], channel = 'uncensored_channel', pages = 367)
wallpaper = Container(type_id = 8, tags = ['wallpaper'], command_keys = ['wallpaper'], message_keys = ['Wallpaper'], pages = 523)
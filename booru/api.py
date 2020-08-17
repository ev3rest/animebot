import aiohttp
import asyncio
from storage import *
try:
	import ujson as json
except:
	import json

storage = Storage()

class MoeBooru():
	def __init__(self, endpoint):
		self.endpoint = "https://" + endpoint

	async def get_post(self, page, tags):
		if not storage.get(tags):
			print("Empty for tags (%s)" % (tags))
			await self.populate_storage(page, tags)
		to_return = storage.get(tags)[0]
		storage.pop(tags, 0)
		return to_return

	async def populate_storage(self, page, tags):
		posts = await self.posts_list(page, tags)
		storage.populate(tags, posts)

	async def posts_list(self, page, tags) -> [{}]:
		path = '/post.json'
		base_url = self.endpoint
		params = {'limit': 40, 'page': page, 'tags': tags}
		return await self.request(base_url, path, params)

	# Basic aiohttp request
	async def request(self, base_url, path, params=None) -> {}:
		final_url = base_url + path
		async with aiohttp.ClientSession() as session:
			async with session.request('get', final_url, params=params) as response:
				return await response.json()
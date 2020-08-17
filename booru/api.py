import aiohttp

try:
	import ujson as json
except ImportError:
	import json
from typing import List, Union
from .storage import PostsStorage

storage = PostsStorage()


class MoeBooru:
	def __init__(self, endpoint):
		self.endpoint = "https://" + endpoint

	async def request(self, path, params=None) -> Union[List[dict], dict]:
		final_url = self.endpoint + path
		async with aiohttp.ClientSession() as session:
			async with session.request('get', final_url, params=params) as response:
				return await response.json()

	async def get_posts(self, page, tags) -> List[dict]:
		params = {'limit': 40, 'page': page, 'tags': tags}
		return await self.request('/post.json', params)

	async def get_post(self, page, tags):
		if not storage.get(tags):
			print("Empty for tags (%s)" % tags)
			posts = await self.get_posts(page, tags)
			storage.store(tags, posts)
		return storage.pop_first(tags)



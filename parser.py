from pybooru import Moebooru
from random import randint, shuffle
from datatypes import get_objects

posts = {}

for i in get_objects():
	posts[i.get_tags()] = []

async def retrieve_posts(tags, pages, limit):
	client = Moebooru('yandere')
	randompage = randint(1, pages)
	posts = client.post_list(tags = tags, page = randompage, limit = limit)
	return posts


def populate_posts(tags, pages, limit):
	global posts
	client = Moebooru('yandere')
	randompage = randint(1, pages)
	posts[tags] = await retrieve_posts(tags = tags, pages = pages, limit = limit)
	return posts

def get_post(tags=None, pages=None, post_id=None):
	if post_id != None:
		to_return = await retrieve_posts(tags = 'id:%s' %(post_id), pages = 1, limit=1)
		return to_return[0]
	if not posts[tags]: # If the array is empty, add new ones
		print("Empty for tags (%s). Populating..." % (tags))
		populate_posts(tags = tags, pages = pages, limit = 40)
	to_return = posts[tags][0]
	posts[tags].pop(0)
	return to_return
	
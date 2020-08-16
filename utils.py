def normalcaption(post, channel):
	caption = \
	'<b>Tags: </b>' + post['tags'] + \
	'\n<b>Uploader: </b>%s' % (post['author']) + \
	'\n<b>ID: </b><a href="https://t.me/anime_bot?start=%s">%s</a>' %(post['id'], post['id']) + \
	'\n<a href="%s">Source</a>' % (post['source']) + \
	'\n\nWanna see more? Join @%s' % (channel)
	return caption
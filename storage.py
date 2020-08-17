class Storage:
	data = {}
	def get(self, tags):
		return self.data.get(tags)

	def populate(self, tags, posts):
		self.data[tags] = posts

	def pop(self, tags, index):
		self.data[tags].pop(index)
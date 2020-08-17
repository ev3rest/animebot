class Storage:
	data = {}
	def get(self, tags):
		to_return = self.data.get(tags)
		self.data[tags].pop()
		return to_return
class PostsStorage:
    def __init__(self):
        self.posts = {}

    def store(self, key, data):
        self.posts[key] = data

    def get(self, key):
        return self.posts.get(key)

    def pop_first(self, key):
        return self.posts[key].pop(0)
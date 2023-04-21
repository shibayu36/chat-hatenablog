import hashlib


class Entry:
    def __init__(self, title, body, basename):
        self.title = title
        self.body = body
        self.basename = basename

    def content_hash(self):
        content = self.title + self.body
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

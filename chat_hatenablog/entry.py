import hashlib


class Entry:
    def __init__(self, title, body, basename):
        self.title = title
        self.body = body
        self.basename = basename

    def content_hash(self):
        return hashlib.sha256(self.body.encode('utf-8')).hexdigest()

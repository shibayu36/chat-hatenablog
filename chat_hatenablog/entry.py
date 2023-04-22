import hashlib


class Entry:
    def __init__(self, title: str, body: str, basename: str) -> None:
        self.title = title
        self.body = body
        self.basename = basename

    def content_hash(self) -> str:
        content = self.title + self.body
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

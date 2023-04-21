import hashlib
from chat_hatenablog.entry import Entry


def test_entry_init():
    entry = Entry("Test Title", "Test Body", "test-basename")
    assert entry.title == "Test Title"
    assert entry.body == "Test Body"
    assert entry.basename == "test-basename"


def test_entry_content_hash():
    entry = Entry("Test Title", "Test Body", "test-basename")
    assert entry.content_hash(
    ) == hashlib.sha256("Test TitleTest Body".encode('utf-8')).hexdigest()

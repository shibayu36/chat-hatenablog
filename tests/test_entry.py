from chat_hatenablog.entry import Entry


def test_entry_init():
    entry = Entry("Test Title", "Test Body", "test-basename")
    assert entry.title == "Test Title"
    assert entry.body == "Test Body"
    assert entry.basename == "test-basename"


def test_entry_content_hash():
    entry = Entry("Test Title", "Test Body", "test-basename")
    assert entry.content_hash(
    ) == 'ae6d8a1c07f438667618879eae74ffab84c236ea5d8ca52d5ca0523cc35e8bb9'

import pytest
from chat_hatenablog.vector_store import VectorStore


class TestVectorStore:
    def test_init(self):
        vector_store = VectorStore("./test_index.pkl")
        assert vector_store.index_file == "./test_index.pkl"
        assert vector_store.cache == {}

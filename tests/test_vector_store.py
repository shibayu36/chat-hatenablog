import pytest
from unittest.mock import patch
from chat_hatenablog.vector_store import VectorStore, create_embeddings


class TestVectorStore:
    def test_init(self):
        vector_store = VectorStore("./test_index.pkl")
        assert vector_store.index_file == "./test_index.pkl"
        assert vector_store.cache == {}

    @patch('chat_hatenablog.vector_store.create_embeddings')
    def test_add_record_new(self, mock_create_embeddings):
        mock_create_embeddings.return_value = [0.5, 0.5, 0.5]

        vector_store = VectorStore("./test_index.pkl")

        body, title, basename = "test body", "test title", "test_basename"
        vector_store.add_record(body, title, basename)
        mock_create_embeddings.assert_called_with(body)
        assert vector_store.cache == {
            body: ([0.5, 0.5, 0.5], title, basename)
        }, "the first record should be added"

        mock_create_embeddings.return_value = [0.2, 0.2, 0.2]
        body2, title2, basename2 = "test body2", "test title2", "test_basename2"
        vector_store.add_record(body2, title2, basename2)
        mock_create_embeddings.assert_called_with(body2)
        assert vector_store.cache == {
            body: ([0.5, 0.5, 0.5], title, basename),
            body2: ([0.2, 0.2, 0.2], title2, basename2)
        }, "the second record should be added"

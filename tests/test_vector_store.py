import os
import pickle
import tempfile
import pytest
from unittest.mock import patch
from chat_hatenablog.entry import Entry
from chat_hatenablog.vector_store import VectorStore, create_embeddings


class MockMarkdownTextSplitter:
    def split_text(self, text):
        return text.split(",")


class TestVectorStore:
    def test_init(self):
        vector_store = VectorStore("./test_index.pkl")
        assert vector_store.index_file == "./test_index.pkl"
        assert vector_store.cache == {}

    @patch('chat_hatenablog.vector_store.create_embeddings')
    def test_add_entry(self, mock_create_embeddings):
        vector_store = VectorStore("./test_index.pkl")
        vector_store.markdown_splitter = MockMarkdownTextSplitter()

        mock_create_embeddings.return_value = [0.5, 0.5]
        entry1 = Entry("test title1", "test body1", "test_basename1")
        vector_store.add_entry(entry1)
        assert vector_store.cache == {
            "test_basename1": {
                "content_hash": entry1.content_hash(),
                "title": "test title1",
                "embeddings_list": [{
                    "body": "test body1",
                    "embeddings": [0.5, 0.5]
                }]
            }
        }, "the first entry should be added"

        mock_create_embeddings.return_value = [0.3, 0.3]
        entry2 = Entry("test title2", "test body2", "test_basename2")
        vector_store.add_entry(entry2)
        assert vector_store.cache == {
            "test_basename1": {
                "content_hash": entry1.content_hash(),
                "title": "test title1",
                "embeddings_list": [{
                    "body": "test body1",
                    "embeddings": [0.5, 0.5]
                }]
            },
            "test_basename2": {
                "content_hash": entry2.content_hash(),
                "title": "test title2",
                "embeddings_list": [{
                    "body": "test body2",
                    "embeddings": [0.3, 0.3]
                }]
            },
        }, "the second entry should be added"

        mock_create_embeddings.return_value = [0.2, 0.2]
        updated_entry1 = Entry(
            "test title1", "test body1,updated", "test_basename1")
        vector_store.add_entry(updated_entry1)
        assert vector_store.cache == {
            "test_basename1": {
                "content_hash": updated_entry1.content_hash(),
                "title": "test title1",
                "embeddings_list": [
                    {
                        "body": "test body1",
                        "embeddings": [0.2, 0.2]
                    },
                    {
                        "body": "updated",
                        "embeddings": [0.2, 0.2]
                    }
                ]
            },
            "test_basename2": {
                "content_hash": entry2.content_hash(),
                "title": "test title2",
                "embeddings_list": [{
                    "body": "test body2",
                    "embeddings": [0.3, 0.3]
                }]
            },
        }, "the first entry should be updated"

    @patch('chat_hatenablog.vector_store.create_embeddings')
    def test_save(self, mock_create_embeddings):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "index.pkl")

            vector_store = VectorStore(temp_file_path)

            mock_create_embeddings.return_value = [0.1, 0.1]
            entry = Entry("test title1", "test body1", "test_basename1")
            vector_store.add_entry(entry)
            vector_store.save()

            saved_data = pickle.load(open(temp_file_path, "rb"))
            assert saved_data == {
                "test_basename1": {
                    "content_hash": entry.content_hash(),
                    "title": "test title1",
                    "embeddings_list": [{
                        "body": "test body1",
                        "embeddings": [0.1, 0.1]
                    }]
                },
            }

    @patch('chat_hatenablog.vector_store.create_embeddings')
    @patch('pickle.dump')
    def test_save_only_when_dirty(self, mock_create_embeddings, mock_pickle_dump):
        mock_create_embeddings.return_value = [0.1, 0.1]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "index.pkl")

            vector_store = VectorStore(temp_file_path)

            entry = Entry("test title1", "test body1", "test_basename1")
            vector_store.add_entry(entry)
            vector_store.save()
            assert mock_pickle_dump.call_count == 1

            vector_store.save()
            assert mock_pickle_dump.call_count == 1

            another_entry = Entry(
                "test title2", "test body2", "test_basename2")
            vector_store.add_entry(another_entry)
            vector_store.save()
            assert mock_pickle_dump.call_count == 2

            vector_store.add_entry(entry)
            vector_store.save()
            assert mock_pickle_dump.call_count == 2, "should not be called because the entry is not updated"

    @patch('chat_hatenablog.vector_store.create_embeddings')
    def test_get_sorted(self, mock_create_embeddings):
        vector_store = VectorStore("./test_index.pkl")

        vector_store.cache = {
            "test_basename1": {
                "content_hash": 'dummy_hash1',
                "title": "test title1",
                "embeddings_list": [
                    {
                        "body": "test body1",
                        "embeddings": [0.1, 0.1]
                    },
                    {
                        "body": "updated",
                        "embeddings": [0.2, 0.2]
                    }
                ]
            },
            "test_basename2": {
                "content_hash": 'dummy_hash2',
                "title": "test title2",
                "embeddings_list": [{
                    "body": "test body2",
                    "embeddings": [0.5, 0.5]
                }]
            },
        }

        mock_create_embeddings.return_value = [0.2, 0.2]
        assert vector_store.get_sorted('query1') == [
            (0.2, 'test body2', 'test title2', 'test_basename2'),
            (0.08000000000000002, 'updated', 'test title1', 'test_basename1'),
            (0.04000000000000001, 'test body1', 'test title1', 'test_basename1'),
        ]

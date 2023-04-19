import pickle
import time
import numpy as np
import os
from tenacity import retry, stop_after_attempt
import openai
from langchain.text_splitter import MarkdownTextSplitter


@retry(reraise=True, stop=stop_after_attempt(3))
def create_embeddings(text):
    res = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002")

    return res["data"][0]["embedding"]


class VectorStore:
    """
    VectorStore creates embeddings for each entry and stores them.

    The data structure is as follows:
    {
        "basename1": {
            "content_hash": "...",
            "title": "title1",
            "embeddings_list": [
                {"body": ..., "embeddings": [...]},
                {"body": ..., "embeddings": [...]},
            ],
        },
        "basename2": { ... },
    }
    """

    def __init__(self, index_file):
        self.index_file = index_file
        try:
            self.cache = pickle.load(open(self.index_file, "rb"))
        except FileNotFoundError as e:
            self.cache = {}

            # Prepare index directory
            index_dir = os.path.dirname(self.index_file)
            if not os.path.exists(index_dir):
                os.makedirs(index_dir)

        self.markdown_splitter = MarkdownTextSplitter(
            chunk_size=1000, chunk_overlap=0)

    def add_entry(self, entry):
        # Skip if the entry is not changed
        existing_entry_data = self.cache.get(entry.basename)
        if existing_entry_data is not None and existing_entry_data.get("content_hash") == entry.content_hash():
            return

        embeddings_list = []
        self.cache[entry.basename] = {
            "content_hash": entry.content_hash(),
            "title": entry.title,
            "embeddings_list": embeddings_list,
        }

        for chunk in self.markdown_splitter.split_text(entry.body):
            embeddings_list.append({
                "body": chunk,
                "embeddings": create_embeddings(chunk),
            })
            time.sleep(0.2)

    def save(self):
        pickle.dump(self.cache, open(self.index_file, "wb"))

    def get_sorted(self, query):
        q = np.array(create_embeddings(query))
        items = [
            [info['title'], embeddings_list['body'], basename,
                embeddings_list['embeddings']]
            for basename, info in self.cache.items()
            for embeddings_list in info.get('embeddings_list')
        ]
        buf = []
        for title, body, basename, embeddings in items:
            buf.append((q.dot(embeddings), body, title, basename))
        buf.sort(reverse=True)
        return buf

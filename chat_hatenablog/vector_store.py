import pickle
import time
import numpy as np
import os
from tenacity import retry, stop_after_attempt
import openai


@retry(reraise=True, stop=stop_after_attempt(3))
def create_embeddings(text):
    res = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002")

    return res["data"][0]["embedding"]


class VectorStore:
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

    def add_record(self, body, title, basename):
        if body not in self.cache:
            self.cache[body] = (create_embeddings(body), title, basename)
            time.sleep(0.2)

        return self.cache[body]

    def save(self):
        pickle.dump(self.cache, open(self.index_file, "wb"))

    def get_sorted(self, query):
        q = np.array(create_embeddings(query))
        buf = []
        for body, (v, title, basename) in self.cache.items():
            buf.append((q.dot(v), body, title, basename))
        buf.sort(reverse=True)
        return buf

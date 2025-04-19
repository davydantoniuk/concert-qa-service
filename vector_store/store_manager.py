import os
import faiss
import pickle

from qa.embedder import get_embedding

# Path where we store FAISS + metadata
INDEX_PATH = "vector_store/faiss_index"
META_PATH = "vector_store/meta.pkl"

# Global in-memory references
index = None
metadata_store = []

def load_vector_store():
    global index, metadata_store
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            metadata_store = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(384)  # 384 dims for 'all-MiniLM-L6-v2'
        metadata_store = []

def embed_and_store(text: str, metadata: dict = None):
    global index, metadata_store
    if index is None:
        load_vector_store()

    embedding = get_embedding(text)
    index.add(embedding.reshape(1, -1))
    metadata_store.append({
        "text": text,
        "metadata": metadata or {}
    })
    # Save index and metadata
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata_store, f)

def search_similar(query: str, top_k: int = 3):
    global index, metadata_store
    if index is None:
        load_vector_store()

    query_vector = get_embedding(query).reshape(1, -1)
    D, I = index.search(query_vector, top_k)

    results = []
    for idx in I[0]:
        if idx < len(metadata_store):
            results.append(metadata_store[idx])
    return results
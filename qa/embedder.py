from sentence_transformers import SentenceTransformer

# Use a small, performant model for embedding
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return EMBEDDING_MODEL.encode(text, convert_to_tensor=False)
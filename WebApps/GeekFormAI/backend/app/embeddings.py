from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def generate_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()

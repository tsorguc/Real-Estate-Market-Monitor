from sentence_transformers import SentenceTransformer
import torch

class Embedder:
    """
    Handles loading the sentence-transformer model and generating embeddings.
    Uses the all-MiniLM-L6-v2 model as per Lab 11 requirements.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load model once and reuse
        self.model = SentenceTransformer(model_name)
        print(f"Model '{model_name}' loaded successfully.")

    def generate_embeddings(self, texts):
        """
        Generates embeddings for a list of strings.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # normalize_embeddings=True ensures cosine similarity works correctly
        return self.model.encode(texts, normalize_embeddings=True)

    def combine_property_fields(self, row):
        """
        Helper function to combine property fields into a single text string before embedding.
        Equivalent to (title + overview + genres) in the movie project.
        """
        title = str(row.get('title', ''))
        description = str(row.get('description', ''))
        p_type = str(row.get('primary_genre', row.get('type', '')))
        
        return f"{title}. {description}. Category: {p_type}".strip()

def get_similarity_scores(emb_a, emb_b):
    """
    Demonstrates similarity calculations (cosine, dot product, Euclidean).
    As per Lab 11 Requirement 1.
    """
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    
    # Cosine Similarity
    cos_sim = cosine_similarity(emb_a.reshape(1, -1), emb_b.reshape(1, -1))[0][0]
    
    # Dot Product (if normalized, same as cosine)
    dot_prod = np.dot(emb_a, emb_b)
    
    # Euclidean Distance
    euclidean_dist = np.linalg.norm(emb_a - emb_b)
    
    return {
        "cosine_similarity": cos_sim,
        "dot_product": dot_prod,
        "euclidean_distance": euclidean_dist
    }

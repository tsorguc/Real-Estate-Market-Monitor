import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

try:
    from src.embeddings.embedder import Embedder, get_similarity_scores
    from src.embeddings.chroma_store import ChromaStore
    from src.embeddings.search_engine import SearchEngine
    from src.embeddings.hybrid_search import hybrid_search
    print("✅ Module Imports: SUCCESS")
except ImportError as e:
    print(f"❌ Module Imports: FAILED ({e})")
    sys.exit(1)

def verify():
    print("\n--- Lab 11 Final Verification ---")

    # 1. Embeddings & Similarity
    try:
        embedder = Embedder()
        texts = ["Property A", "Property B"]
        embs = embedder.generate_embeddings(texts)
        if embs.shape == (2, 384):
            print(f"✅ Requirement 1 (Embeddings Shape): SUCCESS {embs.shape}")
        
        scores = get_similarity_scores(embs[0], embs[1])
        if all(k in scores for k in ["cosine_similarity", "dot_product", "euclidean_distance"]):
            print("✅ Requirement 1 (Similarity Measures): SUCCESS")
    except Exception as e:
        print(f"❌ Requirement 1: FAILED ({e})")

    # 2. ChromaDB
    try:
        store = ChromaStore()
        count = store.count()
        if count > 0:
            print(f"✅ Requirement 2 (ChromaDB Population): SUCCESS ({count} records)")
        else:
            print("❌ Requirement 2 (ChromaDB Population): FAILED (Database empty)")
            
        # Metadata filtering check
        # Assuming we have some 'Office' types from your previous output
        filtered = store.query_semantic("office", n_results=1, where={"type": "Office"})
        if len(filtered['ids'][0]) > 0:
            print("✅ Requirement 2 (Metadata Filtering): SUCCESS")
        else:
            print("⚠️ Requirement 2 (Metadata Filtering): No results found for 'Office' (check data)")
    except Exception as e:
        print(f"❌ Requirement 2: FAILED ({e})")

    # 3. Search System
    try:
        df = pd.read_csv('data/processed/cleaned/cleaned_data.csv')
        searcher = SearchEngine(store, df, embedder)
        
        # Semantic search
        sem = searcher.semantic_search("modern space")
        # Keyword search
        key = searcher.keyword_search("office")
        # Hybrid search
        hyb = hybrid_search(sem, key)
        
        if len(sem) > 0 and len(key) > 0 and len(hyb) > 0:
            print("✅ Requirement 3 (Search Methods: Semantic, Keyword, Hybrid): SUCCESS")
        else:
            print("❌ Requirement 3: FAILED (One or more search methods returned no results)")
    except Exception as e:
        print(f"❌ Requirement 3: FAILED ({e})")

    # 4. Files check
    notebook_path = 'notebooks/lab11_embeddings.ipynb'
    if os.path.exists(notebook_path):
        print(f"✅ Requirement 5 (Notebook): SUCCESS")
    else:
        print(f"❌ Requirement 5 (Notebook): MISSING")

    print("\n🏁 Lab 11 Verification Complete!")

if __name__ == "__main__":
    verify()

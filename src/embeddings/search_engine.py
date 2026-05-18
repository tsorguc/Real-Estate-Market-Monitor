import pandas as pd
import numpy as np
from src.embeddings.embedder import Embedder
from src.embeddings.chroma_store import ChromaStore

class SearchEngine:
    """
    High-level search functions: semantic, keyword, and comparison.
    As per Lab 11 Requirement 3.
    """
    def __init__(self, chroma_store: ChromaStore, df: pd.DataFrame, embedder: Embedder):
        self.store = chroma_store
        self.df = df
        self.embedder = embedder

    def semantic_search(self, query, n_results=5, where=None):
        """
        Searches properties by meaning using ChromaDB.
        Encodes query locally using our Embedder.
        """
        # Encode query locally
        query_emb = self.embedder.generate_embeddings([query]).tolist()
        
        # Query using the pre-computed embedding
        results = self.store.query_semantic(query, n_results=n_results, where=where, query_embeddings=query_emb)
        
        # Convert results to a list of dicts for easier display
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append({
                "id": results['ids'][0][i],
                "document": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i]
            })
        return search_results

    def keyword_search(self, query, columns=['title', 'description'], n_results=5):
        """
        Simpler search method that looks for exact words inside columns.
        """
        query = query.lower()
        mask = np.column_stack([self.df[col].str.lower().str.contains(query, na=False) for col in columns]).any(axis=1)
        results_df = self.df[mask].head(n_results)
        
        return results_df.to_dict('records')

    def compare_search(self, query, n_results=5):
        """
        Runs both search methods on the same query and displays results side by side.
        """
        print(f"\n--- Comparing Search Methods for Query: '{query}' ---")
        
        semantic = self.semantic_search(query, n_results=n_results)
        keyword = self.keyword_search(query, n_results=n_results)
        
        print(f"\n[Semantic Search Results] (Found: {len(semantic)})")
        for res in semantic:
            print(f"- {res['metadata'].get('title', 'N/A')} (Dist: {res['distance']:.4f})")
            
        print(f"\n[Keyword Search Results] (Found: {len(keyword)})")
        for res in keyword:
            print(f"- {res.get('title', 'N/A')}")
            
        return semantic, keyword

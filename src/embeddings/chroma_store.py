from src.embeddings.embedder import Embedder
import chromadb
import os

class ChromaStore:
    """
    Manages all ChromaDB vector database operations.
    Enforces local embedding to avoid timeout-prone downloads.
    """
    def __init__(self, path="data/embeddings/chroma_db", collection_name="properties"):
        # Ensure path exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Initialize persistent client
        self.client = chromadb.PersistentClient(path=path)
        
        # Create or get collection with cosine similarity
        # We set embedding_function=None to disable ChromaDB's internal model downloads
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=None
        )
        
        # Initialize local embedder for internal use
        self.embedder = Embedder()
        print(f"ChromaDB collection '{collection_name}' initialized.")

    def add_properties(self, documents, metadatas, ids, embeddings=None):
        """
        Adds properties. If embeddings are missing, generates them locally.
        """
        if embeddings is None:
            print(f"🔄 Encoding {len(documents)} documents locally...")
            embeddings = self.embedder.generate_embeddings(documents).tolist()
            
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        print(f"Added {len(ids)} properties to ChromaDB.")

    def query_semantic(self, query_text, n_results=5, where=None, query_embeddings=None):
        """
        Performs semantic search. Automatically encodes query text locally
        if query_embeddings are not provided.
        """
        if query_embeddings is None and query_text:
            # Encode locally using our already-loaded model
            query_embeddings = self.embedder.generate_embeddings([query_text]).tolist()

        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where
        )

    def reset_collection(self, collection_name="properties"):
        """
        Resets/Deletes and recreates the collection.
        """
        try:
            self.client.delete_collection(name=collection_name)
            self.collection = self.client.create_collection(name=collection_name)
            print(f"Collection '{collection_name}' reset.")
        except Exception as e:
            print(f"Reset failed: {e}")

    def count(self):
        """Returns the number of documents in the collection."""
        return self.collection.count()

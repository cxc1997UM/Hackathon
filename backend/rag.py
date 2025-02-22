# rag.py
import os
import openai
import json
import numpy as np
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()  # Optional, if you're storing OPENAI_API_KEY in .env

class RAGEngine:
    """
    A simple RAG engine for grading:
      - Reads example grading style files (text/JSON).
      - Embeds them with OpenAI Embeddings.
      - Returns top-k examples relevant to the new assignment text.
    """

    def __init__(self, 
                 openai_api_key: str = None,
                 examples_dir: Path = Path("professor_examples"), 
                 model: str = "text-embedding-ada-002"):
        """
        :param openai_api_key: Your OpenAI API key.
        :param examples_dir: Path to directory with grading style examples.
        :param model: Embedding model name.
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.examples_dir = examples_dir
        self.model = model
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided or found in environment.")
        
        openai.api_key = self.openai_api_key
        
        # List of dicts: [{'text': str, 'embedding': np.array, 'filepath': str}, ...]
        self.examples = []
        
        # Load and embed examples at init
        self._load_and_embed_examples()

    def _load_and_embed_examples(self):
        """
        Loads all .txt or .json files from self.examples_dir,
        reads their content, and stores embeddings.
        """
        if not self.examples_dir.exists():
            print(f"Warning: Examples directory {self.examples_dir} not found.")
            return
        
        for file_path in self.examples_dir.glob("*"):
            if file_path.suffix.lower() in [".txt", ".json"]:
                text_content = file_path.read_text(encoding="utf-8").strip()
                
                embedding = self._embed_text(text_content)
                
                self.examples.append({
                    "text": text_content,
                    "embedding": embedding,
                    "filepath": str(file_path)
                })
        
        print(f"Loaded and embedded {len(self.examples)} example(s).")

    def _embed_text(self, text: str) -> np.ndarray:
        """
        Uses OpenAI to create an embedding vector from text.
        Returns a numpy array (shape depends on embedding model).
        """
        # The embedding API can handle up to ~8000 tokens of text (for ADA-002).
        response = openai.Embedding.create(
            model=self.model,
            input=text
        )
        vector = response["data"][0]["embedding"]
        return np.array(vector, dtype=np.float32)

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute the cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

    def get_similar_grading_examples(self, assignment_text: str, top_k: int = 2) -> List[Dict]:
        """
        Embeds the new assignment text and returns the top-k most similar
        examples from our stored professor examples.

        :param assignment_text: The student's assignment text to be graded.
        :param top_k: Number of examples to retrieve.
        :return: A list of example dicts with 'text' and 'filepath' (and 'similarity').
        """
        if not self.examples:
            return []
        
        query_embedding = self._embed_text(assignment_text)
        
        # Score each example by cosine similarity
        for ex in self.examples:
            sim = self._cosine_similarity(query_embedding, ex["embedding"])
            ex["similarity"] = sim
        
        # Sort by similarity descending
        sorted_examples = sorted(self.examples, key=lambda x: x["similarity"], reverse=True)
        
        return sorted_examples[:top_k]


# Example usage (if running this file standalone):
if __name__ == "__main__":
    # Make sure you have your OpenAI key in an .env or pass here
    rag = RAGEngine(examples_dir=Path("professor_examples"))
    
    student_assignment_text = "Explain the difference between supervised and unsupervised learning..."
    
    top_examples = rag.get_similar_grading_examples(student_assignment_text, top_k=3)
    for i, ex in enumerate(top_examples, start=1):
        print(f"--- Example #{i} (similarity={ex['similarity']:.4f}) ---")
        print(ex["text"][:200] + "...")
        print()
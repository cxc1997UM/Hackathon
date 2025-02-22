# llm_grader.py
import os
import json
import openai
from typing import Dict
from rag import RAGEngine  # Make sure rag.py is in the same project, or installed as a package

class LLMGrader:
    """
    LLMGrader uses an LLM (OpenAI GPT) to assign a numeric grade and provide feedback,
    using professor-specific style examples retrieved via RAGEngine.
    """

    def __init__(self,
                 openai_api_key: str = None,
                 rag_engine: RAGEngine = None,
                 model: str = "gpt-o4-mini"):
        """
        :param openai_api_key: API key for OpenAI.
        :param rag_engine: A RAGEngine instance for retrieving professor style examples.
        :param model: The OpenAI Chat model to use (e.g., gpt-3.5-turbo, gpt-4).
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.rag_engine = rag_engine
        self.model = model

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided or found in the environment.")
        openai.api_key = self.openai_api_key

        if not self.rag_engine:
            raise ValueError("RAGEngine instance not provided.")

    def grade_submission(self, assignment_text: str) -> Dict[str, str]:
        """
        Grades the given assignment text, returning a JSON-like dict:
        {
            "score": <numeric score 0-100 or letter>,
            "feedback": <short textual feedback>
        }
        """
        # 1. Retrieve top style examples from the RAG engine
        similar_examples = self.rag_engine.get_similar_grading_examples(assignment_text, top_k=2)

        # 2. Build prompt, injecting style examples
        examples_str = ""
        for ex in similar_examples:
            # Each ex is a dict like: {"text": "...", "similarity": 0.8, "filepath": "..."}
            # For the prompt, we only need ex["text"] or a curated excerpt.
            examples_str += f"\n--- Professor Style Example ---\n{ex['text']}\n"

        user_prompt = f"""
You are an AI that grades student assignments in the professor's style.
Below are examples of how the professor typically grades (rubrics, point distribution, feedback style):
{examples_str}

---
Now grade the following student submission. Provide:
1) A numeric score from 0-100
2) A brief feedback paragraph explaining the rationale behind the score.

Return the result ONLY as valid JSON, in the format:
{{
  "score": 95,
  "feedback": "Your explanation is clear, but you missed a key part on data structures."
}}

---
Student submission:
{assignment_text}
        """

        # 3. Call the OpenAI Chat Completion API
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assignment grader. Output valid JSON only."},
                {"role": "user", "content": user_prompt.strip()}
            ],
            temperature=0.2,
            max_tokens=800
        )
        
        assistant_message = response["choices"][0]["message"]["content"].strip()

        # 4. Attempt to parse as JSON
        try:
            result = json.loads(assistant_message)
            score = result.get("score", None)
            feedback = result.get("feedback", "")
            # In case of partial or missing fields, handle defaults:
            return {
                "score": score if score is not None else "N/A",
                "feedback": feedback
            }
        except json.JSONDecodeError:
            # Fallback if LLM output isn't valid JSON
            return {
                "score": "N/A",
                "feedback": "Unable to parse LLM response as JSON. Check the logs."
            }
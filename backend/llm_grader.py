# llm_grader.py
import os
import json
from typing import Dict
from openai import OpenAI
from rag import RAGEngine

class LLMGrader:
    """
    LLMGrader uses an LLM to grade homework assignments based on professor's rubrics 
    and grading style examples.
    """

    def __init__(self,
                 openai_api_key: str = None,
                 rag_engine: RAGEngine = None,
                 model: str = "gpt-4o-mini"):
        """
        Initialize the homework grading system.
        :param openai_api_key: API key for OpenAI
        :param rag_engine: RAGEngine instance for retrieving rubrics and grading examples
        :param model: The OpenAI model to use
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.rag_engine = rag_engine
        self.model = model

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided or found in the environment.")
        
        self.client = OpenAI(api_key=self.openai_api_key)

        if not self.rag_engine:
            raise ValueError("RAGEngine instance not provided.")

    def grade_submission(self, homework_text: str) -> Dict[str, str]:
        """
        Grade a homework submission using the professor's rubric and style.
        Returns score and detailed academic feedback.
        """
        # Get relevant rubrics and grading examples
        examples = self.rag_engine.get_similar_grading_examples(homework_text, top_k=2)

        # Build prompt with rubric and examples
        examples_str = ""
        for ex in examples:
            examples_str += f"\n--- Grading Example/Rubric ---\n{ex['text']}\n"

        grading_prompt = f"""
You are an AI teaching assistant helping a professor grade homework assignments.
Use these rubrics and past grading examples as reference:
{examples_str}

Grade this homework submission following these guidelines:
1. Assign points based on the rubric criteria
2. Provide specific feedback on:
   - What was done correctly
   - What needs improvement
   - Any conceptual misunderstandings
3. Include suggestions for improvement
4. Keep feedback constructive and educational

Return ONLY valid JSON in this format:
{{
  "score": <numeric score 0-100>,
  "feedback": "Detailed academic feedback here"
}}

Homework submission to grade:
{homework_text}
"""

        try:
            # Call OpenAI with academic grading focus
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an experienced teaching assistant helping grade homework assignments."},
                    {"role": "user", "content": grading_prompt.strip()}
                ],
                temperature=0.3,  # Lower temperature for more consistent grading
                max_tokens=1000   # Increased for detailed feedback
            )
            
            assistant_message = response.choices[0].message.content.strip()

            try:
                result = json.loads(assistant_message)
                return {
                    "score": result.get("score", "N/A"),
                    "feedback": result.get("feedback", "Unable to generate feedback.")
                }
            except json.JSONDecodeError:
                print(f"Error parsing LLM response: {assistant_message}")
                return {
                    "score": "N/A",
                    "feedback": "Error: Unable to parse grading response. Please check the format."
                }
                
        except Exception as e:
            print(f"Error during grading: {str(e)}")
            return {
                "score": "N/A",
                "feedback": f"Grading error: {str(e)}"
            }
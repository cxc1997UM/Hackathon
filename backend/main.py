import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from rag import RAGEngine
from file_parser import parse_file
from llm_grader import LLMGrader

# Create FastAPI app
app = FastAPI()

# Enable CORS specifically for the Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories for persistent storage and temporary uploads
PROFESSOR_EXAMPLES_DIR = Path("professor_examples")
TEMP_UPLOADS_DIR = Path("temp_uploads")

# Ensure the directories exist
PROFESSOR_EXAMPLES_DIR.mkdir(exist_ok=True)
TEMP_UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize the RAG engine and LLM grader
rag_engine = RAGEngine(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    examples_dir=PROFESSOR_EXAMPLES_DIR
)
llm_grader = LLMGrader(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    rag_engine=rag_engine,
    model="gpt-4o-mini"
)

@app.post("/upload-professor-example")
async def upload_professor_example(file: UploadFile = File(...)):
    """
    Upload a professor's grading example to be used in the RAG engine.
    """
    try:
        file_path = PROFESSOR_EXAMPLES_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Reload examples and update embeddings
        rag_engine._load_and_embed_examples()

        return {"message": f"Professor example '{file.filename}' uploaded successfully!"}
    except Exception as e:
        print(f"[ERROR] Error uploading professor example: {e}")
        return {"error": "Failed to upload professor example"}

@app.post("/grade")
async def grade_assignment(file: UploadFile = File(...)):
    """
    Grade a submitted resume file.
    """
    try:
        temp_path = TEMP_UPLOADS_DIR / file.filename
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"[DEBUG] File saved to {temp_path}")

        assignment_text = parse_file(temp_path)
        print(f"[DEBUG] Parsed assignment text (first 200 chars): {assignment_text[:200]}")

        result = llm_grader.grade_submission(assignment_text)
        print(f"[DEBUG] Grading result: {result}")

        return {
            "score": result["score"],
            "feedback": result["feedback"]
        }

    except Exception as e:
        print(f"[ERROR] Error during grading: {e}")
        return {"error": "Failed to grade resume"}

    finally:
        try:
            temp_path.unlink()
        except Exception as cleanup_err:
            print(f"[ERROR] Error cleaning up temp file: {cleanup_err}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
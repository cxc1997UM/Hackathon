# main.py
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

# Enable CORS so the Vue frontend (or any client) can call these endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories for persistent storage and temporary uploads.
# In a Dockerized environment, you can map these directories to volumes.
PROFESSOR_EXAMPLES_DIR = Path("professor_examples")
TEMP_UPLOADS_DIR = Path("temp_uploads")

# Ensure the directories exist
PROFESSOR_EXAMPLES_DIR.mkdir(exist_ok=True)
TEMP_UPLOADS_DIR.mkdir(exist_ok=True)

# Initialize the RAG engine and LLM grader using environment variables for the OpenAI API key.
rag_engine = RAGEngine(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    examples_dir=PROFESSOR_EXAMPLES_DIR
)
llm_grader = LLMGrader(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    rag_engine=rag_engine,
    model="gpt-4o-mini"  # You can change this to "gpt-4" if desired.
)

@app.post("/upload-professor-example")
async def upload_professor_example(file: UploadFile = File(...)):
    """
    Upload a professor's grading example to be used in the RAG engine.
    The file is stored persistently in the 'professor_examples' directory.
    After saving, the RAG engine reloads its embeddings.
    """
    file_path = PROFESSOR_EXAMPLES_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Reload examples and update embeddings immediately.
    rag_engine._load_and_embed_examples()

    return {"message": f"Professor example '{file.filename}' uploaded successfully!"}

@app.post("/grade")
async def grade_assignment(file: UploadFile = File(...)):
    """
    Grade a student's assignment by:
      1. Saving the uploaded file to a temporary directory.
      2. Parsing its content into text.
      3. Passing the text to the LLM grader (which uses RAG for style examples).
      4. Returning the grading score and feedback as JSON.
    """
    # Save the uploaded file to a temporary location
    temp_path = TEMP_UPLOADS_DIR / file.filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse the file into raw text (supports PDF, DOCX, HTML, TXT)
    assignment_text = parse_file(temp_path)

    # Grade the assignment using the LLM grader
    result = llm_grader.grade_submission(assignment_text)

    # Clean up the temporary file
    try:
        temp_path.unlink()
    except Exception as e:
        print(f"Error cleaning up temp file: {e}")

    # Return the grading results to the frontend
    return {
        "score": result["score"],
        "feedback": result["feedback"]
    }

# (Optional) Serve static frontend assets if needed.
# Uncomment and adjust the directory path if you build your Vue app.
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")

if __name__ == '__main__':
    import uvicorn
    # Run the FastAPI app on host 0.0.0.0 and port 8000 so it is accessible in Docker.
    uvicorn.run(app, host="0.0.0.0", port=8000)

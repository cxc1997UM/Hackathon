# main.py
import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from rag import RAGEngine
from file_parser import parse_file
from llm_grader import LLMGrader

# 1. Create a FastAPI app
app = FastAPI()

# 2. (Optional) Enable CORS so your Vue frontend can call these endpoints
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize your RAG engine and LLM grader
#    We assume you keep your professor examples in "professor_examples" dir
#    and your OpenAI API key is in an environment variable or .env file
rag_engine = RAGEngine(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    examples_dir=Path("professor_examples")  # Directory with professor's style examples
)
llm_grader = LLMGrader(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    rag_engine=rag_engine,
    model="gpt-3.5-turbo"  # or "gpt-4", etc.
)

@app.post("/upload-professor-example")
async def upload_professor_example(file: UploadFile = File(...)):
    """
    Endpoint to upload new 'professor style' examples for RAG.
    Saves the file in 'professor_examples/' and re-embeds them in the rag_engine.
    This allows the system to dynamically learn new grading styles.
    """
    file_path = Path("professor_examples") / file.filename
    file_path.parent.mkdir(exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Re-load and embed the new examples so they're available immediately
    rag_engine._load_and_embed_examples()

    return {"message": f"Professor example '{file.filename}' uploaded successfully!"}

@app.post("/grade")
async def grade_assignment(file: UploadFile = File(...)):
    """
    Endpoint to grade a student assignment.
    1. Saves the uploaded file temporarily.
    2. Parses it into raw text.
    3. Feeds it into LLMGrader which uses the professor style examples (RAG).
    4. Returns a score & feedback JSON back to the frontend.
    """
    # 1. Save the file to a temporary location
    temp_path = Path("temp_uploads") / file.filename
    temp_path.parent.mkdir(exist_ok=True)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Parse the student's assignment text (PDF, DOCX, HTML, TXT)
    assignment_text = parse_file(temp_path)

    # 3. Grade it using the LLM grader (RAG + LLM)
    result = llm_grader.grade_submission(assignment_text)

    # 4. Return the result JSON to the frontend
    return {
        "score": result["score"],
        "feedback": result["feedback"]
    }
# iGrade.ai

An open-source, AI-powered grading assistant that learns from teachers' grading styles to provide accurate, consistent, and affordable assessment at scale.

## Features

- 📚 Learn from existing grading styles using RAG (Retrieval-Augmented Generation)
- 📝 Support for multiple file formats (PDF, DOCX, HTML, TXT)
- 🚀 Fast and efficient grading process
- 💰 Cost-effective alternative to expensive grading platforms
- 🌐 Works offline with local models (coming soon)

## Architecture

The system consists of two main components:

1. Frontend (Vue.js)
   - Intuitive file upload interface
   - Real-time grading feedback
   - Modal-based results display
   - Responsive design

2. Backend (FastAPI)
   - File processing system
   - RAG-based grading engine
   - LLM integration
   - Temporary file management

## Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Virtual environment (recommended)

## Installation

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/cxc1997UM/Hackathon.git
cd Hackathon/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env and set your backend API URL
```

## Configuration

### Backend (.env)

```plaintext
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini  # or your preferred model
MAX_TOKENS=1000
TEMPERATURE=0.3
```

### Frontend (.env)

```plaintext
VITE_API_URL=http://localhost:8000
```

## Running the Application

### Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage Guide

1. **Upload Grading Examples**
   - Choose "Rubric" or "Graded Example" type
   - Upload PDF, DOCX, or TXT files
   - For graded examples, use filename format: `assignment_score.pdf` (e.g., `homework1_90.pdf`)

2. **Upload Student Homework**
   - Drag and drop or select files
   - Supported formats: PDF, DOCX, TXT
   - System will process and grade automatically

3. **Review Results**
   - View score and detailed feedback
   - Adjust grades if needed
   - Export results (coming soon)

## API Endpoints

### Backend API

```plaintext
POST /upload-professor-example
- Upload rubrics or graded examples
- Multipart form data Hackathon
POST /grade
- Upload student homework for grading
- Multipart form data with file
- Returns score and feedback
```

## Directory Structure

```
├── backend/
│   ├── file_parser.py    # File format handling
│   ├── llm_grader.py     # Grading logic
│   ├── main.py          # FastAPI entry point
│   ├── rag.py           # RAG implementation
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.vue      # Main component
│   │   ├── components/  # Vue components
│   │   └── api/        # Backend communication
│   ├── package.json    # Node.js dependencies
│   └── vite.config.js  # Vite configuration
└── README.md
```

## Contributing

We welcome contributions! Please check our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Cost Estimation

- OpenAI API: ~$0.10-0.15 per assignment
- Hosting: From $5/month (basic tier)
- Storage: From $1/month per GB

## Roadmap

- [ ] Offline mode support
- [ ] Mobile application
- [ ] Multiple language support
- [ ] LMS integration
- [ ] Advanced analytics
- [ ] Peer review system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [FAQ](docs/FAQ.md)
2. Search existing [Issues](https://github.com/cxc1997UM/Hackathon/issues)
3. Create a new issue if needed

## Acknowledgments

- OpenAI for API access
- Vue.js team
- FastAPI developers
- All our contributors

---

Built with ❤️ for educators everywhere

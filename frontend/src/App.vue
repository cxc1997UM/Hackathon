<template>
  <div>
    <Header />
    <div class="homepage">
      <div class="hero-section">
        <h1 class="title">Welcome to iGrade.ai</h1>
        <p class="subtitle">
          Upload your grading rubric or past graded examples to help the AI learn your grading style.
          Then upload student homework assignments for rapid grading.
        </p>
      </div>

      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        Loading...
      </div>
      <div v-if="error" class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        {{ error }}
      </div>

      <div class="upload-container">
        <!-- RAG Memory Upload: left-indented box -->
        <div class="rag-upload">
          <h2 class="upload-title">Upload Rubric or Grading Examples</h2>
          <p class="upload-subtitle">Select document type and upload</p>
          
          <!-- Document Type Selection -->
          <div class="document-type-selector">
            <label class="type-option">
              <input 
                type="radio" 
                v-model="documentType" 
                value="rubric" 
                name="docType"
              >
              <span class="type-label">Rubric</span>
            </label>
            <label class="type-option">
              <input 
                type="radio" 
                v-model="documentType" 
                value="example" 
                name="docType"
              >
              <span class="type-label">Graded Example</span>
            </label>
          </div>

          <!-- File Upload Zone -->
          <div class="file-upload-zone">
            <input 
              type="file" 
              @change="handleRagFile" 
              accept=".pdf,.docx,.txt"
              id="rag-file-input"
              class="file-input" 
              :disabled="!documentType"
            />
            <label for="rag-file-input" class="file-input-label">
              <svg xmlns="http://www.w3.org/2000/svg" class="upload-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Choose file or drag here</span>
            </label>
            <span v-if="ragFile" class="selected-file">
              <span class="file-name">Selected: {{ ragFile.name }}</span>
              <button class="clear-file" @click.prevent="clearRagFile" title="Remove selected file">×</button>
            </span>
          </div>
          <button @click="uploadRagFile" :disabled="loading" class="upload-button">
            {{ loading ? 'Uploading...' : 'Upload Example' }}
          </button>
        </div>

        <!-- Homework Upload: larger and centered -->
        <div class="homework-upload">
          <h2 class="upload-title">Upload Student Homework</h2>
          <div class="file-upload-zone">
            <input 
              type="file" 
              @change="handleHomeworkFile" 
              accept=".pdf,.docx,.txt"
              id="homework-file-input"
              class="file-input" 
            />
            <label for="homework-file-input" class="file-input-label">
              <svg xmlns="http://www.w3.org/2000/svg" class="upload-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Choose file or drag here</span>
            </label>
            <span v-if="homeworkFile" class="selected-file">
              <span class="file-name">Selected: {{ homeworkFile.name }}</span>
              <button class="clear-file" @click.prevent="clearHomeworkFile" title="Remove selected file">×</button>
            </span>
          </div>
          <button @click="uploadHomeworkFile" :disabled="loading" class="upload-button">
            {{ loading ? 'Grading...' : 'Grade Homework' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Feedback Modal -->
    <FeedbackModal
      :show="showModal"
      :title="modalTitle"
      :score="modalScore"
      :feedback="modalFeedback"
      @close="showModal = false"
    />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import FeedbackModal from './components/FeedbackModal.vue';
import { uploadProfessorExample, gradeHomework } from './api';

export default {
  name: "App",
  components: {
    Header,
    FeedbackModal,
  },
  data() {
    return {
      ragFile: null,
      homeworkFile: null,
      documentType: '', // 'rubric' or 'example'
      loading: false,
      error: null,
      showModal: false,
      modalTitle: '',
      modalScore: null,
      modalFeedback: '',
      uploadedDocuments: [], // Track uploaded RAG documents
    };
  },
  methods: {
    handleRagFile(e) {
      if (!this.documentType) {
        this.error = "Please select a document type (Rubric or Graded Example)";
        return;
      }

      const file = e.target.files[0];
      if (!file) return;

      // For graded examples, check filename score format
      if (this.documentType === 'example') {
        const match = file.name.match(/(.+)_(\d+)\.(pdf|docx|txt)$/);
        if (!match) {
          this.error = "Graded examples must be named: assignment_score.pdf (e.g., homework1_90.pdf)";
          return;
        }

        const [, name, score] = match;
        this.ragFile = {
          file,
          name: name,
          score: parseInt(score),
          type: 'example'
        };
      } else {
        // For rubrics, just store the file
        this.ragFile = {
          file,
          name: file.name.replace(/\.[^/.]+$/, ""), // Remove extension
          type: 'rubric'
        };
      }
      this.error = null;
    },

    clearRagFile() {
      this.ragFile = null;
      const input = document.getElementById('rag-file-input');
      if (input) input.value = '';
    },

    clearHomeworkFile() {
      this.homeworkFile = null;
      const input = document.getElementById('homework-file-input');
      if (input) input.value = '';
    },

    removeDocument(documentId) {
      this.uploadedDocuments = this.uploadedDocuments.filter(doc => doc.id !== documentId);
      // Here you would also want to call an API to remove the document from the backend
      // await removeDocument(documentId);
    },

    handleHomeworkFile(e) {
      this.homeworkFile = e.target.files[0];
      this.error = null;
    },
    async uploadRagFile() {
      if (!this.ragFile) {
        this.error = "Please select a file to upload.";
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        const data = await uploadProfessorExample(this.ragFile.file);
        this.uploadedDocuments.push({
          id: Date.now(),
          name: this.ragFile.name,
          score: this.ragFile.score,
          type: this.ragFile.type,
          filename: this.ragFile.file.name
        });
        
        let successMessage = this.ragFile.type === 'rubric' 
          ? `Rubric "${this.ragFile.name}" has been added.`
          : `Graded example "${this.ragFile.name}" (Score: ${this.ragFile.score}) has been added.`;

        this.modalTitle = 'Upload Successful';
        this.modalFeedback = successMessage;
        this.showModal = true;
        this.ragFile = null;
        this.documentType = ''; // Reset document type
        
        // Reset the file input
        const input = document.getElementById('rag-file-input');
        if (input) input.value = '';
      } catch (error) {
        console.error("Error uploading document:", error);
        this.error = "Failed to upload document.";
      } finally {
        this.loading = false;
      }
    },
    async uploadHomeworkFile() {
      if (!this.homeworkFile) {
        this.error = "Please select a homework file to grade.";
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        const data = await gradeHomework(this.homeworkFile);
        this.modalTitle = 'Grading Complete';
        this.modalScore = data.score;
        this.modalFeedback = data.feedback;
        this.showModal = true;
      } catch (error) {
        console.error("Error grading homework:", error);
        this.error = "Failed to grade homework.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
/* Global styles */
:root {
  --primary-color: #AEDFF7;  /* Pastel blue */
  --secondary-color: rgb(255, 255, 255); /* White */
  --accent-color: #FF4444;    /* Red accent */
  --text-color: #333333;
  --font-family: 'Helvetica Neue', Arial, sans-serif;
}

/* Body styling */
body {
  background-color: var(--secondary-color);
  color: var(--text-color);
  margin: 0;
  font-family: var(--font-family);
}

/* Homepage styling */
.homepage {
  text-align: center;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  margin-bottom: 3rem;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--text-color);
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Upload container layout */
.upload-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
  margin-top: 2rem;
}

/* RAG Upload Box styling */
.rag-upload {
  width: 30%;
  background-color: var(--primary-color);
  padding: 1.5rem;
  border-radius: 12px;
  color: var(--text-color);
  text-align: left;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.rag-upload:hover {
  transform: translateY(-2px);
}

/* Homework Upload Box styling */
.homework-upload {
  width: 50%;
  background-color: var(--primary-color);
  padding: 1.5rem;
  border-radius: 12px;
  color: var(--text-color);
  text-align: left;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.homework-upload:hover {
  transform: translateY(-2px);
}

/* Upload zone styling */
.file-upload-zone {
  margin: 1.5rem 0;
  position: relative;
}

.file-input {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

.file-input-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.5);
  border: 2px dashed #666;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-input-label:hover {
  background-color: rgba(255, 255, 255, 0.8);
  border-color: var(--accent-color);
}

.upload-icon {
  width: 2.5rem;
  height: 2.5rem;
  margin-bottom: 0.5rem;
  color: #666;
}

.selected-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  font-size: 0.9rem;
  color: #666;
}

.file-name {
  margin-right: 0.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-file {
  background: none;
  border: none;
  color: var(--accent-color);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  line-height: 1;
  transition: background-color 0.2s ease;
}

.clear-file:hover {
  background-color: rgba(255, 68, 68, 0.1);
}

/* Button styling */
.upload-button {
  background-color: var(--accent-color);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  color: var(--secondary-color);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  font-weight: 500;
}

.upload-button:hover {
  background-color: #e03d3d;
  transform: translateY(-1px);
}

.upload-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
}

/* Document type selector styling */
.document-type-selector {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 6px;
}

.type-option {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.type-option:hover {
  background-color: rgba(255, 255, 255, 0.8);
}

.type-option input[type="radio"] {
  margin: 0;
}

.type-label {
  font-size: 0.9rem;
  color: var(--text-color);
}

/* Update document list to show type */
.document-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.document-type {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #666;
  background-color: rgba(174, 223, 247, 0.3);
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  display: inline-block;
}
.uploaded-documents {
  margin: 1rem 0;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
}

.document-list {
  max-height: 200px;
  overflow-y: auto;
}

.document-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  margin: 0.5rem 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.document-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.document-name {
  font-weight: 500;
}

.document-score {
  font-size: 0.875rem;
  color: #666;
}

.remove-button {
  background: none;
  border: none;
  color: var(--accent-color);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.remove-button:hover {
  background-color: rgba(255, 68, 68, 0.1);
}
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1rem;
  color: var(--accent-color);
}

.loading-spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid #f3f3f3;
  border-top: 2px solid var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 1rem;
  padding: 0.75rem;
  background-color: #fff3f3;
  border: 1px solid var(--accent-color);
  border-radius: 6px;
  color: var(--accent-color);
}

.error-icon {
  width: 1.25rem;
  height: 1.25rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive design */
@media (max-width: 768px) {
  .upload-container {
    flex-direction: column;
    align-items: center;
  }
  
  .rag-upload,
  .homework-upload {
    width: 100%;
    max-width: 500px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
}
</style>
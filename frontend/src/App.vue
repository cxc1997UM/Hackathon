<template>
  <div>
    <!-- Include the Header at the top -->
    <Header />

    <div class="homepage">
      <h1>Welcome to iGrade.ai</h1>
      <p>
        Optionally upload your grading examples (to help the LLM learn your style) 
        and upload a resume for grading.
      </p>

      <div class="upload-container">
        <!-- RAG Memory Upload: left-indented box -->
        <div class="rag-upload">
          <h2>Upload Grading Examples</h2>
          <p>(Optional: Teach the AI your grading style)</p>
          <input type="file" @change="handleRagFile" accept=".pdf,.docx,.txt" />
          <button @click="uploadRagFile">Upload to RAG</button>
        </div>

        <!-- Resume Upload: larger and centered -->
        <div class="resume-upload">
          <h2>Upload Student Resume</h2>
          <input type="file" @change="handleResumeFile" accept=".pdf,.docx,.txt" />
          <button @click="uploadResumeFile">Upload Resume</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue';

export default {
  name: "App",
  components: {
    Header,
  },
  data() {
    return {
      ragFile: null,
      resumeFile: null,
    };
  },
  methods: {
    handleRagFile(e) {
      this.ragFile = e.target.files[0];
    },
    handleResumeFile(e) {
      this.resumeFile = e.target.files[0];
    },
    uploadRagFile() {
      if (!this.ragFile) {
        alert("Please select a file for grading examples.");
        return;
      }
      alert(`RAG file "${this.ragFile.name}" uploaded!`);
      // Replace with actual API call to your FastAPI backend
    },
    uploadResumeFile() {
      if (!this.resumeFile) {
        alert("Please select a resume file to upload.");
        return;
      }
      alert(`Resume file "${this.resumeFile.name}" uploaded!`);
      // Replace with actual API call to your FastAPI backend
    },
  },
};
</script>

<style>
/* Remove "scoped" so these styles can apply globally */
:root {
  --primary-color: #AEDFF7;  /* Pastel blue */
  --secondary-color:rgb(255, 255, 255); /* White */
  --accent-color: #FF4444;    /* Red accent */
  --text-color: #333333;
  --font-family: 'Helvetica Neue', Arial, sans-serif;
}

/* Apply white background and standard text color to the body */
body {
  background-color: var(--secondary-color);
  color: var(--text-color);
  margin: 0;
  font-family: var(--font-family);
}

.homepage {
  text-align: center;
  padding: 2rem;
}

.upload-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 2rem;
  margin-top: 2rem;
}

/* RAG Upload Box: left-indented and smaller */
.rag-upload {
  width: 30%;
  background-color: var(--primary-color); /* Pastel blue box */
  padding: 1.5rem;
  border-radius: 8px;
  color: var(--secondary-color);          /* White text inside the box */
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Resume Upload Box: larger and centered */
.resume-upload {
  width: 50%;
  background-color: var(--primary-color); /* Pastel blue box */
  padding: 1.5rem;
  border-radius: 8px;
  color: var(--secondary-color);          /* White text inside the box */
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input[type="file"] {
  display: block;
  margin-bottom: 1rem;
}

button {
  background-color: var(--accent-color); /* Red accent */
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  color: var(--secondary-color);         /* White text on button */
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e03d3d; /* Slightly darker red on hover */
}
</style>

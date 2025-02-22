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
    async uploadRagFile() {
      if (!this.ragFile) {
        alert("Please select a file for grading examples.");
        return;
      }
      const formData = new FormData();
      formData.append("file", this.ragFile);

      try {
        const response = await fetch("/upload-professor-example", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        alert(data.message); // Expecting a message like: "Professor example 'filename' uploaded successfully!"
      } catch (error) {
        console.error("Error uploading professor example:", error);
        alert("Failed to upload professor example.");
      }
    },
    async uploadResumeFile() {
      if (!this.resumeFile) {
        alert("Please select a resume file to upload.");
        return;
      }
      const formData = new FormData();
      formData.append("file", this.resumeFile);

      try {
        const response = await fetch("/grade", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        alert(`Grading complete!\nScore: ${data.score}\nFeedback: ${data.feedback}`);
      } catch (error) {
        console.error("Error grading resume:", error);
        alert("Failed to grade resume.");
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
  border-radius: 8px;
  color: var(--secondary-color);
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Resume Upload Box styling */
.resume-upload {
  width: 50%;
  background-color: var(--primary-color);
  padding: 1.5rem;
  border-radius: 8px;
  color: var(--secondary-color);
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Input and button styling */
input[type="file"] {
  display: block;
  margin-bottom: 1rem;
}

button {
  background-color: var(--accent-color);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  color: var(--secondary-color);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e03d3d;
}
</style>
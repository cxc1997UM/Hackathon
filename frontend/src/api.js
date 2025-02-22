// src/api.js

const API_BASE_URL = 'http://localhost:8000';  // FastAPI server URL

export const uploadProfessorExample = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload-professor-example`, {
    method: "POST",
    body: formData,
  });
  return response.json();
};

export const gradeHomework = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/grade`, {
    method: "POST",
    body: formData,
  });
  return response.json();
};
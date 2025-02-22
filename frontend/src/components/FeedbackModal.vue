<template>
  <transition name="modal-fade">
    <div v-if="show" class="modal-backdrop">
      <div class="modal-content">
        <header class="modal-header">
          <h3 class="modal-title">{{ title }}</h3>
          <button class="close-button" @click="$emit('close')">×</button>
        </header>
        <section class="modal-body">
          <div v-if="score !== null" class="score-section">
            Score: <span class="score">{{ score }}</span>
          </div>
          <div class="feedback-section">
            {{ feedback }}
          </div>
        </section>
        <footer class="modal-footer">
          <button class="modal-button" @click="$emit('close')">Close</button>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'FeedbackModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Feedback'
    },
    score: {
      type: [Number, String],
      default: null
    },
    feedback: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
}

.modal-title {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
  font-weight: 600;
}

.close-button {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  color: #888;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #555;
}

.modal-body {
  padding: 1.5rem;
  color: #444;
  overflow-y: auto;
  flex-grow: 1;
}

.score-section {
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.score {
  font-weight: bold;
  color: #ff7f7f; /* lighter shade of red */
}

.feedback-section {
  line-height: 1.6;
  white-space: pre-wrap;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
  display: flex;
  justify-content: flex-end;
}

.modal-button {
  background-color: #ff6b6b;
  color: #fff;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.modal-button:hover {
  background-color: #ff4c4c;
}

/* Transition animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>

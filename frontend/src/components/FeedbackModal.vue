# FeedbackModal.vue
<template>
  <transition name="modal-fade">
    <div v-if="show" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-button" @click="$emit('close')">×</button>
        </div>
        <div class="modal-body">
          <div v-if="score" class="score-section">
            Score: <span class="score">{{ score }}</span>
          </div>
          <div class="feedback-section">
            {{ feedback }}
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-button" @click="$emit('close')">Close</button>
        </div>
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--secondary-color);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: var(--text-color);
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
}

.close-button:hover {
  color: var(--accent-color);
}

.modal-body {
  padding: 1.5rem;
  color: var(--text-color);
  overflow-y: auto;
  flex-grow: 1;
  min-height: 0;
}

.score-section {
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.score {
  font-weight: bold;
  color: var(--accent-color);
}

.feedback-section {
  line-height: 1.6;
  white-space: pre-wrap;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.modal-button {
  background-color: var(--accent-color);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.modal-button:hover {
  background-color: #e03d3d;
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
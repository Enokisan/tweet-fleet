<!-- src/components/NoteInput.vue -->
<template>
  <div class="note-input-container">
    <div class="input-header">
      <h3>新しいフリーティングノート</h3>
      <span class="character-count" :class="{ 'limit-reached': isLimitReached }">
        {{ characterCount }}/140
      </span>
    </div>
    
    <textarea
      :value="modelValue"
      class="note-textarea"
      placeholder="気づきや考えを140文字以内で記録しましょう..."
      @input="onInput"
      :maxlength="140"
    ></textarea>
    
    <div class="action-buttons">
      <div class="share-options">
        <label class="share-option">
          <input type="checkbox" :checked="shareToX" @change="$emit('update:shareToX', $event.target.checked)">
          <span>Xに投稿</span>
        </label>
        <label class="share-option">
          <input type="checkbox" :checked="saveToGithub" @change="$emit('update:saveToGithub', $event.target.checked)">
          <span>GitHubに保存</span>
        </label>
      </div>
      
      <button 
        class="save-button" 
        @click="$emit('save')" 
        :disabled="!modelValue || modelValue.length > 140"
      >
        投稿
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NoteInput',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    characterCount: {
      type: Number,
      default: 0
    },
    shareToX: {
      type: Boolean,
      default: true
    },
    saveToGithub: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue', 'update:characterCount', 'update:shareToX', 'update:saveToGithub', 'save'],
  computed: {
    isLimitReached() {
      return this.characterCount > 130;
    }
  },
  methods: {
    onInput(event) {
      this.$emit('update:modelValue', event.target.value);
      this.$emit('update:characterCount');
    }
  }
}
</script>

<style scoped>
.note-input-container {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.input-header h3 {
  font-size: 18px;
  margin: 0;
  color: #333;
}

.character-count {
  font-size: 14px;
  color: #666;
}

.limit-reached {
  color: #e53935;
  font-weight: bold;
}

.note-textarea {
  width: 100%;
  min-height: 120px;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  resize: vertical;
  margin-bottom: 12px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.note-textarea:focus {
  outline: none;
  border-color: #1da1f2;
  box-shadow: 0 0 0 2px rgba(29, 161, 242, 0.2);
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.share-options {
  display: flex;
  gap: 16px;
}

.share-option {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #555;
}

.save-button {
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button:hover {
  background-color: #0c8bd9;
}

.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .action-buttons {
    flex-direction: column;
    gap: 16px;
  }
  
  .share-options {
    justify-content: space-between;
    width: 100%;
  }
  
  .save-button {
    width: 100%;
  }
}
</style>
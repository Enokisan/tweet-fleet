<!-- src/components/NoteInput.vue -->
<template>
  <div class="note-input">
    <textarea
      v-model="localContent"
      :maxlength="140"
      placeholder="ノートを入力..."
      @input="updateContent"
    ></textarea>
    
    <div class="input-footer">
      <div class="character-count" :class="{ 'near-limit': characterCount > 120 }">
        {{ characterCount }}/140
      </div>
      
      <div class="share-options">
        <label class="share-option" :class="{ disabled: !isAuthenticated }">
          <input
            type="checkbox"
            :checked="shareToX"
            :disabled="!isAuthenticated"
            @change="$emit('update:shareToX', $event.target.checked)"
          >
          <span>Xに投稿</span>
        </label>
        
        <label class="share-option" :class="{ disabled: !isAuthenticated }">
          <input
            type="checkbox"
            :checked="saveToGithub"
            :disabled="!isAuthenticated"
            @change="$emit('update:saveToGithub', $event.target.checked)"
          >
          <span>GitHubに保存</span>
        </label>
      </div>
      
      <button 
        class="save-button" 
        :disabled="!localContent || characterCount > 140"
        @click="$emit('save')"
      >
        保存
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
      required: true
    },
    characterCount: {
      type: Number,
      required: true
    },
    shareToX: {
      type: Boolean,
      required: true
    },
    saveToGithub: {
      type: Boolean,
      required: true
    },
    isAuthenticated: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      localContent: this.modelValue
    }
  },
  watch: {
    modelValue(newValue) {
      this.localContent = newValue;
    }
  },
  methods: {
    updateContent() {
      this.$emit('update:modelValue', this.localContent);
      this.$emit('update:characterCount', this.localContent.length);
    }
  }
}
</script>

<style scoped>
.note-input {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #e1e8ed;
  border-radius: 4px;
  resize: vertical;
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 12px;
}

textarea:focus {
  outline: none;
  border-color: #1da1f2;
  box-shadow: 0 0 0 2px rgba(29, 161, 242, 0.2);
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.character-count {
  font-size: 0.875rem;
  color: #666;
}

.character-count.near-limit {
  color: #e53935;
}

.share-options {
  display: flex;
  gap: 16px;
}

.share-option {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  color: #333;
  cursor: pointer;
}

.share-option.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.share-option input[type="checkbox"] {
  margin: 0;
}

.save-button {
  padding: 8px 16px;
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button:hover:not(:disabled) {
  background-color: #1a91da;
}

.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .input-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .share-options {
    justify-content: space-between;
  }
}
</style>
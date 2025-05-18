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
            :checked="isAuthenticated && shareToX"
            :disabled="!isAuthenticated"
            @change="handleCheckboxChange('shareToX', $event)"
          >
          <span>Xに投稿</span>
          <span v-if="!isAuthenticated" class="auth-required">(認証が必要)</span>
        </label>
        
        <label class="share-option" :class="{ disabled: !isAuthenticated }">
          <input
            type="checkbox"
            :checked="isAuthenticated && saveToGithub"
            :disabled="!isAuthenticated"
            @change="handleCheckboxChange('saveToGithub', $event)"
          >
          <span>GitHubに保存</span>
          <span v-if="!isAuthenticated" class="auth-required">(認証が必要)</span>
        </label>
      </div>
      
      <button 
        class="save-button" 
        :disabled="!localContent || characterCount > 140 || !isAuthenticated"
        @click="$emit('save')"
      >
        {{ isAuthenticated ? '保存' : '認証が必要' }}
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
    },
    handleCheckboxChange(type, event) {
      if (!this.isAuthenticated) {
        event.preventDefault();
        return;
      }
      this.$emit(`update:${type}`, event.target.checked);
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
  width: 100%;
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
  background-color: #fff;
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
  flex-wrap: wrap;
}

.character-count {
  font-size: 0.875rem;
  color: #666;
  white-space: nowrap;
}

.character-count.near-limit {
  color: #e53935;
}

.share-options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  flex: 1;
  justify-content: flex-end;
}

.share-option {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  color: #333;
  cursor: pointer;
  white-space: nowrap;
}

.share-option.disabled {
  opacity: 0.7;
  cursor: not-allowed;
  pointer-events: none;
  user-select: none;
}

.share-option input[type="checkbox"] {
  margin: 0;
  cursor: pointer;
}

.share-option.disabled input[type="checkbox"] {
  cursor: not-allowed;
  pointer-events: none;
}

.auth-required {
  font-size: 0.75rem;
  color: #666;
  font-style: italic;
}

.save-button {
  padding: 8px 16px;
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
  white-space: nowrap;
}

.save-button:hover:not(:disabled) {
  background-color: #1a91da;
}

.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .note-input {
    padding: 12px;
  }
  
  textarea {
    min-height: 80px;
    font-size: 0.9375rem;
    padding: 10px;
  }
  
  .input-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .share-options {
    justify-content: space-between;
    width: 100%;
    gap: 12px;
  }
  
  .share-option {
    font-size: 0.8125rem;
  }
  
  .save-button {
    width: 100%;
    padding: 10px;
    font-size: 0.9375rem;
  }
  
  .character-count {
    font-size: 0.8125rem;
  }
  
  .auth-required {
    font-size: 0.6875rem;
  }
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
  .note-input {
    background-color: #192734;
  }
  
  textarea {
    background-color: #253341;
    border-color: #38444d;
    color: #fff;
  }
  
  .share-option {
    color: #fff;
  }
  
  .character-count {
    color: #8899a6;
  }
  
  .auth-required {
    color: #8899a6;
  }
}
</style>
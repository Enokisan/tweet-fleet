<template>
  <div class="settings-modal" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>設定</h2>
      
      <div class="settings-section">
        <h3>Xアカウント連携</h3>
        <div v-if="xConnected" class="connection-status connected">
          <i class="fas fa-check-circle"></i>
          <span>管理者として連携済み</span>
          <button class="disconnect-button" @click="$emit('disconnect-x')">連携解除</button>
        </div>
        <div v-else class="connection-status">
          <button class="connect-button" @click="$emit('connect-x')">管理者として連携する</button>
        </div>
      </div>
      
      <div class="settings-section">
        <h3>GitHub連携</h3>
        <div class="form-group">
          <label for="github-repo">GitHubリポジトリ</label>
          <input 
            type="text" 
            id="github-repo" 
            :value="githubRepo" 
            @input="$emit('update:githubRepo', $event.target.value)" 
            placeholder="username/repository"
          >
        </div>
        <div class="form-group">
          <label for="github-path">ファイルパス</label>
          <input 
            type="text" 
            id="github-path" 
            :value="githubPath" 
            @input="$emit('update:githubPath', $event.target.value)" 
            placeholder="notes/fleeting-notes.md"
          >
        </div>
        <div v-if="githubConnected" class="connection-status connected">
          <i class="fas fa-check-circle"></i>
          <span>GitHubと連携済み</span>
          <button class="disconnect-button" @click="$emit('disconnect-github')">連携解除</button>
        </div>
        <div v-else class="connection-status">
          <button class="connect-button" @click="$emit('connect-github')">GitHubと連携する</button>
        </div>
      </div>
      
      <div class="modal-buttons">
        <button class="close-button" @click="$emit('close')">閉じる</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsModal',
  props: {
    xConnected: {
      type: Boolean,
      default: false
    },
    xUsername: {
      type: String,
      default: ''
    },
    githubConnected: {
      type: Boolean,
      default: false
    },
    githubRepo: {
      type: String,
      default: ''
    },
    githubPath: {
      type: String,
      default: ''
    }
  },
  emits: [
    'close', 
    'connect-x', 
    'disconnect-x', 
    'connect-github', 
    'disconnect-github',
    'update:githubRepo',
    'update:githubPath'
  ]
}
</script>

<style scoped>
.settings-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-content h2 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 22px;
  color: #333;
}

.settings-section {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e1e8ed;
}

.settings-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.settings-section h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: #333;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e1e8ed;
  border-radius: 4px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #1da1f2;
  box-shadow: 0 0 0 2px rgba(29, 161, 242, 0.2);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.connection-status.connected {
  color: #34a853;
}

.connect-button {
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.connect-button:hover {
  background-color: #0c8bd9;
}

.disconnect-button {
  background-color: transparent;
  border: 1px solid #e1e8ed;
  color: #666;
  border-radius: 50px;
  padding: 4px 12px;
  font-size: 12px;
  cursor: pointer;
  margin-left: auto;
  transition: all 0.2s;
}

.disconnect-button:hover {
  background-color: #f5f5f5;
  color: #e53935;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.close-button {
  background-color: #f5f5f5;
  border: none;
  color: #333;
  border-radius: 50px;
  padding: 8px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: #e1e8ed;
}
</style>
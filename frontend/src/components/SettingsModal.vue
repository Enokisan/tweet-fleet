<template>
  <div class="settings-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>API認証</h2>
        <button class="close-button" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="auth-section">
          <div v-if="!localIsAuthenticated">
            <p class="auth-description">APIを使用するには認証が必要です</p>
            <div class="form-group">
              <input 
                type="password" 
                v-model="password" 
                placeholder="パスワードを入力"
                @keyup.enter="authenticate"
              >
              <button class="auth-button" @click="authenticate">認証</button>
            </div>
            <p v-if="authError" class="error-message">{{ authError }}</p>
          </div>
          
          <div v-else class="auth-success">
            <p>認証済み（1時間有効）</p>
            <button class="logout-button" @click="logout">ログアウト</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import xService from '../services/xService';
import githubService from '../services/githubService';

export default {
  name: 'SettingsModal',
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      password: '',
      authError: '',
      localIsAuthenticated: false
    }
  },
  created() {
    // 初期化時に認証状態を確認
    this.updateAuthState();
  },
  watch: {
    isAuthenticated: {
      immediate: true,
      handler(newValue) {
        this.updateAuthState();
      }
    }
  },
  methods: {
    updateAuthState() {
      // XサービスとGitHubサービスの認証状態を確認
      const xAuth = xService.isAuthenticated && xService.isTokenValid();
      const githubAuth = githubService.isAuthenticated && githubService.isTokenValid();
      
      // 両方のサービスが認証済みの場合のみtrue
      this.localIsAuthenticated = xAuth && githubAuth;
      
      // 認証済みの場合、GitHubサービスにトークンを設定
      if (this.localIsAuthenticated && xService.accessToken) {
        githubService.setAuthToken(xService.accessToken);
      }
    },
    async authenticate() {
      if (!this.password) {
        this.authError = 'パスワードを入力してください';
        return;
      }

      try {
        const success = await xService.authenticate(this.password);
        if (success) {
          // XサービスとGitHubサービスの両方にトークンを設定
          const token = xService.accessToken;
          githubService.setAuthToken(token);
          this.updateAuthState();
          this.$emit('authenticated');
          this.password = '';
          this.authError = '';
        } else {
          this.authError = '認証に失敗しました';
        }
      } catch (error) {
        console.error('認証エラー:', error);
        this.authError = error.message || '認証に失敗しました';
      }
    },
    logout() {
      xService.logout();
      githubService.logout();
      this.updateAuthState();
      this.$emit('unauthenticated');
    }
  }
}
</script>

<style scoped>
.settings-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 20px;
}

.auth-section {
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.auth-description {
  margin: 0 0 16px 0;
  color: #666;
  font-size: 0.875rem;
}

.form-group {
  display: flex;
  gap: 8px;
}

.form-group input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
}

.form-group input:focus {
  outline: none;
  border-color: #1da1f2;
  box-shadow: 0 0 0 2px rgba(29, 161, 242, 0.2);
}

.auth-button {
  padding: 8px 16px;
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.auth-button:hover {
  background-color: #1a91da;
}

.error-message {
  margin: 8px 0 0 0;
  color: #e53935;
  font-size: 0.875rem;
}

.auth-success {
  text-align: center;
  color: #2e7d32;
}

.auth-success p {
  margin: 0 0 12px 0;
}

.logout-button {
  padding: 8px 16px;
  background-color: white;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-button:hover {
  background-color: #f5f5f5;
  color: #e53935;
  border-color: #e53935;
}

@media (max-width: 480px) {
  .modal-content {
    width: 95%;
  }
  
  .modal-header {
    padding: 12px 16px;
  }
  
  .modal-body {
    padding: 16px;
  }
}
</style>
<template>
  <div class="oauth-callback">
    <div class="callback-content">
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin"></i>
        <p>認証を処理中...</p>
      </div>
      
      <div v-else-if="success" class="success">
        <i class="fas fa-check-circle"></i>
        <p>認証が完了しました！</p>
        <p>アプリに戻ります...</p>
      </div>
      
      <div v-else class="error">
        <i class="fas fa-exclamation-circle"></i>
        <p>認証に失敗しました</p>
        <p>{{ errorMessage }}</p>
        <button @click="goHome" class="home-button">ホームに戻る</button>
      </div>
    </div>
  </div>
</template>

<script>
import xService from '../services/xService';
import githubService from '../services/githubService';

export default {
  name: 'OAuthCallback',
  data() {
    return {
      loading: true,
      success: false,
      errorMessage: ''
    }
  },
  async mounted() {
    await this.handleCallback();
  },
  methods: {
    async handleCallback() {
      try {
        // URLからクエリパラメータを取得
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        const username = urlParams.get('username');
        const error = urlParams.get('error');
        
        if (error) {
          throw new Error(decodeURIComponent(error));
        }
        
        if (!token) {
          throw new Error('認証トークンが取得できませんでした');
        }
        
        // 認証成功時の処理
        // xServiceにトークンを設定
        xService.accessToken = token;
        xService.isAuthenticated = true;
        xService.tokenExpiry = new Date(Date.now() + 60 * 60 * 1000); // 1時間後
        
        // GitHubサービスにもトークンを設定
        githubService.setAuthToken(token);
        
        // ローカルストレージに保存
        const settings = {
          isAuthenticated: true,
          xUsername: username ? decodeURIComponent(username) : ''
        };
        localStorage.setItem('tweetfleet-settings', JSON.stringify(settings));
        
        this.success = true;
        this.loading = false;
        
        // 2秒後にホーム画面に戻る
        setTimeout(() => {
          this.goHome();
        }, 2000);
        
      } catch (error) {
        console.error('OAuth コールバック処理エラー:', error);
        this.errorMessage = error.message;
        this.loading = false;
      }
    },
    goHome() {
      // ホーム画面に戻る（現在はSPAなのでwindow.locationを使用）
      window.location.href = '/';
    }
  }
}
</script>

<style scoped>
.oauth-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.callback-content {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.loading i,
.success i,
.error i {
  font-size: 3rem;
  margin-bottom: 16px;
}

.loading i {
  color: #1da1f2;
}

.success i {
  color: #2e7d32;
}

.error i {
  color: #e53935;
}

.loading p,
.success p,
.error p {
  margin: 8px 0;
  color: #333;
}

.home-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #1da1f2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.home-button:hover {
  background-color: #1a91da;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> 
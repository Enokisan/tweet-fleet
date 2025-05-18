import axios from 'axios';

class XService {
  constructor() {
    this.apiUrl = import.meta.env.VITE_BACKEND_API_URL;
    this.accessToken = null;
    this.isAuthenticated = false;
    this.tokenExpiry = null;
    
    // 初期化時の設定値をログ出力
    console.log('API設定:', {
      apiUrl: this.apiUrl,
      isAuthenticated: this.isAuthenticated
    });
  }

  async authenticate(password) {
    try {
      console.log('認証リクエスト開始:', {
        apiUrl: `${this.apiUrl}/api/auth/login`,
        password: password ? '****' : undefined
      });

      const response = await axios.post(
        `${this.apiUrl}/api/auth/login`,
        { password }
      );
      
      this.accessToken = response.data.access_token;
      this.isAuthenticated = true;
      // トークンの有効期限を1時間後に設定
      this.tokenExpiry = new Date(Date.now() + 60 * 60 * 1000);
      return true;
    } catch (error) {
      console.error('認証エラー:', error);
      return false;
    }
  }

  logout() {
    this.accessToken = null;
    this.isAuthenticated = false;
    this.tokenExpiry = null;
  }

  isTokenValid() {
    if (!this.tokenExpiry) return false;
    return new Date() < this.tokenExpiry;
  }

  async postTweet(content) {
    if (!this.isAuthenticated || !this.accessToken) {
      throw new Error('パスワード認証が必要です');
    }

    if (!this.isTokenValid()) {
      this.logout();
      throw new Error('トークンの有効期限が切れています');
    }

    try {
      console.log('ツイート投稿開始:', {
        apiUrl: `${this.apiUrl}/api/tweets`,
        content: content,
        isAuthenticated: this.isAuthenticated,
        tokenExpiry: this.tokenExpiry
      });

      const response = await axios.post(
        `${this.apiUrl}/api/tweets`,
        {
          text: content
        },
        {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('ツイート投稿レスポンス:', response.data);
      return response.data;
    } catch (error) {
      console.error('ツイート投稿エラー詳細:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers
      });

      if (error.response?.status === 401) {
        this.logout();
        throw new Error('認証が必要です');
      }
      
      throw new Error(`ツイートの投稿に失敗しました: ${error.message}`);
    }
  }
}

export default new XService(); 
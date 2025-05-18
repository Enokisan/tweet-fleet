import axios from 'axios';

class XService {
  constructor() {
    this.apiUrl = import.meta.env.VITE_BACKEND_API_URL;
    this.adminToken = import.meta.env.VITE_X_ADMIN_TOKEN;
    this.isAuthenticated = false;
    
    // 初期化時の設定値をログ出力
    console.log('API設定:', {
      apiUrl: this.apiUrl,
      hasAdminToken: !!this.adminToken
    });
  }

  authenticate(password) {
    if (password === import.meta.env.VITE_X_PASSWORD) {
      this.isAuthenticated = true;
      return true;
    }
    return false;
  }

  logout() {
    this.isAuthenticated = false;
  }

  async postTweet(content) {
    if (!this.adminToken) {
      throw new Error('管理者認証が必要です');
    }

    if (!this.isAuthenticated) {
      throw new Error('パスワード認証が必要です');
    }

    try {
      console.log('ツイート投稿開始:', {
        apiUrl: `${this.apiUrl}/api/tweets`,
        content: content,
        adminToken: this.adminToken
      });

      const response = await axios.post(
        `${this.apiUrl}/api/tweets`,
        {
          text: content
        },
        {
          headers: {
            'X-Admin-Token': this.adminToken,
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
        throw new Error('管理者認証が必要です');
      }
      
      throw new Error(`ツイートの投稿に失敗しました: ${error.message}`);
    }
  }
}

export default new XService(); 
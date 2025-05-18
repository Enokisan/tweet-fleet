import axios from 'axios';

class XService {
  constructor() {
    this.apiUrl = import.meta.env.VITE_BACKEND_API_URL;
    this.adminToken = localStorage.getItem('admin-token');
    
    // 初期化時の設定値をログ出力
    console.log('API設定:', {
      apiUrl: this.apiUrl,
      hasAdminToken: !!this.adminToken
    });
  }

  setAdminToken(token) {
    this.adminToken = token;
    localStorage.setItem('admin-token', token);
  }

  async postTweet(content) {
    if (!this.adminToken) {
      throw new Error('管理者認証が必要です');
    }

    try {
      console.log('ツイート投稿開始:', {
        apiUrl: `${this.apiUrl}/api/tweets`,
        content: content
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
        status: error.response?.status
      });

      if (error.response?.status === 401) {
        throw new Error('管理者認証が必要です');
      }
      
      throw new Error(`ツイートの投稿に失敗しました: ${error.message}`);
    }
  }
}

export default new XService(); 
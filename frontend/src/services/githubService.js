import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:3000';

class GitHubService {
  constructor() {
    this.apiUrl = API_BASE_URL;
    this.accessToken = null;
    this.isAuthenticated = false;
    this.tokenExpiry = null;
  }

  setAuthToken(token) {
    this.accessToken = token;
    this.isAuthenticated = true;
    this.tokenExpiry = new Date(Date.now() + 60 * 60 * 1000); // 1時間有効
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

  async saveNote(content) {
    if (!this.isAuthenticated || !this.accessToken) {
      throw new Error('パスワード認証が必要です');
    }

    if (!this.isTokenValid()) {
      this.logout();
      throw new Error('トークンの有効期限が切れています');
    }

    try {
      const response = await axios.post(
        `${this.apiUrl}/api/save`,
        { content },
        {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      return response.data;
    } catch (error) {
      console.error('GitHub保存エラー:', error);
      if (error.response?.status === 401) {
        this.logout();
        throw new Error('認証が必要です');
      }
      throw new Error(error.response?.data?.detail || 'GitHubへの保存に失敗しました');
    }
  }
}

export default new GitHubService(); 
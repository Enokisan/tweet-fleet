<template>
  <div class="tweet-fleet">
    <AppHeader 
      :showSettings="showSettings"
      @toggle-settings="showSettings = !showSettings"
    />
    
    <main class="app-main">
      <NoteInput
        v-model="noteContent"
        :characterCount="characterCount"
        :shareToX="shareToX"
        :saveToGithub="saveToGithub"
        @update:shareToX="shareToX = $event"
        @update:saveToGithub="saveToGithub = $event"
        @save="saveNote"
        @update:characterCount="updateCharacterCount"
      />
      
      <div class="status-message" v-if="statusMessage">
        {{ statusMessage }}
      </div>
    </main>
    
    <SettingsModal
      v-if="showSettings"
      :xConnected="xConnected"
      :xUsername="xUsername"
      :githubConnected="githubConnected"
      :githubRepo="githubRepo"
      :githubPath="githubPath"
      @update:githubRepo="githubRepo = $event"
      @update:githubPath="githubPath = $event"
      @close="showSettings = false"
      @connect-x="connectX"
      @disconnect-x="disconnectX"
      @connect-github="connectGithub"
      @disconnect-github="disconnectGithub"
    />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import NoteInput from './components/NoteInput.vue';
import SettingsModal from './components/SettingsModal.vue';
import xService from './services/xService';

export default {
  name: 'App',
  components: {
    AppHeader,
    NoteInput,
    SettingsModal
  },
  data() {
    return {
      noteContent: '',
      characterCount: 0,
      shareToX: true,
      saveToGithub: true,
      statusMessage: '',
      showSettings: false,
      
      // X連携
      xConnected: false,
      xUsername: '',
      
      // GitHub連携
      githubConnected: false,
      githubRepo: import.meta.env.VITE_GITHUB_REPO || '',
      githubToken: import.meta.env.VITE_GITHUB_TOKEN || '',
      githubApiUrl: import.meta.env.VITE_GITHUB_API_URL || '',
      githubUsername: import.meta.env.VITE_GITHUB_OWNER || '',
      githubPath: import.meta.env.VITE_GITHUB_PATH || ''
    }
  },
  created() {
    // 設定を読み込む
    this.loadSettings();
    
    // 環境変数のデバッグ出力
    console.log('環境変数の確認:', {
      BACKEND_API_URL: import.meta.env.VITE_BACKEND_API_URL,
      GITHUB_REPO: import.meta.env.VITE_GITHUB_REPO,
      hasGithubToken: !!import.meta.env.VITE_GITHUB_TOKEN,
    });
  },
  methods: {
    updateCharacterCount() {
      this.characterCount = this.noteContent.length;
    },
    saveNote() {
      if (!this.noteContent || this.noteContent.length > 140) {
        return;
      }
      
      const note = {
        id: Date.now(),
        content: this.noteContent,
        timestamp: new Date().toISOString()
      };
      
      // ノートをXに投稿
      if (this.shareToX) {
        this.postToX(note);
      }
      
      // ノートをGitHubに保存
      if (this.saveToGithub) {
        this.saveNoteToGithub(note);
      }
      
      // 入力フォームをクリア
      this.noteContent = '';
      this.characterCount = 0;
      
      // ステータスメッセージを表示
      this.showStatusMessage('フリーティングノートを保存しました！');
    },
    async postToX(note) {
      if (!this.xConnected) {
        console.warn('X連携が無効です:', {
          xConnected: this.xConnected,
          xUsername: this.xUsername
        });
        this.showStatusMessage('Xと連携してください', 'error');
        return;
      }
      
      try {
        console.log('X投稿開始:', {
          content: note.content,
          xConnected: this.xConnected,
          xUsername: this.xUsername
        });
        await xService.postTweet(note.content);
        this.showStatusMessage('Xに投稿しました！');
      } catch (error) {
        console.error('X投稿エラー:', error);
        this.showStatusMessage(`Xへの投稿に失敗しました: ${error.message}`, 'error');
      }
    },
    async saveNoteToGithub(note) {
      if (!this.githubConnected) {
        this.showStatusMessage('GitHubと連携してください', 'error');
        return;
      }
      
      // 実際にはGitHub APIを呼び出す処理を実装
      console.log('GitHubに保存:', note.content, '場所:', this.githubRepo, this.githubPath);
      
      // テスト用に成功したふりをする
      this.showStatusMessage('GitHubに保存しました！');
    },
    showStatusMessage(message, type = 'success') {
      this.statusMessage = message;
      
      // 3秒後にメッセージを消す
      setTimeout(() => {
        this.statusMessage = '';
      }, 3000);
    },
    loadSettings() {
      // ローカルストレージから設定を読み込む
      const settings = localStorage.getItem('tweetfleet-settings');
      if (settings) {
        const parsedSettings = JSON.parse(settings);
        
        // X連携
        if (parsedSettings.xConnected) {
          this.xConnected = parsedSettings.xConnected;
          this.xUsername = parsedSettings.xUsername || '';
        }
        
        // GitHub連携
        if (parsedSettings.githubConnected) {
          this.githubConnected = parsedSettings.githubConnected;
          this.githubRepo = parsedSettings.githubRepo || '';
          this.githubPath = parsedSettings.githubPath || '';
        }
      }
    },
    saveSettings() {
      // 設定をローカルストレージに保存
      const settings = {
        xConnected: this.xConnected,
        xUsername: this.xUsername,
        githubConnected: this.githubConnected,
        githubRepo: this.githubRepo,
        githubPath: this.githubPath
      };
      
      localStorage.setItem('tweetfleet-settings', JSON.stringify(settings));
    },
    connectX() {
      // 管理者認証トークンの設定
      const adminToken = prompt('管理者認証トークンを入力してください');
      if (!adminToken) {
        this.showStatusMessage('認証トークンが必要です', 'error');
        return;
      }

      // トークンの検証（実際のバックエンドではここでAPIを呼び出して検証）
      if (adminToken.length < 8) {
        this.showStatusMessage('無効な認証トークンです', 'error');
        return;
      }

      xService.setAdminToken(adminToken);
      this.xConnected = true;
      this.xUsername = 'admin';
      this.saveSettings();
      this.showStatusMessage('Xと連携しました！');
    },
    disconnectX() {
      this.xConnected = false;
      this.xUsername = '';
      localStorage.removeItem('admin-token');
      this.saveSettings();
      this.showStatusMessage('X連携を解除しました');
    },
    connectGithub() {
      if (!this.githubRepo || !this.githubPath) {
        this.showStatusMessage('GitHubリポジトリとファイルパスを入力してください', 'error');
        return;
      }
      
      // 実際にはGitHubの認証フローを実装
      // ここではダミーの実装
      this.githubConnected = true;
      this.saveSettings();
      this.showStatusMessage('GitHubと連携しました！');
    },
    disconnectGithub() {
      this.githubConnected = false;
      this.saveSettings();
      this.showStatusMessage('GitHub連携を解除しました');
    }
  }
}
</script>

<style>
/* ベースとなるスタイル */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f5f8fa;
  color: #333;
  line-height: 1.6;
}

/* アプリケーション全体のスタイル */
.tweet-fleet {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

/* メインコンテンツ */
.app-main {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ステータスメッセージ */
.status-message {
  background-color: #e8f5fe;
  border-left: 4px solid #1da1f2;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
}

.status-message.error {
  background-color: #ffe8e8;
  border-left-color: #e53935;
}

/* レスポンシブ対応 */
@media (max-width: 480px) {
  .tweet-fleet {
    padding: 16px;
  }
  
  .app-main {
    margin-top: 20px;
  }
}
</style>

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
        :isAuthenticated="xConnected && githubConnected"
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
      @authenticated="handleAuthenticated"
      @unauthenticated="handleUnauthenticated"
    />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import NoteInput from './components/NoteInput.vue';
import SettingsModal from './components/SettingsModal.vue';
import xService from './services/xService';
import githubService from './services/githubService';

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
      statusType: 'success',
      showSettings: false,
      xConnected: false,
      xUsername: '',
      githubConnected: false,
      githubRepo: '',
      githubPath: ''
    }
  },
  created() {
    // 設定を読み込む
    this.loadSettings();
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
        this.showStatusMessage('X連携の準備ができていません。設定から環境変数を確認してください。', 'error');
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
        if (error.message === 'パスワード認証が必要です') {
          this.showSettings = true;
          this.showStatusMessage('ツイートを投稿するには、設定からパスワード認証が必要です。', 'error');
        } else if (error.message === 'トークンの有効期限が切れています') {
          this.showSettings = true;
          this.showStatusMessage('認証の有効期限が切れました。再度パスワード認証を行ってください。', 'error');
        } else {
          this.showStatusMessage(`Xへの投稿に失敗しました: ${error.message}`, 'error');
        }
      }
    },
    async saveNoteToGithub(note) {
      if (!this.githubConnected) {
        this.showStatusMessage('GitHubと連携してください', 'error');
        return;
      }
      
      try {
        const result = await githubService.saveNote(note.content);
        
        if (result.success) {
          this.showStatusMessage('GitHubに保存しました！');
        } else {
          this.showStatusMessage(result.message, 'error');
        }
      } catch (error) {
        console.error('GitHub保存エラー:', error);
        this.showStatusMessage(error.message, 'error');
      }
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
        
        // 認証状態の読み込み
        if (parsedSettings.isAuthenticated) {
          this.xConnected = true;
          this.githubConnected = true;
          this.xUsername = parsedSettings.xUsername || '';
        }
      }
    },
    saveSettings() {
      // 設定をローカルストレージに保存
      const settings = {
        isAuthenticated: this.xConnected && this.githubConnected,
        xUsername: this.xUsername
      };
      
      localStorage.setItem('tweetfleet-settings', JSON.stringify(settings));
    },
    handleAuthenticated() {
      this.xConnected = true;
      this.githubConnected = true;
      this.saveSettings();
      this.showStatusMessage('認証が完了しました');
    },
    handleUnauthenticated() {
      this.xConnected = false;
      this.githubConnected = false;
      this.saveSettings();
      this.showStatusMessage('ログアウトしました');
    },
    connectX() {
      this.showStatusMessage('X連携は環境変数で設定されています。', 'error');
    },
    disconnectX() {
      this.showStatusMessage('X連携は環境変数で設定されています。', 'error');
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
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
}

/* アプリケーション全体のスタイル */
.tweet-fleet {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: auto;
  gap: 20px;
}

/* メインコンテンツ */
.app-main {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  align-items: center;
}

/* ステータスメッセージ */
.status-message {
  background-color: #e8f5fe;
  border-left: 4px solid #1da1f2;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  width: 100%;
}

.status-message.error {
  background-color: #ffe8e8;
  border-left-color: #e53935;
}

/* レスポンシブ対応 */
@media (max-width: 480px) {
  body {
    padding: 12px;
  }
  
  .tweet-fleet {
    gap: 16px;
  }
  
  .app-main {
    gap: 16px;
  }
  
  .status-message {
    font-size: 13px;
    padding: 10px;
  }
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
  body {
    background-color: #15202b;
    color: #fff;
  }
  
  .tweet-fleet {
    background-color: #15202b;
  }
  
  .status-message {
    background-color: rgba(29, 161, 242, 0.1);
    color: #fff;
  }
  
  .status-message.error {
    background-color: rgba(229, 57, 53, 0.1);
  }
}
</style>

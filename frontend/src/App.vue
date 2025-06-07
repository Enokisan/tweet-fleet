<template>
  <router-view />
</template>

<script>
export default {
  name: 'App'
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

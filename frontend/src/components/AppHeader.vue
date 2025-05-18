<!-- src/components/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="logo">
      <h1>TweetFleet</h1>
      <p class="tagline">思考をフリートし、ツイートする</p>
    </div>
    <button class="settings-button" @click="$emit('toggle-settings')">
      <i class="fas fa-cog"></i>
    </button>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  emits: ['toggle-settings']
}
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.logo h1 {
  font-size: 28px;
  margin: 0;
  color: #1da1f2;
}

.tagline {
  margin: 5px 0 0;
  font-size: 14px;
  color: #666;
}

.settings-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #1da1f2;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.settings-button:hover {
  background-color: rgba(29, 161, 242, 0.1);
}

@media (max-width: 480px) {
  .app-header {
    margin-bottom: 20px;
  }
  
  .logo h1 {
    font-size: 24px;
  }
}
</style>
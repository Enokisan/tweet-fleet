import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import OAuthCallback from './components/OAuthCallback.vue'
import '@fortawesome/fontawesome-free/css/all.css'
import './style.css'

const routes = [
  { path: '/', component: Home },
  { path: '/auth/callback', component: OAuthCallback }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
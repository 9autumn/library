import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/global.css'

// 微信浏览器缓存控制
const isWechat = /micromessenger/i.test(navigator.userAgent)
const currentVersion = '1.0.0' // 每次更新代码时修改这个版本号

// 检查版本并强制刷新
const checkVersion = () => {
  const storedVersion = localStorage.getItem('app_version')
  if (storedVersion !== currentVersion) {
    // 清除所有缓存
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => {
          caches.delete(name)
        })
      })
    }
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(registrations => {
        registrations.forEach(registration => registration.unregister())
      })
    }
    // 清除localStorage
    localStorage.clear()
    // 存储新版本
    localStorage.setItem('app_version', currentVersion)
    // 强制刷新
    if (isWechat) {
      // 微信浏览器特殊处理
      window.location.reload(true)
    } else {
      window.location.reload()
    }
  } else {
    localStorage.setItem('app_version', currentVersion)
  }
}

// 微信浏览器特殊处理
if (isWechat) {
  // 添加时间戳防止缓存
  const timestamp = Date.now()
  document.title = `青山图书馆_${timestamp}`
  
  // 定期检查更新
  setInterval(() => {
    checkVersion()
  }, 30000) // 每30秒检查一次
}

// 应用启动
checkVersion()
const registerServiceWorker = () => {
  if ('serviceWorker' in navigator && import.meta.env.PROD) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch(() => {})
    })
  }
}
registerServiceWorker()
createApp(App).use(router).mount('#app')



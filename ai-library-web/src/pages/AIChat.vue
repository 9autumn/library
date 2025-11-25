<template>
  <div class="chat-container">
    <!-- 背景视频层 -->
    <div class="video-background">
      <video 
        ref="videoRef"
        autoplay 
        muted
        loop
        playsinline
        webkit-playsinline
        x5-video-player-type="h5"
        x5-video-player-fullscreen="false"
        x5-video-orientation="portraint"
        @loadeddata="onVideoLoaded"
      >
        <source src="/videos/background.mp4" type="video/mp4">
      </video>
      
    </div>

    <!-- 内容层 -->
    <div class="chat-page">
      <!-- 顶部导航栏 -->
      <header class="nav">
      <div class="nav-container">
        <div class="brand">
          <div class="logo">
            <img src="/images/logo.png" alt="馆徽">
          </div>
          <div class="brand-text">
            <h1>青山区图书馆</h1>
            <p>Qingshan District Library</p>
          </div>
        </div>
      </div>
    </header>

    <!-- 遮罩层 -->
    <div class="overlay" v-if="showOverlay" @click="closeSidebars"></div>
    
    
    <!-- 右侧边栏 -->
    <RightSidebar 
      @faq-selected="onFaqSelected" 
      @recommendation-selected="onRecommendationSelected"
      @sidebar-toggle="onRightSidebarToggle"
    />
    


    <!-- 主聊天区域 -->
    <div class="chat-main" :class="{ 'with-sidebars': rightSidebarOpen }">
      <div class="chat-panel" :class="{ 'has-messages': hasMessages }" v-if="isDialogVisible">
        <div class="messages" ref="msgBox">
          <div v-for="(m,i) in messages" :key="i" :class="['msg', m.role]">
            <div 
              class="bubble" 
              :class="{ 'markdown-content': m.role === 'assistant' }"
              v-html="m.role === 'assistant' ? renderMarkdown(m.content) : m.content"
            ></div>
          </div>
        </div>
        <form class="input" @submit.prevent="onSend">
          <!-- 输入框区域 -->
          <div class="input-main">
            <div class="input-container">
              <textarea 
                v-model="text" 
                ref="textareaRef"
                :placeholder="isEnglish ? 'Please enter your question...' : '请输入问题...'"
                @input="adjustTextareaHeight"
                @keydown.enter.exact.prevent="onSend"
                @keydown.shift.enter.prevent="handleShiftEnter"
              ></textarea>
              <button type="submit" :disabled="!canSend" class="send-btn-inside">
                <svg v-if="!loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 2L11 13"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z"/>
                </svg>
                <div v-else class="loading-spinner"></div>
              </button>
            </div>
          </div>
          
          <!-- 底部功能按钮 -->
          <div class="input-bottom">
            <button type="button" class="bottom-btn web-search-btn" title="联网搜索">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              联网搜索
            </button>
            <button type="button" class="bottom-btn" title="模型切换">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              模型切换
            </button>
            <button type="button" class="bottom-btn" title="更多技能">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
              </svg>
              更多技能
            </button>
          </div>
          
          <!-- 提示文字 -->
          <div class="input-hint">
            shift+enter换行, enter发送
          </div>
        </form>
      </div>
      
      <!-- 开始AI对话卡片 -->
      <div class="ai-start-card" v-if="!isDialogVisible" @click="startNewChat">
        <div class="card-container">
          <!-- 顶部圆形图标 -->
          <div class="card-icon">
            <img src="/images/background.png" alt="图书馆">
          </div>
          
          <!-- 卡片文字内容 -->
          <div class="card-text">
            <h3>青山区图书馆AI助手</h3>
            <p>我是您的专属图书助手，随时为您服务</p>
          </div>
          
          <!-- 金色渐变按钮 -->
          <div class="start-button">
            <div class="button-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z"/>
              </svg>
            </div>
            <span>AI开始对话</span>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted, computed } from 'vue'
import { streamChatMessage } from '../services/dify'
import { renderMarkdown } from '../utils/markdown'
import RightSidebar from '../components/RightSidebar.vue'

// ==================== 类型定义 ====================
// 微信JSBridge类型声明
declare const WeixinJSBridge: any


type Msg = { role: 'user' | 'assistant', content: string }

// ==================== 状态管理 ====================
// 消息相关
const messages = ref<Msg[]>([
  { role: 'assistant', content: '您好，我是青山区图书馆内 AI 助手，欢迎提问。' }
])
const text = ref('')
const loading = ref(false)

// DOM 引用
const msgBox = ref<HTMLDivElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const videoRef = ref<HTMLVideoElement | null>(null)

// UI 状态
const isEnglish = ref(false)
const isDialogVisible = ref(false)
const showSidebars = ref(false)
const showOverlay = ref(false)
const rightSidebarOpen = ref(false)
const isMobile = ref(false)

// ==================== 计算属性 ====================
const hasMessages = computed(() => messages.value.length > 1)
const canSend = computed(() => !loading.value && text.value.trim().length > 0)

// ==================== 工具函数 ====================
/**
 * 滚动消息列表到底部
 */
function scrollToBottom() {
  nextTick(() => {
    const el = msgBox.value
    if (el) {
      el.scrollTop = el.scrollHeight
    }
  })
}

/**
 * 自动调整输入框高度
 * 根据内容动态调整，最大高度 120px
 */
function adjustTextareaHeight() {
  const textarea = textareaRef.value
  if (textarea) {
    textarea.style.height = 'auto'
    const newHeight = Math.min(textarea.scrollHeight, 120)
    textarea.style.height = `${newHeight}px`
  }
}

/**
 * 处理 Shift+Enter 换行
 */
function handleShiftEnter() {
  text.value += '\n'
  nextTick(() => adjustTextareaHeight())
}


// ==================== 消息处理 ====================
/**
 * 发送消息
 */
async function onSend() {
  // 验证输入
  if (!text.value.trim()) {
    return
  }
  
  const input = text.value.trim()
  
  // 添加用户消息
  messages.value.push({ 
    role: 'user', 
    content: input 
  })
  
  // 清空输入框并重置高度
  text.value = ''
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  })
  
  // 开始加载
  loading.value = true
  
  // 添加空的助手消息用于流式更新
  const assistantIndex = messages.value.push({ 
    role: 'assistant', 
    content: '' 
  }) - 1
  
  scrollToBottom()
  
  try {
    // 流式接收消息
    await streamChatMessage(input, (chunk) => {
      messages.value[assistantIndex].content += chunk
      scrollToBottom()
    })
  } catch (error: any) {
    // 错误处理
    const errorMessage = error.message || '未知错误'
    messages.value[assistantIndex].content = `❌ 抱歉，出现错误：${errorMessage}`
    console.error('消息发送失败:', error)
  } finally {
    loading.value = false
  }
}

// ==================== UI 交互 ====================
/**
 * 开启新对话
 */
function startNewChat() {
  const welcomeMessage = isEnglish.value 
    ? 'Hello, I am the library AI assistant, welcome to ask questions.'
    : '您好，我是青山区图书馆内 AI 助手，欢迎提问。'
  
  messages.value = [
    { role: 'assistant', content: welcomeMessage }
  ]
  
  // 显示对话框
  isDialogVisible.value = true
}

/**
 * 语言切换处理
 */
function onLanguageChange(english: boolean) {
  isEnglish.value = english
  
  // 如果只有欢迎消息，则更新语言
  if (messages.value.length === 1) {
    messages.value[0].content = english 
      ? 'Hello, I am the library AI assistant, welcome to ask questions.'
      : '您好，我是青山区图书馆内 AI 助手，欢迎提问。'
  }
}

/**
 * 常见问题选择处理
 */
function onFaqSelected(item: any) {
  text.value = item.question
  nextTick(() => adjustTextareaHeight())
}

/**
 * 馆内推荐选择处理
 */
function onRecommendationSelected(item: any) {
  const prompt = isEnglish.value 
    ? `I want to use ${item.title} service: ${item.description}`
    : `我想使用${item.title}服务：${item.description}`
  text.value = prompt
  nextTick(() => adjustTextareaHeight())
}

// ==================== 侧边栏管理 ====================
/**
 * 关闭所有侧边栏
 */
function closeSidebars() {
  showSidebars.value = false
  showOverlay.value = false
  rightSidebarOpen.value = false
}



/**
 * 右侧边栏切换处理
 */
function onRightSidebarToggle(isOpen: boolean) {
  rightSidebarOpen.value = isOpen
  showSidebars.value = isOpen
  
  // 移动端显示遮罩
  if (window.innerWidth <= 1024) {
    showOverlay.value = isOpen
  }
}

// ==================== 响应式处理 ====================
/**
 * 窗口大小变化处理
 * 移动端自动关闭侧边栏
 */
function handleResize() {
  const isMobileNow = window.innerWidth <= 1024
  isMobile.value = isMobileNow
  
  // 移动端关闭所有侧边栏
  if (isMobileNow) {
    closeSidebars()
  }
}

// ==================== 视频控制函数 ====================
/**
 * 视频加载完成
 */
const onVideoLoaded = () => {
  if (videoRef.value) {
    // 页面加载时自动有声播放一次
    videoRef.value.muted = false
    videoRef.value.volume = 1.0
    videoRef.value.loop = false
    
    // 监听视频播放结束，然后切换到静音循环
    videoRef.value.addEventListener('ended', () => {
      if (videoRef.value) {
        videoRef.value.muted = true
        videoRef.value.volume = 0
        videoRef.value.loop = true
        videoRef.value.currentTime = 0
        videoRef.value.play()
      }
    }, { once: true })
  }
}

// ==================== 生命周期钩子 ====================
/**
 * 组件挂载时的初始化
 */
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  handleResize()
  
  // 添加聊天模式样式类
  const body = document.body
  const app = document.getElementById('app')
  
  body?.classList.add('chat-mode')
  app?.classList.add('chat-mode')
  
  // 微信端视频播放处理
  const isWechat = /micromessenger/i.test(navigator.userAgent)
  if (isWechat && videoRef.value) {
    // 设置视频属性
    videoRef.value.playsInline = true
    videoRef.value.setAttribute('webkit-playsinline', 'true')
    videoRef.value.setAttribute('x5-playsinline', 'true')
    
    // 强制播放函数
    const forcePlayVideo = () => {
      if (videoRef.value) {
        // 微信端先尝试有声播放
        videoRef.value.muted = false
        videoRef.value.volume = 1.0
        videoRef.value.loop = false
        
        videoRef.value.play().catch(() => {
          // 如果有声播放失败，改为静音播放
          if (videoRef.value) {
            videoRef.value.muted = true
            videoRef.value.volume = 0
            videoRef.value.loop = true
            videoRef.value.play().catch(() => {
              // 静默失败
            })
          }
        })
      }
    }
    
    // 方式1: 微信JSBridge (iOS主要)
    if (typeof WeixinJSBridge !== 'undefined') {
      WeixinJSBridge.invoke('getNetworkType', {}, forcePlayVideo)
    } else {
      document.addEventListener('WeixinJSBridgeReady', forcePlayVideo, { once: true })
    }
    
    // 方式2: 页面加载完成后立即尝试 (Android)
    setTimeout(forcePlayVideo, 100)
    setTimeout(forcePlayVideo, 500)
    setTimeout(forcePlayVideo, 1000)
    
    // 方式3: 页面可见时尝试
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) {
        forcePlayVideo()
      }
    })
    
    // 方式4: 用户任意交互时播放 (最后保障)
    document.addEventListener('touchstart', forcePlayVideo, { once: true })
    document.addEventListener('click', forcePlayVideo, { once: true })
  }
})

/**
 * 组件卸载时的清理
 */
onUnmounted(() => {
  // 移除事件监听
  window.removeEventListener('resize', handleResize)
  
  // 清理聊天模式样式类
  const body = document.body
  const app = document.getElementById('app')
  
  body?.classList.remove('chat-mode')
  app?.classList.remove('chat-mode')
  
  // 清理视频
  if (videoRef.value) {
    videoRef.value.pause()
    videoRef.value.currentTime = 0
  }
})
</script>

<style scoped>
/* ==================== 科技风容器和背景 ==================== */
.chat-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: var(--dark-gradient);
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
  /* 科技风视频遮罩 */
  background: radial-gradient(circle at center, transparent 0%, rgba(0, 212, 255, 0.1) 100%);
}

.video-background video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7) contrast(1.2);
}

/* ==================== 科技风页面布局 ==================== */
.chat-page {
  position: relative;
  z-index: 1;
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: transparent;
  /* 科技感网格叠加 */
  background-image:
    linear-gradient(45deg, rgba(0, 212, 255, 0.05) 25%, transparent 25%),
    linear-gradient(-45deg, rgba(0, 212, 255, 0.05) 25%, transparent 25%);
  background-size: 40px 40px;
}

/* ==================== 导航栏样式 ==================== */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(173, 216, 230, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(135, 206, 235, 0.3);
  height: 60px;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand-text h1 {
  font-size: 18px;
  font-weight: 600;
  color: #2F4F4F;
  margin: 0;
  line-height: 1.2;
}

.brand-text p {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.2;
}

/* 移动端导航栏优化 */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 16px;
  }
  
  .logo {
    width: 32px;
    height: 32px;
  }
  
  .brand-text h1 {
    font-size: 16px;
  }
  
  .brand-text p {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 12px;
  }
  
  .brand {
    gap: 8px;
  }
  
  .logo {
    width: 28px;
    height: 28px;
  }
  
  .brand-text h1 {
    font-size: 15px;
  }
  
  .brand-text p {
    font-size: 10px;
  }
}

/* 强制覆盖全局背景 */
:global(body),
:global(#app) {
  background: transparent !important;
  background-image: none !important;
}




/* 移动端侧边栏遮罩 - 浅蓝色增强 */
.overlay {
  position: fixed;
  top: 50px;  /* 从导航栏下方开始，减少间距 */
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(135, 206, 235, 0.6) 0%, rgba(100, 149, 237, 0.7) 100%);
  z-index: 999;
  backdrop-filter: blur(10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}


/* ==================== 主聊天区域 ==================== */
.chat-main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;  /* 改为居中，手机端会覆盖 */
  padding: 20px;
  margin: 0 auto;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 0;
  min-height: calc(100vh - 80px);
  max-width: 1200px;
  width: 100%;
}

.chat-main.with-sidebars {
  margin: 0 auto;
}

/* 侧边栏展开时调整 */
.chat-main.with-sidebars .chat-panel {
  max-width: 100%;
  width: 100%;
}

/* ==================== 对话框 ==================== */
.chat-panel {
  width: 100%;
  max-width: 100%;
  border-radius: 0;
  overflow: hidden;
  /* 完全透明背景 */
  background: transparent;
  backdrop-filter: none;
  box-shadow: none;
  border: none;
  position: relative;
  max-height: 100vh;
  transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
              max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 有对话时自动拉长 */
.chat-panel.has-messages {
  max-height: 85vh;
  max-width: 1000px;
}

/* ==================== 消息列表 ==================== */
.messages {
  height: 50vh;
  min-height: 350px;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  padding-top: 60px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: transparent;  /* 透明背景 */
  transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  scroll-behavior: smooth;
  border-radius: 0;
  margin: 0;
  box-shadow: none;
}

/* 对话增多时自动拉高 */
.chat-panel.has-messages .messages {
  height: 70vh;  /* 进一步增加高度 */
  min-height: 500px;  /* 增加最小高度 */
  padding: 28px;  /* 增加内边距 */
  gap: 24px;  /* 增加消息间距 */
}

.msg {
  display: flex;
  gap: 20px;  /* 增加间距 */
  align-items: flex-start;
  animation: fadeInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);  /* 优化动画 */
  margin-bottom: 8px;  /* 增加底部间距 */
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);  /* 增加动画效果 */
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.msg .role {
  display: none;
}

.bubble {
  background: rgba(255, 255, 255, 0.9);  /* 白色背景 */
  padding: 12px 16px;
  border-radius: 18px;  /* 圆角设计 */
  border: none;
  max-width: 80%;
  line-height: 1.5;
  word-wrap: break-word;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}

.bubble::before {
  content: '';
  position: absolute;
  top: 16px;  /* 调整位置 */
  left: -10px;  /* 调整位置 */
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 10px 10px 10px 0;  /* 增加尺寸 */
  border-color: transparent rgba(255, 255, 255, 0.9) transparent transparent;  /* 白色小箭头 */
  filter: drop-shadow(-2px 0 4px rgba(0, 0, 0, 0.1));  /* 添加阴影 */
}

.msg.user .bubble {
  background: rgba(255, 255, 255, 0.9);  /* 白色背景 */
  color: #333;  /* 深色字体 */
  margin-left: auto;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 80%;
}

.msg.user .bubble::before {
  left: auto;
  right: -10px;  /* 调整位置 */
  border-width: 10px 0 10px 10px;  /* 增加尺寸 */
  border-color: transparent transparent transparent rgba(255, 255, 255, 0.9);  /* 白色小箭头 */
  filter: drop-shadow(2px 0 4px rgba(0, 0, 0, 0.1));  /* 添加阴影 */
}

.msg.assistant .bubble {
  background: rgba(255, 255, 255, 0.9);  /* 白色背景 */
  border: none;
  color: #333;  /* 深色字体 */
  max-width: 85%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ==================== 输入区域 ==================== */
.input {
  padding: 20px;
  border-top: none;
  background: transparent;  /* 透明背景 */
  backdrop-filter: none;
  border-radius: 0;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;  /* 降低z-index，避免遮挡数字人背景 */
}

/* ==================== 主输入区域 ==================== */
.input-main {
  display: flex;
  gap: 12px;  /* 增加间距 */
  align-items: flex-end;
  margin-bottom: 16px;  /* 增加底部间距 */
  padding: 8px 0;  /* 增加内边距 */
}

/* 多行输入框 */
.input-main textarea {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 18px;  /* 圆角设计，参考图片 */
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  background: rgba(173, 216, 230, 0.65);  /* 浅蓝色背景，降低透明度 */
  backdrop-filter: blur(10px);
  color: #333;
  resize: none;
  min-height: 48px;
  max-height: 120px;
  line-height: 1.5;
  font-family: inherit;
  -webkit-text-size-adjust: 100%;
  transform: scale(1);
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-main textarea::-webkit-scrollbar {
  width: 6px;  /* 增加滚动条宽度 */
}

.input-main textarea::-webkit-scrollbar-track {
  background: transparent;
}

.input-main textarea::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.4);  /* 增强滚动条颜色 */
  border-radius: 3px;  /* 增加圆角 */
}

.input-main textarea::placeholder {
  color: rgba(255, 255, 255, 0.7);  /* 增强占位符颜色 */
  font-size: 16px;  /* 增加占位符字体大小 */
  font-weight: 400;  /* 添加字体粗细 */
}

.input-main textarea:focus {
  border-color: rgba(102, 126, 234, 0.7);  /* 增强焦点边框 */
  background: rgba(255, 255, 255, 0.18);  /* 增强焦点背景 */
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15), 0 6px 20px rgba(0, 0, 0, 0.15);  /* 增强焦点阴影 */
  transform: translateY(-1px);  /* 添加焦点动画 */
}

/* 保持旧的 input 样式作为备用 */
.input-main input {
  flex: 1;
  padding: 14px 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  -webkit-text-size-adjust: 100%;
  transform: scale(1);
}

.input-main input:focus {
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.2);
}

/* ==================== 操作按钮 ==================== */
.input-actions {
  display: flex;
  gap: 10px;  /* 增加间距 */
  align-items: center;
}

.action-btn {
  padding: 14px 20px;  /* 增加内边距 */
  border-radius: 20px;  /* 增加圆角 */
  border: 1px solid rgba(255, 255, 255, 0.35);  /* 增强边框 */
  background: rgba(255, 255, 255, 0.12);  /* 增强背景 */
  color: white;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;  /* 增加字体大小 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);  /* 优化过渡 */
  display: flex;
  align-items: center;
  gap: 8px;  /* 增加间距 */
  backdrop-filter: blur(12px);  /* 增强模糊效果 */
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);  /* 添加阴影 */
}

.action-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);  /* 增强悬停背景 */
  border-color: rgba(255, 255, 255, 0.6);  /* 增强悬停边框 */
  transform: translateY(-2px);  /* 增加悬停动画 */
  box-shadow: 0 4px 16px rgba(255, 255, 255, 0.25);  /* 增强悬停阴影 */
}

.action-btn:active:not(:disabled) {
  transform: translateY(0);
}

/* 科技风发送按钮 */
.send-btn {
  background: var(--glass-bg) !important;
  color: var(--primary-neon) !important;
  border: 2px solid var(--primary-neon) !important;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
  min-width: 60px;
  justify-content: center;
  font-weight: 600;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.send-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.3;
  transition: left var(--transition-fast);
}

.send-btn:hover::before {
  left: 100%;
}

.send-btn:hover {
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6) !important;
  transform: scale(1.1);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);  /* 增加悬停动画 */
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);  /* 增强悬停阴影 */
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;  /* 悬停时渐变变化 */
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* ==================== 底部功能按钮 ==================== */
/* 模型切换、更多技能等 - 扁平化设计 */
.input-bottom {
  display: flex;
  align-items: center;
  gap: 12px;  /* 增加间距 */
  justify-content: space-between;
  padding: 8px 0;  /* 增加内边距 */
}

.bottom-btn {
  padding: 8px 12px;
  border-radius: 12px;  /* 圆角设计，参考图片 */
  border: none;
  background: rgba(173, 216, 230, 0.8);  /* 浅蓝色背景 */
  color: #333;
  cursor: pointer;
  font-weight: 500;
  font-size: 12px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.bottom-btn:hover {
  background: rgba(255, 255, 255, 0.15);  /* 增强悬停背景 */
  border-color: rgba(255, 255, 255, 0.4);  /* 增强悬停边框 */
  color: white;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15);  /* 增强悬停阴影 */
  transform: translateY(-1px);  /* 添加悬停动画 */
}

.bottom-btn:active {
  transform: scale(0.98);
}

.bottom-btn svg {
  width: 14px;  /* 增加图标尺寸 */
  height: 14px;
  flex-shrink: 0;
}

.input-hint {
  font-size: 11px;  /* 增加字体大小 */
  color: rgba(255, 255, 255, 0.6);  /* 增强颜色 */
  font-style: italic;
  margin-left: auto;
  white-space: nowrap;
  font-weight: 400;  /* 添加字体粗细 */
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .chat-main.with-sidebars {
    margin-left: 280px;
    margin-right: 280px;
  }
}

@media (max-width: 1200px) {
  .chat-main.with-sidebars {
    margin-left: 60px;
    margin-right: 60px;
  }
  
  .chat-main.with-sidebars .chat-panel {
    max-width: 100%;
  }
}

@media (max-width: 1024px) {
  .chat-main {
    margin-left: 0;
    margin-right: 0;
    padding: 15px;
    width: 100%;
    max-width: 100%;
  }
  
  .chat-main.with-sidebars {
    margin-left: 0;
    margin-right: 0;
    width: 100%;
    max-width: 100%;
  }
  
  .chat-panel {
    max-width: 100%;
    width: 100%;
  }
  
  /* 移动端侧边栏样式 */
  .left-sidebar, .right-sidebar {
    z-index: 1003;
  }
  
  .left-sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .right-sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .overlay {
    display: block;
  }
}

/* ==================== 手机端优化（平板/手机） ==================== */
@media (max-width: 768px) {
  
  .chat-main {
    padding: 0;  /* 完全无边距 */
    margin: 0;
    padding-top: 60px;  /* 给导航栏留空间 */
    width: 100%;
    max-width: 100%;
    min-height: 100vh;  /* 占满全屏 */
    align-items: flex-start;  /* 从顶部开始 */
  }
  
  /* 对话框占满屏幕水平空间 */
  .chat-panel {
    max-width: 100% !important;
    width: 100% !important;
    border-radius: 0;  /* 完全无圆角，贴合屏幕 */
    margin: 0;
    max-height: calc(100vh - 60px);  /* 减去导航栏高度 */
  }
  
  .chat-panel.has-messages {
    max-width: 100% !important;
    width: 100% !important;
    max-height: calc(100vh - 60px);
  }
  
  /* 消息区域优化 */
  .messages {
    height: 55vh;  /* 进一步增加高度 */
    min-height: 350px;
    padding: 12px;
  }
  
  .chat-panel.has-messages .messages {
    height: 65vh;  /* 有对话时进一步增加 */
    min-height: 400px;
  }
  
  .bubble {
    max-width: 85%;
    padding: 10px 14px;
    font-size: 14px;
  }
  
  /* 输入区域紧凑布局 */
  .input {
    padding: 12px;  /* 增加内边距 */
    background: transparent;
    backdrop-filter: none;
    border-top: none;
  }
  
  /* 工具按钮样式已删除 */
  
  /* 输入框区域 */
  .input-main {
    margin-bottom: 8px;
  }
  
  .input-container {
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;  /* 占满整个屏幕宽度 */
    max-width: none;  /* 移除最大宽度限制 */
    margin: 0;
    padding: 0 20px;  /* 左右留一些边距 */
  }
  
  /* 输入框占满宽度 */
  .input-main textarea {
    flex: 1;
    min-height: 40px;
    max-height: 80px;
    font-size: 16px;  /* 防止iOS自动缩放 */
    padding: 12px 56px 12px 20px;  /* 右侧留出发送按钮空间 */
    border-radius: 25px;
    background: rgba(255, 255, 255, 0.2);  /* 微信端更透明的白色背景 */
    border: 3px solid rgba(135, 206, 235, 0.8);  /* 加粗边框，更醒目 */
    backdrop-filter: blur(10px);
    box-shadow: 0 6px 25px rgba(135, 206, 235, 0.3);  /* 增强阴影 */
    color: #333;  /* 输入文字颜色 */
  }
  
  /* 占位符文字颜色 */
  .input-main textarea::placeholder {
    color: #333;  /* 占位符文字改为黑色 */
    opacity: 1;  /* 确保透明度为100% */
  }
  
  /* 透明发送按钮 */
  .send-btn-inside {
    position: absolute;
    right: 18px;
    top: 50%;
    transform: translateY(-50%);
    width: 34px;
    height: 34px;
    border-radius: 18px;
    border: 2px solid rgba(102, 126, 234, 0.6);
    background: rgba(255, 255, 255, 0.9);
    color: #4c5fe8;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    z-index: 1;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
  }
  
  .send-btn-inside:hover:not(:disabled) {
    transform: translateY(-50%) scale(1.08);
    color: #2f49e0;
    border-color: rgba(102, 126, 234, 0.8);
    box-shadow: 0 6px 18px rgba(102, 126, 234, 0.35);
  }
  
  .send-btn-inside:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: translateY(-50%);
    box-shadow: none;
  }
  
  /* 加载动画 */
  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* 底部功能按钮 - 三个按钮占满一排 */
  .input-bottom {
    display: flex;
    gap: 8px;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    width: 100%;
  }
  
  .bottom-btn {
    flex: 1;
    font-size: 11px;
    padding: 8px 6px;
    border-radius: 12px;
    background: rgba(173, 216, 230, 0.6);
    border: 1px solid rgba(135, 206, 235, 0.4);
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    text-align: center;
    min-height: 36px;
  }
  
  .bottom-btn svg {
    width: 12px;
    height: 12px;
    flex-shrink: 0;
  }
  
  .input-hint {
    width: 100%;
    font-size: 10px;
    color: #666;
    text-align: center;
    margin-top: 6px;
    white-space: nowrap;
  }
}

/* ==================== 小屏手机优化（<480px 微信等） ==================== */
@media (max-width: 480px) {
  .chat-main {
    padding: 0;  /* 完全无边距 */
    padding-top: 60px;  /* 给导航栏留空间 */
  }
  
  /* 对话框完全占满屏幕 */
  .chat-panel {
    border-radius: 0;  /* 完全无圆角 */
    max-height: calc(100vh - 60px);  /* 减去导航栏 */
  }
  
  .chat-panel.has-messages {
    max-height: calc(100vh - 60px);
  }
  
  /* 消息区域最大化 */
  .messages {
    height: 58vh;  /* 进一步增加高度 */
    min-height: 300px;
    padding: 10px;
  }
  
  .chat-panel.has-messages .messages {
    height: 68vh;  /* 有对话时占更多空间 */
    min-height: 350px;
  }
  
  /* 输入区域紧凑设计 */
  .input {
    padding: 10px;
    background: transparent !important;  /* 微信端强制透明 */
    backdrop-filter: none !important;
    border-top: none !important;
    z-index: 1 !important;  /* 确保不遮挡背景 */
  }
  
  /* 输入框优化 */
  .input-main {
    margin-bottom: 6px;
  }
  
  .input-container {
    max-width: none;
    width: 100%;
    padding: 0 15px;  /* 移动端稍微减少边距 */
  }
  
  .input-main textarea {
    padding: 10px 46px 10px 16px;  /* 右侧留出发送按钮空间 */
    font-size: 16px;  /* 微信推荐16px防止自动缩放 */
    min-height: 38px;
    max-height: 75px;
    border-radius: 20px;
    border: 2px solid rgba(135, 206, 235, 0.8);  /* 移动端也加粗边框 */
    background: rgba(255, 255, 255, 0.15) !important;  /* 微信端极透明背景 */
    box-shadow: 0 4px 20px rgba(135, 206, 235, 0.1) !important;  /* 减少阴影 */
    color: #333;  /* 移动端输入文字颜色 */
  }
  
  /* 移动端占位符文字颜色 */
  .input-main textarea::placeholder {
    color: #333;  /* 移动端占位符文字改为黑色 */
    opacity: 1;  /* 确保透明度为100% */
  }
  
  .send-btn-inside {
    width: 30px;
    height: 30px;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    border-radius: 16px;
    border: 2px solid rgba(102, 126, 234, 0.6);
    background: rgba(255, 255, 255, 0.9);
    color: #4c5fe8;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
  }
  
  .send-btn-inside svg {
    width: 14px;
    height: 14px;
  }
  
  /* 功能按钮优化 - 三个按钮占满一排 */
  .input-bottom {
    gap: 6px;
    margin-top: 6px;
    padding: 0 10px;
  }
  
  .bottom-btn {
    font-size: 10px;
    padding: 6px 4px;
    border-radius: 10px;
    min-height: 32px;
  }
  
  .bottom-btn svg {
    width: 10px;
    height: 10px;
  }
  
  .input-hint {
    font-size: 9px;
    opacity: 0.8;
    margin-top: 4px;
    padding: 0 10px;
  }
  
  /* 关闭按钮样式已删除 */
  
  /* 消息气泡优化 */
  .bubble {
    max-width: 82%;
    padding: 9px 12px;
    font-size: 14px;
    border-radius: 10px;
  }
}

/* ==================== 科技风AI开始对话卡片 ==================== */
.ai-start-card {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 320px;
  padding: 16px;
  z-index: 10;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.card-container {
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(139, 0, 255, 0.1) 100%);
  backdrop-filter: blur(15px);
  border-radius: var(--glass-radius);
  padding: 20px;
  text-align: center;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--glass-border);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.card-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.1;
  transition: left var(--transition-normal);
}

.ai-start-card:hover .card-container::before {
  left: 100%;
}

.ai-start-card:hover .card-container {
  transform: translateY(-4px);
  box-shadow: var(--hover-shadow);
  border-color: var(--primary-neon);
}

/* 科技风图标 */
.card-icon {
  margin: 0 auto 12px;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  border: 2px solid var(--glass-border);
  border-radius: 50%;
  background: rgba(0, 212, 255, 0.05);
}

.card-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 10px var(--primary-neon));
}

.ai-start-card:hover .card-icon {
  transform: scale(1.05) rotate(5deg);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
  border-color: var(--primary-neon);
}

/* 科技风文字 */
.card-text {
  margin-bottom: 16px;
}

.card-text h3 {
  color: var(--primary-neon);
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 6px 0;
  line-height: 1.3;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  letter-spacing: 1px;
}

.card-text p {
  color: var(--accent-cyan);
  font-size: 13px;
  margin: 0;
  line-height: 1.4;
  opacity: 0.9;
}

/* 科技风按钮 */
.start-button {
  background: transparent;
  color: var(--primary-neon);
  border: 2px solid var(--primary-neon);
  border-radius: var(--border-radius);
  padding: 10px 20px;
  font-weight: 600;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: all var(--transition-normal);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
  position: relative;
  overflow: hidden;
  letter-spacing: 1px;
}

.start-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.2;
  transition: left var(--transition-normal);
  z-index: -1;
}

.ai-start-card:hover .start-button::before {
  left: 100%;
}

.ai-start-card:hover .start-button {
  transform: translateY(-2px);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6);
  background: rgba(0, 212, 255, 0.1);
}

.button-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 0 5px var(--primary-neon));
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 768px) {
  .ai-start-card {
    padding: 12px;
    max-width: 300px;
  }
  
  .card-container {
    padding: 16px;
  }
  
  .card-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 10px;
  }
  
  .card-text h3 {
    font-size: 15px;
  }
  
  .card-text p {
    font-size: 12px;
  }
  
  .start-button {
    padding: 8px 16px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .ai-start-card {
    padding: 10px;
    max-width: 280px;
  }
  
  .card-container {
    padding: 14px;
  }
  
  .card-icon {
    width: 90px;
    height: 90px;
    margin-bottom: 8px;
  }
  
  .card-text h3 {
    font-size: 14px;
  }
  
  .card-text p {
    font-size: 11px;
  }
  
  .start-button {
    padding: 7px 14px;
    font-size: 11px;
  }
}
</style>

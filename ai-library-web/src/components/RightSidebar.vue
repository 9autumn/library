<template>
  <div class="right-sidebar" :class="{ collapsed: isCollapsed }">
    <!-- 展开/收起按钮 -->
    <button class="toggle-btn" @click="toggleSidebar" :title="isCollapsed ? '展开边栏' : '收起边栏'" style="width: 40px !important; height: 40px !important; padding: 0 !important; margin: 0 !important; box-sizing: border-box !important;">
      <svg v-if="isCollapsed" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M9 18l6-6-6-6"/>
      </svg>
      <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M15 18l-6-6 6-6"/>
      </svg>
    </button>


    <!-- 侧边栏内容 -->
    <div class="sidebar-content" v-show="!isCollapsed">
      <!-- 常见问题部分 -->
      <div class="section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
            <path d="M12 17h.01"/>
          </svg>
          常见问题
        </h3>
        <div class="tabs">
          <button 
            v-for="tab in faqTabs" 
            :key="tab.key"
            :class="['tab', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="faq-list">
          <button 
            v-for="(item, index) in currentFaqItems" 
            :key="index"
            class="faq-item"
            @click="selectFaq(item)"
          >
            <span class="faq-icon">?</span>
            <span class="faq-text">{{ item.question }}</span>
          </button>
        </div>
      </div>

      <!-- 馆内推荐部分 -->
      <div class="section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          馆内推荐
        </h3>
        <div class="recommendations">
          <button 
            v-for="(item, index) in recommendations" 
            :key="index"
            class="recommendation-item"
            @click="selectRecommendation(item)"
          >
            <div class="recommendation-icon" :style="{ backgroundColor: item.color }">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path :d="item.icon"/>
              </svg>
            </div>
            <div class="recommendation-content">
              <div class="recommendation-title">{{ item.title }}</div>
              <div class="recommendation-desc">{{ item.description }}</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const isCollapsed = ref(true) // 默认关闭
const activeTab = ref('card')

const faqTabs = [
  { key: 'card', label: '办证退证' },
  { key: 'network', label: '网络服务' },
  { key: 'guide', label: '入馆须知' }
]

const faqData = {
  card: [
    { question: '如何办理借书证？', answer: '请携带身份证到一楼服务台办理借书证，需要缴纳押金100元。' },
    { question: '借书证丢失怎么办？', answer: '请及时到服务台挂失，补办需要携带身份证和10元工本费。' },
    { question: '如何退证？', answer: '携带借书证和身份证到服务台办理退证手续，押金将全额退还。' },
    { question: '借书证有效期多长？', answer: '借书证有效期为3年，到期后可免费续期。' }
  ],
  network: [
    { question: '图书馆WiFi密码是多少？', answer: '图书馆WiFi密码为：library2024，连接后需要手机验证。' },
    { question: '如何访问数字资源？', answer: '在图书馆内使用电脑或手机连接WiFi，访问图书馆官网的数字资源栏目。' },
    { question: '电子阅览室如何预约？', answer: '可通过图书馆官网或微信公众号预约电子阅览室座位。' },
    { question: '如何下载电子书？', answer: '使用图书馆提供的数字资源平台，注册账号后即可下载电子书。' }
  ],
  guide: [
    { question: '图书馆开放时间？', answer: '周一至周日：8:00-22:00，节假日正常开放。' },
    { question: '可以带包进入吗？', answer: '可以带包进入，但需要在入口处寄存大件物品。' },
    { question: '图书馆有停车位吗？', answer: '图书馆提供免费停车位，位于地下停车场。' },
    { question: '如何保持安静？', answer: '请将手机调至静音，轻声交谈，避免影响其他读者。' }
  ]
}

const recommendations = [
  {
    title: 'AI荐书',
    description: '智能推荐图书',
    icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
    color: '#ff6b6b'
  },
  {
    title: 'AI阅读',
    description: '智能阅读助手',
    icon: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z',
    color: '#4ecdc4'
  },
  {
    title: 'AI解书',
    description: '智能图书解读',
    icon: 'M9 12l2 2 4-4M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    color: '#45b7d1'
  },
  {
    title: 'AI学术问答',
    description: '学术问题解答',
    icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    color: '#96ceb4'
  },
  {
    title: '留言板',
    description: '读者意见反馈',
    icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
    color: '#feca57'
  },
  {
    title: '人工服务',
    description: '在线人工客服',
    icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    color: '#ff9ff3'
  }
]

const currentFaqItems = computed(() => {
  return faqData[activeTab.value as keyof typeof faqData] || []
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  // 通知父组件侧边栏状态变化
  emit('sidebar-toggle', !isCollapsed.value)
}

const selectFaq = (item: any) => {
  emit('faq-selected', item)
}

const selectRecommendation = (item: any) => {
  if (item.title === 'AI荐书') {
    // 跳转到AI荐书页面
    window.location.href = '/recommendation'
  } else {
    emit('recommendation-selected', item)
  }
}

const emit = defineEmits<{
  'faq-selected': [item: any]
  'recommendation-selected': [item: any]
  'sidebar-toggle': [isOpen: boolean]
}>()
</script>

<style scoped>
.right-sidebar {
  position: fixed;
  right: 0;
  top: 0;
  height: 100vh;
  width: 320px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border-left: 1px solid var(--glass-border);
  transition: all var(--transition-normal);
  z-index: 1002;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: -2px 0 20px rgba(0, 212, 255, 0.2);
  /* 科技风边框效果 */
  position: relative;
}

.right-sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.05;
  pointer-events: none;
}

.right-sidebar.collapsed {
  width: 60px;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
}

button.toggle-btn,
.toggle-btn {
  position: absolute !important;
  top: 16px !important;
  right: 16px !important;
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  min-height: 40px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 50% !important;
  background: var(--glass-bg) !important;
  border: 2px solid var(--primary-neon) !important;
  color: var(--primary-neon) !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  backdrop-filter: blur(15px) !important;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
  z-index: 10 !important;
  transition: all var(--transition-normal) !important;
  box-sizing: border-box !important;
}

.right-sidebar.collapsed .toggle-btn {
  right: 10px;
}

.toggle-btn:hover {
  background: rgba(0, 212, 255, 0.2) !important;
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6) !important;
  transform: translateY(-2px) scale(1.1) !important;
}

.toggle-btn:active {
  transform: translateY(-1px) scale(0.95) !important;
}

.toggle-btn svg {
  width: 18px;
  height: 18px;
  stroke-width: 2;
  filter: drop-shadow(0 0 5px var(--primary-neon));
}


.sidebar-content {
  padding: 80px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
}


@media (max-width: 768px) {
  button.toggle-btn,
  .toggle-btn {
    top: 3px !important;
    right: 3px !important;
    width: 20px !important;  /* 移动端按钮宽度 */
    height: 22px !important;  /* 移动端按钮高度 */
    min-width: 20px !important;  /* 覆盖全局移动端min-width */
    min-height: 22px !important;  /* 覆盖全局移动端min-height */
    padding: 0 !important;  /* 强制移除内边距，覆盖全局padding */
    margin: 0 !important;  /* 强制移除外边距 */
    border-radius: 1px !important;  /* 移动端小圆角 */
    box-sizing: border-box !important;  /* 确保尺寸计算包含边框 */
  }
  
  .toggle-btn svg {
    width: 8px;  /* 移动端图标尺寸，与桌面端保持一致 */
    height: 8px;
  }
  
  .sidebar-content {
    padding-top: 30px;  /* 为按钮留出空间 */
  }
}

.section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-neon);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 30px;
  height: 2px;
  background: var(--neon-gradient);
}

.tabs {
  display: flex;
  gap: 4px;
  background: rgba(0, 212, 255, 0.1);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
}

.tab {
  flex: 1;
  padding: 8px 12px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  color: var(--accent-cyan);
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.tab::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.2;
  transition: left var(--transition-fast);
}

.tab:hover::before {
  left: 100%;
}

.tab.active {
  background: var(--primary-neon);
  color: var(--dark-bg);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.faq-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border: none;
  background: rgba(0, 212, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  width: 100%;
  border: 1px solid transparent;
}

.faq-item:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: var(--glass-border);
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
  transform: translateX(-2px);
}

.faq-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-neon);
  color: var(--dark-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.faq-text {
  font-size: 13px;
  line-height: 1.4;
  color: var(--accent-cyan);
}

.recommendations {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.recommendation-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 12px;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: rgba(0, 212, 255, 0.05);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.recommendation-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.1;
  transition: left var(--transition-fast);
}

.recommendation-item:hover::before {
  left: 100%;
}

.recommendation-item:hover {
  border-color: var(--primary-neon);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
  transform: translateY(-2px);
}

.recommendation-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}

.recommendation-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.recommendation-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-neon);
}

.recommendation-desc {
  font-size: 10px;
  color: var(--accent-cyan);
  line-height: 1.3;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .right-sidebar {
    width: 280px;
  }
  
  .recommendations {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .right-sidebar {
    width: 100%;
    transform: translateX(100%);
    top: 50px; /* 适配移动端导航栏高度，减少间距 */
    height: calc(100vh - 50px);
  }
  
  .right-sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .right-sidebar.collapsed {
    width: 0;
    transform: translateX(100%);
    background: transparent;
    border: none;
    box-shadow: none;
    overflow: visible;
  }
  
  .right-sidebar {
    background: linear-gradient(135deg, rgba(173, 216, 230, 0.15) 0%, rgba(135, 206, 235, 0.12) 100%);
  }
  
  .right-sidebar.collapsed .sidebar-content {
    display: none;
  }
  
  
  
  .sidebar-content {
    padding: 20px 16px;
    gap: 20px;
  }
  
  .recommendations {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .recommendation-item {
    padding: 16px 12px;
  }
  
  .recommendation-title {
    font-size: 13px;
  }
  
  .recommendation-desc {
    font-size: 11px;
  }
}
</style>

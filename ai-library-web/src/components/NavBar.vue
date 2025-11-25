<template>
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
      <!-- 科技风状态指示器 -->
      <div class="status-indicator">
        <div class="status-dot"></div>
        <span class="status-text">AI系统在线</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--card-shadow);
  position: sticky;
  top: 0;
  z-index: 1001;
  /* 科技风动画背景 */
  position: relative;
  overflow: hidden;
}

.nav::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.1;
  animation: navScan 3s linear infinite;
}

@keyframes navScan {
  0% { left: -100%; }
  100% { left: 100%; }
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  position: relative;
  z-index: 2;
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
  /* 科技风logo效果 */
  position: relative;
}

.logo {
  width: 48px;
  height: 48px;
  background: rgba(0, 212, 255, 0.1);
  border: 2px solid var(--primary-neon);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  transition: all var(--transition-normal);
  animation: logoRotate 10s linear infinite;
}

@keyframes logoRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.logo:hover {
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
  transform: scale(1.1);
}

.logo img {
  width: 28px;
  height: 28px;
  object-fit: contain;
  filter: drop-shadow(0 0 5px var(--primary-neon));
}

.brand-text h1 {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-neon);
  margin: 0;
  line-height: 1.2;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  letter-spacing: 1px;
}

.brand-text p {
  font-size: 12px;
  color: var(--accent-cyan);
  margin: 0;
  font-weight: 500;
  opacity: 0.8;
}

/* 科技风状态指示器 */
.status-indicator {
  position: absolute;
  top: 50%;
  right: 24px;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-neon);
  box-shadow: 0 0 10px var(--primary-neon);
  animation: statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

.status-text {
  font-size: 12px;
  color: var(--accent-cyan);
  font-weight: 500;
}

/* 导航按钮样式已删除 */

@media (max-width: 1024px) {
  .nav-container {
    padding: 10px 16px;
  }
  
  .brand-text h1 {
    font-size: 18px;
  }
  
  .status-indicator {
    right: 16px;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 8px 12px;
  }
  
  .logo {
    width: 40px;
    height: 40px;
  }
  
  .logo img {
    width: 24px;
    height: 24px;
  }
  
  .brand-text h1 {
    font-size: 16px;
  }
  
  .brand-text p {
    font-size: 10px;
  }
  
  .status-text {
    display: none; /* 移动端隐藏状态文字 */
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 6px 8px;
  }
  
  .brand-text h1 {
    font-size: 14px;
  }
  
  .brand-text p {
    font-size: 9px;
  }
}
</style>



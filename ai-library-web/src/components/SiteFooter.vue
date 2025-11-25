<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-brand">
        <div class="brand-info">
          <h3>青山区图书馆</h3>
          <p>Qingshan District Library</p>
          <p class="motto">智慧阅读 · 文化传承</p>
        </div>
      </div>
      <div class="footer-links">
        <div class="link-group">
          <h4>服务信息</h4>
          <a href="javascript:void(0)">开放时间</a>
          <a href="javascript:void(0)">交通指引</a>
          <a href="javascript:void(0)">联系我们</a>
        </div>
        <div class="link-group">
          <h4>数字服务</h4>
          <a href="javascript:void(0)">在线检索</a>
          <a href="javascript:void(0)">电子资源</a>
          <a href="javascript:void(0)">移动服务</a>
        </div>
        <div class="link-group">
          <h4>读者服务</h4>
          <a href="javascript:void(0)">办证指南</a>
          <a href="javascript:void(0)">借阅规则</a>
          <a href="javascript:void(0)">活动预告</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2024 青山区图书馆 版权所有 | 地址：武汉市青山区 | 电话：027-12345678</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #E6F5FF;
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(59, 130, 246, 0.1);
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px 20px;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 40px;
  align-items: start;
  margin-left: 300px;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.brand-info h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-blue);
  margin: 0 0 8px 0;
}

.brand-info p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.motto {
  font-weight: 600;
  color: var(--secondary-blue) !important;
  font-size: 16px !important;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.link-group h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-blue);
  margin: 0 0 16px 0;
}

.link-group a {
  display: block;
  color: #6b7280;
  text-decoration: none;
  padding: 4px 0;
  font-size: 14px;
  transition: color 0.2s ease;
}

.link-group a:hover {
  color: var(--secondary-blue);
}

.footer-bottom {
  border-top: 1px solid rgba(59, 130, 246, 0.1);
  padding: 16px 24px;
  text-align: center;
  background: rgba(248, 250, 252, 0.5);
}

.footer-bottom p {
  margin: 0;
  color: #9ca3af;
  font-size: 12px;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px 16px 16px;
    margin-left: 0;
  }
  
  .footer-links {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
  
  .link-group {
    text-align: center;
  }
  
  .link-group h4 {
    font-size: 14px;
    margin-bottom: 8px;
  }
  
  .link-group a {
    font-size: 12px;
    padding: 2px 0;
  }
  
  .footer-bottom {
    padding: 12px 16px;
  }
  
  .footer-bottom p {
    font-size: 11px;
  }
}
</style>



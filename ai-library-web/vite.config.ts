import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 通过环境变量控制 Dify 代理目标，默认本地 127.0.0.1:8089
const DIFY_TARGET = process.env.VITE_DIFY_TARGET || 'http://124.71.97.68'
const DIFY_BASE_PATH = process.env.VITE_DIFY_BASE_PATH || '/dify'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5199,
    strictPort: true,
    // 添加允许的域名，解决 ngrok 访问问题
    allowedHosts: ['.ngrok-free.app'], // 允许所有以 .ngrok-free.app 结尾的子域名
    // 微信浏览器缓存控制
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
      // 微信浏览器特殊处理
      'X-Frame-Options': 'SAMEORIGIN',
      'X-Content-Type-Options': 'nosniff'
    },
    proxy: {
      [DIFY_BASE_PATH]: {
        target: DIFY_TARGET,
        changeOrigin: true,
        rewrite: (p) => p.replace(new RegExp(`^${DIFY_BASE_PATH}`), '')
      }
    }
  },
  // 构建配置
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].[hash].js`,
        chunkFileNames: `assets/[name].[hash].js`,
        assetFileNames: `assets/[name].[hash].[ext]`,
        // 手动分包优化
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router'],
          'markdown': ['marked'],
        }
      }
    },
    // 压缩优化
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // 生产环境移除 console
        drop_debugger: true
      }
    },
    // chunk 大小警告限制
    chunkSizeWarningLimit: 1000
  },
  // 优化配置
  optimizeDeps: {
    include: ['vue', 'vue-router', 'marked']
  },
  define: {
    __VUE_PROD_DEVTOOLS__: false
  }
})



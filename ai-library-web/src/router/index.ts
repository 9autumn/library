import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { 
    path: '/', 
    name: 'AIChat', 
    component: () => import('../pages/AIChat.vue')
  },
  { 
    path: '/chat', 
    name: 'Chat', 
    component: () => import('../pages/AIChat.vue')
  },
  { 
    path: '/recommendation', 
    name: 'AIRecommendation', 
    component: () => import('../pages/AIRecommendation.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router



<template>
  <div id="app-root">
    <NavBar />
    <main class="main-content">
      <router-view />
    </main>
    <SiteFooter v-if="showFooter" />
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const SiteFooter = defineAsyncComponent(() => import('./components/SiteFooter.vue'))

const route = useRoute()
const showFooter = computed(() => {
  const hiddenRoutes = ['AIChat', 'Chat', 'AIRecommendation']
  const currentName = route.name ? String(route.name) : ''
  return !hiddenRoutes.includes(currentName)
})
</script>

<style>
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.main-content {
  flex: 1;
  position: relative;
}
</style>

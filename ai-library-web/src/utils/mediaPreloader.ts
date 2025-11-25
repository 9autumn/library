// 媒体资源预加载管理器
interface PreloadItem {
  id: number
  title: string
  videoUrl: string
  audioUrl: string
  quoteAudioUrl: string
  audioObjectUrl?: string
  quoteAudioObjectUrl?: string
  loaded: boolean
  videoReady: boolean
  audioReady: boolean
  quoteAudioReady: boolean
  videoPrefetchedBytes?: number
}

const MEDIA_CACHE_NAME = 'ai-library-media-v1'
const VIDEO_PREFETCH_BYTES = 2 * 1024 * 1024 // 2MB 头部预取

class MediaPreloader {
  private items: Map<number, PreloadItem> = new Map()
  private preloadQueue: number[] = []
  private isPreloading = false
  private maxConcurrent = 2 // 最多同时预加载2个视频

  // 注册需要预加载的书籍
  register(books: Array<{ id: number; title: string; videoUrl: string; audioUrl: string; quoteAudioUrl: string }>) {
    books.forEach(book => {
      if (!this.items.has(book.id)) {
        this.items.set(book.id, {
          ...book,
          loaded: false,
          videoReady: false,
          audioReady: false,
          quoteAudioReady: false
        })
        this.preloadQueue.push(book.id)
      }
    })
  }

  // 开始预加载（渐进式，不阻塞UI）
  async startPreload() {
    if (this.isPreloading) return
    this.isPreloading = true

    // 分批预加载，避免阻塞
    while (this.preloadQueue.length > 0) {
      const batch = this.preloadQueue.splice(0, this.maxConcurrent)
      await Promise.all(batch.map(id => this.preloadItem(id)))
      
      // 每批之间延迟，避免阻塞UI
      await this.delay(500)
    }

    this.isPreloading = false
  }

  // 预加载单个项目
  private async preloadItem(id: number): Promise<void> {
    const item = this.items.get(id)
    if (!item || item.loaded) return

    try {
      // 1. 仅预取视频头部，提升首包
      await this.prefetchVideoHead(item)
      item.videoReady = true

      // 2. 预加载名言音频
      if (item.quoteAudioUrl && item.quoteAudioUrl.trim() !== '') {
        const quoteResponse = await this.fetchAndCache(item.quoteAudioUrl)
        if (quoteResponse) {
          const quoteBlob = await quoteResponse.blob()
          item.quoteAudioObjectUrl = URL.createObjectURL(quoteBlob)
          item.quoteAudioReady = true
        }
      } else {
        item.quoteAudioReady = true
      }

      // 3. 预加载完整音频
      if (item.audioUrl && item.audioUrl.trim() !== '') {
        const audioResponse = await this.fetchAndCache(item.audioUrl)
        if (audioResponse) {
          const audioBlob = await audioResponse.blob()
          item.audioObjectUrl = URL.createObjectURL(audioBlob)
          item.audioReady = true
        }
      } else {
        item.audioReady = true
      }

      item.loaded = item.videoReady && item.quoteAudioReady && item.audioReady
    } catch (error) {
      // 静默失败
    }
  }

  // 获取预加载的媒体元素（如果已预加载）
  getPreloadedMedia(id: number) {
    const item = this.items.get(id)
    if (!item || !item.loaded) return null

    return {
      videoUrl: undefined,
      audioUrl: item.audioObjectUrl,
      quoteAudioUrl: item.quoteAudioObjectUrl,
      ready: item.videoReady && (item.quoteAudioReady || !item.quoteAudioUrl) && (item.audioReady || !item.audioUrl)
    }
  }

  // 检查是否已预加载
  isLoaded(id: number): boolean {
    const item = this.items.get(id)
    return item?.loaded || false
  }

  // 获取预加载进度
  getProgress(): { loaded: number; total: number; percentage: number } {
    const total = this.items.size
    const loaded = Array.from(this.items.values()).filter(item => item.loaded).length
    return {
      loaded,
      total,
      percentage: total > 0 ? Math.round((loaded / total) * 100) : 0
    }
  }

  // 清理资源
  cleanup(id?: number) {
    if (id) {
      const item = this.items.get(id)
      if (item?.audioObjectUrl) {
        URL.revokeObjectURL(item.audioObjectUrl)
      }
      if (item?.quoteAudioObjectUrl) {
        URL.revokeObjectURL(item.quoteAudioObjectUrl)
      }
      this.items.delete(id)
    } else {
      this.items.forEach(item => {
        if (item.audioObjectUrl) {
          URL.revokeObjectURL(item.audioObjectUrl)
        }
        if (item.quoteAudioObjectUrl) {
          URL.revokeObjectURL(item.quoteAudioObjectUrl)
        }
      })
      this.items.clear()
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  private async fetchAndCache(resourceUrl: string): Promise<Response | null> {
    try {
      const request = new Request(resourceUrl, { method: 'GET' })

      if ('caches' in window) {
        const cache = await caches.open(MEDIA_CACHE_NAME)
        const cached = await cache.match(request, { ignoreSearch: false })
        if (cached) {
          return cached.clone()
        }

        const response = await fetch(request)
        if (response.ok && response.status === 200) {
          await cache.put(request, response.clone())
          return response
        }
        return response.ok ? response : null
      }

      const response = await fetch(request)
      return response.ok ? response : null
    } catch (error) {
      return null
    }
  }

  private async prefetchVideoHead(item: PreloadItem) {
    const controller = new AbortController()
    const headers = new Headers()
    headers.set('Range', `bytes=0-${VIDEO_PREFETCH_BYTES - 1}`)

    try {
      const response = await fetch(item.videoUrl, {
        headers,
        signal: controller.signal,
        cache: 'no-store'
      })

      if (!response.ok || !response.body) {
        controller.abort()
        return
      }

      const reader = response.body.getReader()
      let received = 0

      while (received < VIDEO_PREFETCH_BYTES) {
        const { done, value } = await reader.read()
        if (done || !value) break
        received += value.byteLength
        if (received >= VIDEO_PREFETCH_BYTES) {
          controller.abort()
          break
        }
      }

      item.videoPrefetchedBytes = received
      reader.releaseLock()
    } catch (error) {
      controller.abort()
    }
  }
}

// 单例模式
export const mediaPreloader = new MediaPreloader()


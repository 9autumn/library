const MEDIA_CACHE = 'ai-library-media-v1'

self.addEventListener('install', event => {
  self.skipWaiting()
})

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== MEDIA_CACHE)
          .map(name => caches.delete(name))
      )
    }).then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', event => {
  const { request } = event
  if (request.method !== 'GET') {
    return
  }

  const url = new URL(request.url)

  if (request.headers.has('range')) {
    return
  }

  const isSameOrigin = url.origin === self.location.origin
  const isMediaRequest = url.pathname.startsWith('/videos/') || url.pathname.startsWith('/audio/')

  if (isSameOrigin && isMediaRequest) {
    event.respondWith(cacheFirst(request))
  }
})

async function cacheFirst(request) {
  const cache = await caches.open(MEDIA_CACHE)
  const cached = await cache.match(request)

  if (cached) {
    return cached
  }

  const response = await fetch(request)
  if (response && response.ok && response.status === 200) {
    cache.put(request, response.clone())
  }
  return response
}



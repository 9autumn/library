// 直接配置您的Dify API地址和密钥
const basePath = 'http://124.71.97.68/v1'
const appKey = 'app-ka994zy9N68cJgaEznXHqbfL'

function getHeaders() {
  if (!appKey) {
    throw new Error('缺少 Dify API Key')
  }
  
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${appKey}`
  }
}

export type StreamChunk = {
  event: string
  data: any
}

// 流式：使用 fetch + ReadableStream 解析 Dify SSE
export async function streamChatMessage(query: string, onMessage: (text: string) => void): Promise<void> {
  const url = `${basePath}/chat-messages`
  
  const res = await fetch(url, {
    method: 'POST',
    headers: getHeaders(),
    mode: 'cors',
    credentials: 'omit',
    body: JSON.stringify({
      inputs: {},
      query,
      response_mode: 'streaming',
      user: 'web-user'
    })
  })
  if (!res.ok || !res.body) {
    const text = await res.text().catch(() => '')
    throw new Error(`Dify 流式接口错误: ${res.status} ${text}`)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    // SSE: 按行解析，以\n\n为界
    const parts = buffer.split('\n\n')
    buffer = parts.pop() || ''
    for (const part of parts) {
      const lines = part.split('\n')
      let event = 'message'
      let data = ''
      for (const line of lines) {
        if (line.startsWith('event:')) event = line.slice(6).trim()
        if (line.startsWith('data:')) data += line.slice(5).trim()
      }
      if (event === 'message' || event === 'answer') {
        try {
          const json = JSON.parse(data)
          const text = json.answer || json.output || ''
          if (text) onMessage(text)
        } catch {
          // 某些实现 data 直接是文本
          if (data) onMessage(data)
        }
      }
    }
  }
}



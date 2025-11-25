import { marked } from 'marked'

// 配置 marked 选项
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持 GitHub Flavored Markdown
})

// 导出渲染函数
export function renderMarkdown(text: string): string {
  if (!text) return ''
  
  try {
    const result = marked(text)
    return typeof result === 'string' ? result : text
  } catch (error) {
    console.warn('Markdown rendering error:', error)
    return text // 如果渲染失败，返回原始文本
  }
}

// 导出清理函数（如果需要）
export function stripMarkdown(text: string): string {
  if (!text) return ''
  
  // 简单的 markdown 符号清理
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1') // 粗体
    .replace(/\*(.*?)\*/g, '$1') // 斜体
    .replace(/`(.*?)`/g, '$1') // 行内代码
    .replace(/```[\s\S]*?```/g, '') // 代码块
    .replace(/#{1,6}\s+/g, '') // 标题
    .replace(/^\s*[-*+]\s+/gm, '') // 列表
    .replace(/^\s*\d+\.\s+/gm, '') // 有序列表
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // 链接
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '$1') // 图片
    .replace(/^\s*>\s*/gm, '') // 引用
    .replace(/^\s*\|.*\|.*$/gm, '') // 表格
    .replace(/^---+$/gm, '') // 分隔线
    .trim()
}

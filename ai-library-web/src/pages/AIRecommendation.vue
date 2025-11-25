<template>
  <div class="ai-recommendation">
    <!-- 数字人背景 -->
    <div class="digital-human-bg">
      <video 
        ref="backgroundVideo" 
        class="background-video"
        autoplay 
        muted
        loop
        playsinline
        @loadeddata="onVideoLoaded"
      >
        <source src="/videos/background.mp4" type="video/mp4">
      </video>
      <div class="video-overlay"></div>
    </div>

    <!-- 主要内容 -->
    <div class="content-container">
      <!-- 页面标题 -->
      <div class="page-header">
        <!-- 返回按钮 -->
        <button class="back-button" @click="goBack" title="返回">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        
        <h1 class="page-title">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          AI智能荐书
        </h1>
        <p class="page-subtitle">为您推荐经典文学作品，开启智慧阅读之旅</p>
      </div>

      <!-- 搜索栏 -->
      <div class="search-section">
        <div class="search-container">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="输入您感兴趣的书籍类型或主题..."
            class="search-input"
            @keyup.enter="handleSearch"
          >
          <button class="search-btn" @click="handleSearch">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 书籍推荐网格 -->
      <div class="books-grid">
        <div 
          v-for="book in filteredBooks" 
          :key="book.id"
          class="book-card"
          @click="showBookDetail(book)"
        >
          <div class="book-cover">
            <video 
              :ref="`video-${book.id}`"
              :data-book-id="book.id"
              class="book-video-poster"
              muted
              preload="metadata"
              playsinline
              webkit-playsinline
              x5-playsinline
              @loadeddata="setVideoPoster(book.id)"
            >
              <source :src="getVideoUrl(book)" type="video/mp4">
            </video>
            <div class="play-overlay">
              <div class="play-button">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
              </div>
            </div>
          </div>
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
            <div class="book-tags">
              <span v-for="tag in book.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 书籍详情弹窗 -->
    <div v-if="selectedBook" class="book-detail-modal" @click="closeBookDetail">
      <div class="detail-container" @click.stop>
        <button class="close-detail-btn" @click="closeBookDetail">×</button>
        
        <div class="detail-content">
          <!-- 左侧：视频播放区域 -->
          <div class="detail-left">
            <div class="detail-video-wrapper">
              <video 
                ref="detailVideoPlayer"
                class="detail-video"
                :src="getVideoUrl(selectedBook)"
                controls
                preload="auto"
                @playing="onDetailVideoPlaying"
                @pause="onDetailVideoPause"
                @ended="onDetailVideoEnded"
                @volumechange="onDetailVideoVolumeChange"
              >
              </video>
              <!-- 名言音频 -->
              <audio 
                v-if="selectedBook.quoteAudioUrl && selectedBook.quoteAudioUrl.trim() !== ''"
                ref="detailQuoteAudioPlayer"
                :src="selectedBook.quoteAudioUrl"
                preload="auto"
                style="display: none;"
              >
              </audio>
              
              <!-- 完整音频 -->
              <audio 
                v-if="selectedBook.audioUrl && selectedBook.audioUrl.trim() !== ''"
                ref="detailAudioPlayer"
                :src="selectedBook.audioUrl"
                preload="auto"
                style="display: none;"
              >
              </audio>
            </div>
          </div>
          
          <!-- 右侧：书籍信息 -->
          <div class="detail-right">
            <h2 class="detail-title">{{ selectedBook.title }}</h2>
            <p class="detail-author">作者：{{ selectedBook.author }}</p>
            
            <div class="detail-tags">
              <span v-for="tag in selectedBook.tags" :key="tag" class="detail-tag">{{ tag }}</span>
            </div>
            
            <!-- 经典名言 -->
            <div v-if="selectedBook.quote" class="quote-section">
              <div class="quote-icon">❝</div>
              <p class="quote-text">{{ selectedBook.quote }}</p>
            </div>
            
            <div class="detail-section">
              <h3 class="section-heading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
                内容简介
              </h3>
              <p class="section-text">{{ selectedBook.description }}</p>
            </div>
            
            <div class="detail-section">
              <h3 class="section-heading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                AI 推荐理由
              </h3>
              <p class="section-text recommendation-highlight">{{ selectedBook.recommendation }}</p>
            </div>
            
            <div class="detail-actions">
              <button class="action-btn close-btn-secondary" @click="closeBookDetail">
                关闭
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预加载进度提示 -->
    <!-- 智能预加载提示已移除 -->

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { mediaPreloader } from '../utils/mediaPreloader'

// 类型定义
const isWechatBrowser = /micromessenger/i.test(navigator.userAgent)

interface Book {
  id: number
  title: string
  author: string
  tags: string[]
  description: string
  recommendation: string
  quote: string
  audioUrl: string
  quoteAudioUrl: string
  videoUrl: string
  mobileVideoUrl?: string
}

interface AudioItem extends Book {
  audio?: HTMLAudioElement
  quoteAudio?: HTMLAudioElement
  video?: HTMLVideoElement
}

// 响应式数据
const searchQuery = ref('')
const currentAudio = ref<AudioItem | null>(null)
const isAudioPlaying = ref(false)
const backgroundVideo = ref<HTMLVideoElement | null>(null)
const selectedBook = ref<Book | null>(null)
const detailVideoPlayer = ref<HTMLVideoElement | null>(null)
const detailAudioPlayer = ref<HTMLAudioElement | null>(null)
const detailQuoteAudioPlayer = ref<HTMLAudioElement | null>(null)
const videoPosterSet = ref<Set<number>>(new Set())
// 书籍数据
const getVideoUrl = (book?: Book | null) => {
  if (!book) return ''
  const mobileUrl = book.mobileVideoUrl?.trim()
  if (isWechatBrowser && mobileUrl) {
    return mobileUrl
  }
  return book.videoUrl
}

const books = ref<Book[]>([
  {
    id: 1,
    title: '堂吉诃德',
    author: '塞万提斯',
    tags: ['经典', '小说', '冒险'],
    description: '西班牙文学巨匠塞万提斯的传世之作，讲述了一位执着于骑士梦想的乡绅堂吉诃德和他的侍从桑丘·潘萨的冒险故事。这部作品以幽默讽刺的笔触，深刻揭示了理想与现实的矛盾。',
    recommendation: '这是世界文学史上最伟大的小说之一，被誉为"第一部现代小说"。书中堂吉诃德对理想的执着追求，展现了人类精神中最纯粹的一面。适合所有追寻梦想、思考人生意义的读者。',
    quote: '我知道我是谁，但我更知道我想成为谁。',
    audioUrl: '/audio/堂吉诃德.MP3',
    quoteAudioUrl: '/audio/堂吉诃德，我知道我是谁，但我更知道我想成为谁。.mp3',
    videoUrl: '/videos/堂吉诃德.mp4',
    mobileVideoUrl: '/videos/堂吉诃德.mp4'
  },
  {
    id: 2,
    title: '小王子',
    author: '安托万·德·圣埃克苏佩里',
    tags: ['童话', '哲学', '成长'],
    description: '一部写给大人的童话。小王子从他的星球出发，游历了多个星球，最后来到地球。在旅途中，他遇到了各种奇特的人物，每个人都代表着成人世界的某种缺陷。',
    recommendation: '这本书用最纯真的语言讲述最深刻的道理。"真正重要的东西，用眼睛是看不见的"——这句话温暖了无数人的心。适合所有年龄段的读者，尤其是需要找回纯真与爱的成年人。',
    quote: '真正重要的东西，用眼睛是看不见的，要用心去寻找。',
    audioUrl: '/audio/小王子.MP3',
    quoteAudioUrl: '/audio/小王子，真正重要的东西，用眼睛是看不见的，要用心去寻找。.mp3',
    videoUrl: '/videos/小王子.mp4',
    mobileVideoUrl: '/videos/小王子.mp4'
  },
  {
    id: 3,
    title: '山海经',
    author: '古代典籍',
    tags: ['神话', '地理', '古代'],
    description: '中国先秦重要古籍，是一部富于神话传说的最古老的奇书。全书记载了约40个邦国、550座山、300条水道、100多个历史人物以及400多个神怪异兽。',
    recommendation: '这是了解中国古代神话体系的必读经典。书中天马行空的想象力、丰富的神话人物和异兽描写，展现了古人对世界的认知。适合对中国古代文化、神话传说感兴趣的读者。',
    quote: '刑天舞干戚，猛志固常在',
    audioUrl: '/audio/山海经.MP3',
    quoteAudioUrl: '/audio/山海经，刑天舞干戚，猛志固常在.mp3',
    videoUrl: '/videos/山海经.mp4',
    mobileVideoUrl: '/videos/山海经.mp4'
  },
  {
    id: 4,
    title: '悲惨世界',
    author: '维克多·雨果',
    tags: ['经典', '社会', '人性'],
    description: '19世纪法国现实主义文学巨著，以冉阿让的命运为主线，展现了法国大革命时期广阔的社会画卷。通过对社会底层人物的描写，深刻揭露了资本主义社会的黑暗。',
    recommendation: '这是一部充满人道主义精神的伟大作品。冉阿让从罪犯到圣徒的转变，诠释了救赎与爱的力量。适合关注社会问题、思考人性善恶的读者。雨果用文字为弱者发声，令人动容。',
    quote: '释放无限光明的是人心，制造无边黑暗的，也是人心',
    audioUrl: '/audio/悲惨世界.MP3',
    quoteAudioUrl: '/audio/悲惨世界，释放无限光明的是人心，制造无边黑暗的，也是人心.mp3',
    videoUrl: '/videos/悲惨世界.mp4',
    mobileVideoUrl: '/videos/悲惨世界.mp4'
  },
  {
    id: 5,
    title: '战争与和平',
    author: '列夫·托尔斯泰',
    tags: ['历史', '战争', '哲学'],
    description: '俄国文学巨匠托尔斯泰的代表作，以1805年至1820年的俄国社会为背景，通过四大贵族家庭的命运变迁，展现了俄法战争的宏大历史画卷。',
    recommendation: '这是一部百科全书式的长篇巨著，被誉为"世界上最伟大的小说"。托尔斯泰以细腻的笔触描绘了战争的残酷与和平的珍贵，探讨了历史、命运、自由等重大命题。适合喜欢历史、哲学的成熟读者。',
    quote: '历史不是由个人推动的，而是无数微小力量的总和。',
    audioUrl: '/audio/战争与和平.MP3',
    quoteAudioUrl: '/audio/战争与和平，历史不是由个人推动的，而是无数微小力量的总和。.mp3',
    videoUrl: '/videos/战争与和平.mp4',
    mobileVideoUrl: '/videos/战争与和平.mp4'
  },
  {
    id: 6,
    title: '水浒传',
    author: '施耐庵',
    tags: ['古典', '英雄', '传奇'],
    description: '中国四大名著之一，描写了北宋末年以宋江为首的108位好汉聚义梁山的故事。全书塑造了众多个性鲜明的英雄形象，展现了"替天行道"的侠义精神。',
    recommendation: '这是一部充满豪情的英雄史诗。武松打虎、鲁智深倒拔垂杨柳、林冲风雪山神庙等经典情节脍炙人口。适合喜欢武侠、英雄故事的读者。书中展现的兄弟情义和侠义精神令人向往。',
    quote: '他时若遂凌云志，敢笑黄巢不丈夫！',
    audioUrl: '/audio/水浒传.MP3',
    quoteAudioUrl: '/audio/水浒，他时若遂凌云志，敢笑黄巢不丈夫！.mp3',
    videoUrl: '/videos/水浒传.mp4',
    mobileVideoUrl: '/videos/水浒传.mp4'
  },
  {
    id: 7,
    title: '水经注',
    author: '郦道元',
    tags: ['地理', '古代', '学术'],
    description: '北魏郦道元所著的综合性地理著作，是对《水经》的详细注释和补充。全书记载了1000多条水道，涉及地理、历史、考古、文学等多个领域，被誉为"宇内奇书"。',
    recommendation: '这不仅是一部地理著作，更是一部文学珍品。郦道元用优美的文笔描绘祖国山川，记录历史人文。适合对中国地理、历史、古代文化感兴趣的读者。读此书可领略古代中国的壮美河山。',
    quote: '山水有灵，亦当惊知己于千古矣！',
    audioUrl: '/audio/水经注.MP3',
    quoteAudioUrl: '/audio/水经注，山水有灵，亦当惊知己于千古矣！.mp3',
    videoUrl: '/videos/水经注.mp4',
    mobileVideoUrl: '/videos/水经注.mp4'
  },
  {
    id: 8,
    title: '简爱',
    author: '夏洛蒂·勃朗特',
    tags: ['爱情', '女性', '成长'],
    description: '19世纪英国女作家夏洛蒂·勃朗特的代表作，讲述了孤女简爱从童年到成年，经历种种磨难，最终获得真爱和独立的故事。塑造了一个追求平等、独立的女性形象。',
    recommendation: '这是女性文学的里程碑之作。简爱"我和你的灵魂是平等的"这句宣言，激励了无数女性追求独立与尊严。适合所有渴望独立、追求真爱的读者，尤其推荐给女性读者。',
    quote: '你以为我贫穷、相貌平平就没有感情吗？我向你发誓，如果上帝赋予我财富和美貌，我会让你无法离开我，就像我现在无法离开你一样。',
    audioUrl: '/audio/简爱.MP3',
    quoteAudioUrl: '/audio/简爱，你以为我贫穷、相貌平平就没有感情吗？我向你发誓，如果上帝赋予我财富和美貌，我会让你无法离开我，就像我现在无法离开你一样。  .mp3',
    videoUrl: '/videos/简爱.mp4',
    mobileVideoUrl: '/videos/简爱.mp4'
  },
  {
    id: 9,
    title: '聊斋志异',
    author: '蒲松龄',
    tags: ['志怪', '古代', '故事'],
    description: '清代文言短篇小说集，作者蒲松龄用一生心血创作了491篇志怪传奇故事。通过花妖狐魅的奇幻世界，讽刺社会黑暗，歌颂纯真爱情，揭露人性善恶。',
    recommendation: '这是中国古代志怪小说的巅峰之作。《聂小倩》《画皮》等故事家喻户晓，充满浪漫主义色彩。适合喜欢奇幻故事、古典文学的读者。蒲松龄笔下的鬼怪比人更有情有义。',
    quote: '书痴者文必工，艺痴者技必良。',
    audioUrl: '/audio/聊斋.MP3',
    quoteAudioUrl: '/audio/聊斋，书痴者文必工，艺痴者技必良。.mp3',
    videoUrl: '/videos/聊斋.mp4',
    mobileVideoUrl: '/videos/聊斋.mp4'
  },
  {
    id: 10,
    title: '西游记',
    author: '吴承恩',
    tags: ['神话', '冒险', '古典'],
    description: '中国四大名著之一，讲述唐僧师徒四人西天取经的传奇故事。孙悟空、猪八戒、沙僧保护唐僧，历经九九八十一难，最终取得真经。充满想象力的神魔世界令人着迷。',
    recommendation: '这是中国神魔小说的巅峰之作，想象力天马行空。孙悟空大闹天宫、三打白骨精等情节深入人心。适合所有年龄段读者，既是精彩的冒险故事，也蕴含深刻的人生哲理。',
    quote: '山高自有客行路，水深自有渡船人。',
    audioUrl: '/audio/西游记.MP3',
    quoteAudioUrl: '/audio/西游记山高自有客行路，水深自有渡船人。.mp3',
    videoUrl: '/videos/西游记.mp4',
    mobileVideoUrl: '/videos/西游记.mp4'
  },
  {
    id: 11,
    title: '云边有个小卖铺',
    author: '张嘉佳',
    tags: ['青春', '治愈', '温情'],
    description: '当代作家张嘉佳的治愈系长篇小说。讲述了少年刘十三的成长故事，山间的云边镇，外婆的小卖铺，以及那些温暖的人和事。一个关于爱与成长、守护与告别的故事。',
    recommendation: '这是一本让人又哭又笑的治愈之书。张嘉佳用温柔的文字书写平凡人的故事，让人在阅读中找到共鸣和慰藉。适合所有需要温暖、寻找人生意义的读者。读完会让你更珍惜身边的人。',
    quote: '',
    audioUrl: '',
    quoteAudioUrl: '',
    videoUrl: '/videos/云边有个小卖铺.mp4',
    mobileVideoUrl: '/videos/云边有个小卖铺.mp4'
  }
])

// 计算属性
const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value
  return books.value.filter(book => 
    book.title.includes(searchQuery.value) ||
    book.author.includes(searchQuery.value) ||
    book.tags.some(tag => tag.includes(searchQuery.value))
  )
})

// 方法

const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const goBack = () => {
  // 返回上一页或主页
  window.history.back()
}

// 显示书籍详情
const showBookDetail = (book: Book) => {
  selectedBook.value = book
  
  // 🚀 检查是否有预加载的资源（静默检查）
  mediaPreloader.getPreloadedMedia(book.id)
}

// 关闭书籍详情 - 完全停止所有媒体
const closeBookDetail = () => {
  if (detailVideoPlayer.value) {
    detailVideoPlayer.value.pause()
    detailVideoPlayer.value.currentTime = 0
    detailVideoPlayer.value.src = ''
    detailVideoPlayer.value.load()
  }
  
  if (detailQuoteAudioPlayer.value) {
    detailQuoteAudioPlayer.value.pause()
    detailQuoteAudioPlayer.value.currentTime = 0
    detailQuoteAudioPlayer.value.src = ''
    detailQuoteAudioPlayer.value.load()
  }
  
  if (detailAudioPlayer.value) {
    detailAudioPlayer.value.pause()
    detailAudioPlayer.value.currentTime = 0
    detailAudioPlayer.value.src = ''
    detailAudioPlayer.value.load()
  }
  
  selectedBook.value = null
}

// 详情视频真正开始播放时 - 同步播放两个音频（确保完全同步）
const applyVideoMuteStateToAudio = () => {
  if (!detailVideoPlayer.value) return

  const muted = detailVideoPlayer.value.muted
  const volume = detailVideoPlayer.value.volume

  if (detailQuoteAudioPlayer.value) {
    detailQuoteAudioPlayer.value.muted = muted
    detailQuoteAudioPlayer.value.volume = muted ? 0 : volume
  }

  if (detailAudioPlayer.value) {
    detailAudioPlayer.value.muted = muted
    detailAudioPlayer.value.volume = muted ? 0 : volume
  }
}

const pauseDetailAudios = () => {
  if (detailQuoteAudioPlayer.value) {
    detailQuoteAudioPlayer.value.pause()
  }
  if (detailAudioPlayer.value) {
    detailAudioPlayer.value.pause()
  }
}

const stopDetailAudios = () => {
  if (detailQuoteAudioPlayer.value) {
    detailQuoteAudioPlayer.value.pause()
    detailQuoteAudioPlayer.value.currentTime = 0
  }
  if (detailAudioPlayer.value) {
    detailAudioPlayer.value.pause()
    detailAudioPlayer.value.currentTime = 0
  }
}

const onDetailVideoPlaying = () => {
  // 只有当视频真正开始播放（缓冲完成）时，才播放音频
  if (detailQuoteAudioPlayer.value && detailQuoteAudioPlayer.value.paused) {
    detailQuoteAudioPlayer.value.play().catch(() => {})
  }
  if (detailAudioPlayer.value && detailAudioPlayer.value.paused) {
    detailAudioPlayer.value.play().catch(() => {})
  }
  applyVideoMuteStateToAudio()
}

// 详情视频暂停事件 - 同步暂停两个音频
const onDetailVideoPause = () => {
  pauseDetailAudios()
}

// 详情视频播放结束 - 重置两个音频
const onDetailVideoEnded = () => {
  stopDetailAudios()
}

const onDetailVideoVolumeChange = () => {
  applyVideoMuteStateToAudio()
}


const setVideoPoster = (bookId: number) => {
  if (videoPosterSet.value.has(bookId)) return
  
  const videoElement = document.querySelector(`video.book-video-poster[data-book-id="${bookId}"]`) as HTMLVideoElement
  if (videoElement && videoElement.readyState >= 2) {
    videoPosterSet.value.add(bookId)
    videoElement.currentTime = 0.1
    videoElement.addEventListener('seeked', () => {
      videoElement.pause()
    }, { once: true })
  }
}

// 初始化所有视频封面
const initAllVideoPosters = () => {
  setTimeout(() => {
    const videoElements = document.querySelectorAll('video.book-video-poster') as NodeListOf<HTMLVideoElement>
    
    videoElements.forEach((videoElement, index) => {
      const bookId = parseInt(videoElement.getAttribute('data-book-id') || '0')
      if (!bookId || videoPosterSet.value.has(bookId)) return
      
      // 分批加载，每个延迟50ms，避免阻塞
      setTimeout(() => {
        videoElement.load()
        videoElement.play().then(() => {
          setTimeout(() => {
            videoElement.pause()
            videoPosterSet.value.add(bookId)
          }, 100)
        }).catch(() => {})
      }, index * 50)
    })
  }, 100)
}

const playVideoAndAudio = (book: Book) => {
  const resolvedVideoUrl = getVideoUrl(book)
  // 如果当前正在播放同一个内容，则暂停
  if (currentAudio.value && currentAudio.value.id === book.id) {
    pauseVideoAndAudio()
    return
  }
  
  // 停止当前播放的内容
  stopVideoAndAudio()
  
  // 🚀 优先使用预加载的资源
  const preloaded = mediaPreloader.getPreloadedMedia(book.id)
  let quoteAudio: HTMLAudioElement | null = null
  let fullAudio: HTMLAudioElement | null = null
  let video: HTMLVideoElement
  
  if (preloaded && preloaded.ready) {
    // ✅ 使用预加载的资源（已经缓冲完成，立即播放）
    if (preloaded.quoteAudioUrl) {
      quoteAudio = new Audio(preloaded.quoteAudioUrl)
      quoteAudio.preload = 'auto'
      quoteAudio.currentTime = 0
    }
    
    if (preloaded.audioUrl) {
      fullAudio = new Audio(preloaded.audioUrl)
      fullAudio.preload = 'auto'
      fullAudio.currentTime = 0
    }
    
    video = document.createElement('video')
    video.src = resolvedVideoUrl
    video.preload = 'auto'
    video.style.display = 'block'
  } else {
    // ⚠️ 未预加载，创建新的元素（可能需要缓冲）
    if (book.quoteAudioUrl && book.quoteAudioUrl.trim() !== '') {
      quoteAudio = new Audio(book.quoteAudioUrl)
      quoteAudio.preload = 'auto'
    }
    
    if (book.audioUrl && book.audioUrl.trim() !== '') {
      fullAudio = new Audio(book.audioUrl)
      fullAudio.preload = 'auto'
    }
    
    video = document.createElement('video')
    video.src = resolvedVideoUrl
  }
  
  // 创建视频容器
  const videoContainer = document.createElement('div')
  videoContainer.style.position = 'fixed'
  videoContainer.style.top = '0'
  videoContainer.style.left = '0'
  videoContainer.style.width = '100%'
  videoContainer.style.height = '100%'
  videoContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)'
  videoContainer.style.zIndex = '2000'
  videoContainer.style.display = 'flex'
  videoContainer.style.alignItems = 'center'
  videoContainer.style.justifyContent = 'center'
  videoContainer.style.cursor = 'pointer'
  videoContainer.onclick = () => stopVideoAndAudio()
  
  // 配置视频样式
  video.muted = false
  video.volume = 1
  video.loop = false
  video.preload = 'auto'
  video.style.width = '80%'
  video.style.maxWidth = '800px'
  video.style.height = 'auto'
  video.style.borderRadius = '15px'
  video.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)'
  video.controls = true
  video.onclick = (e) => e.stopPropagation()

  const syncOverlayMuteState = () => {
    const muted = video.muted
    const volume = video.volume
    if (quoteAudio) {
      quoteAudio.muted = muted
      quoteAudio.volume = muted ? 0 : volume
    }
    if (fullAudio) {
      fullAudio.muted = muted
      fullAudio.volume = muted ? 0 : volume
    }
  }

  const pauseOverlayAudios = () => {
    if (quoteAudio) {
      quoteAudio.pause()
    }
    if (fullAudio) {
      fullAudio.pause()
    }
    isAudioPlaying.value = false
  }

  const startOverlayAudios = () => {
    syncOverlayMuteState()
    if (quoteAudio && quoteAudio.paused) {
      quoteAudio.play().catch(() => {})
    }
    if (fullAudio && fullAudio.paused) {
      fullAudio.play().catch(() => {})
    }
    isAudioPlaying.value = true
  }
  
  // 添加错误处理
  video.addEventListener('error', () => {
    const errorDiv = document.createElement('div')
    errorDiv.style.color = 'white'
    errorDiv.style.textAlign = 'center'
    errorDiv.style.padding = '20px'
    errorDiv.innerHTML = `
      <h3>视频加载失败</h3>
      <p>《${book.title}》</p>
      <p>请检查视频文件格式或网络连接</p>
      <button onclick="this.parentElement.parentElement.click()" style="margin-top: 10px; padding: 8px 16px; background: #ff6b6b; color: white; border: none; border-radius: 4px; cursor: pointer;">关闭</button>
    `
    videoContainer.replaceChild(errorDiv, video)
  })
  
  // 创建关闭按钮
  const closeBtn = document.createElement('button')
  closeBtn.innerHTML = '×'
  closeBtn.style.position = 'absolute'
  closeBtn.style.top = '20px'
  closeBtn.style.right = '20px'
  closeBtn.style.width = '40px'
  closeBtn.style.height = '40px'
  closeBtn.style.borderRadius = '50%'
  closeBtn.style.border = 'none'
  closeBtn.style.backgroundColor = 'rgba(255, 255, 255, 0.2)'
  closeBtn.style.color = 'white'
  closeBtn.style.fontSize = '24px'
  closeBtn.style.cursor = 'pointer'
  closeBtn.style.display = 'flex'
  closeBtn.style.alignItems = 'center'
  closeBtn.style.justifyContent = 'center'
  closeBtn.onclick = (e) => {
    e.stopPropagation()
    stopVideoAndAudio()
  }
  
  // 添加到容器
  videoContainer.appendChild(video)
  videoContainer.appendChild(closeBtn)
  
  // 添加到页面
  document.body.appendChild(videoContainer)
  
  // 设置当前播放内容
  currentAudio.value = {
    ...book,
    audio: fullAudio || undefined,
    quoteAudio: quoteAudio || undefined,
    video: video
  }
  
  // 监听音频结束事件
  if (quoteAudio) {
    quoteAudio.addEventListener('ended', () => {
      stopVideoAndAudio()
    })
  }
  
  if (fullAudio) {
    fullAudio.addEventListener('ended', () => {
      stopVideoAndAudio()
    })
  }
  
  // 监听视频结束事件
  video.addEventListener('ended', () => {
    stopVideoAndAudio()
  })

  video.addEventListener('play', startOverlayAudios)

  video.addEventListener('pause', () => {
    if (video.ended) return
    pauseOverlayAudios()
  })

  video.addEventListener('volumechange', syncOverlayMuteState)
  
  // 先启动视频播放
  syncOverlayMuteState()
  video.play().catch(() => {
    stopVideoAndAudio()
  })
}

const pauseVideoAndAudio = () => {
  if (currentAudio.value) {
    if (currentAudio.value.quoteAudio) {
      currentAudio.value.quoteAudio.pause()
    }
    if (currentAudio.value.audio) {
      currentAudio.value.audio.pause()
    }
    if (currentAudio.value.video) {
      currentAudio.value.video.pause()
    }
    isAudioPlaying.value = false
  }
}

const stopVideoAndAudio = () => {
  if (currentAudio.value) {
    if (currentAudio.value.quoteAudio) {
      currentAudio.value.quoteAudio.pause()
      currentAudio.value.quoteAudio.currentTime = 0
      currentAudio.value.quoteAudio.src = ''
    }
    if (currentAudio.value.audio) {
      currentAudio.value.audio.pause()
      currentAudio.value.audio.currentTime = 0
      currentAudio.value.audio.src = ''
    }
    if (currentAudio.value.video) {
      currentAudio.value.video.pause()
      currentAudio.value.video.currentTime = 0
      const videoContainer = currentAudio.value.video.closest('div')
      if (videoContainer && videoContainer.parentNode) {
        videoContainer.parentNode.removeChild(videoContainer)
      }
    }
    isAudioPlaying.value = false
    currentAudio.value = null
  }
}

// 视频加载完成（推荐页面始终静音）
const onVideoLoaded = () => {
  if (backgroundVideo.value) {
    backgroundVideo.value.muted = true
    backgroundVideo.value.volume = 0
    backgroundVideo.value.play().catch(() => {})
  }
}

// 生命周期
onMounted(() => {
  // 确保视频在移动端可以播放
  if (backgroundVideo.value) {
    backgroundVideo.value.setAttribute('playsinline', 'true')
    backgroundVideo.value.setAttribute('webkit-playsinline', 'true')
    
    // 移动端特殊处理
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent)
    const isAndroid = /Android/.test(navigator.userAgent)
    
    if (isIOS || isAndroid) {
      // 移动端可能需要用户交互才能播放有声音的视频
      backgroundVideo.value.setAttribute('x5-video-player-type', 'h5')
      backgroundVideo.value.setAttribute('x5-video-player-fullscreen', 'false')
    }
  }
  
  // 初始化所有视频封面
  initAllVideoPosters()
  
  // 🚀 注册所有书籍到预加载器
  mediaPreloader.register(books.value.map(book => ({
    id: book.id,
    title: book.title,
    videoUrl: getVideoUrl(book),
    audioUrl: book.audioUrl,
    quoteAudioUrl: book.quoteAudioUrl
  })))
  
  // 🚀 延迟500ms后开始预加载（避免阻塞首屏渲染）
  setTimeout(() => {
    mediaPreloader.startPreload()
  }, 500)
  
  // 监听用户第一次交互，确保视频封面加载
  const handleFirstInteraction = () => {
    initAllVideoPosters()
    document.removeEventListener('click', handleFirstInteraction)
    document.removeEventListener('touchstart', handleFirstInteraction)
    document.removeEventListener('scroll', handleFirstInteraction)
  }
  
  document.addEventListener('click', handleFirstInteraction, { once: true })
  document.addEventListener('touchstart', handleFirstInteraction, { once: true })
  document.addEventListener('scroll', handleFirstInteraction, { once: true })
})

onUnmounted(() => {
  stopVideoAndAudio()
  
  if (backgroundVideo.value) {
    backgroundVideo.value.pause()
  }
  
  // 清理预加载的资源
  mediaPreloader.cleanup()
})
</script>

<style scoped>
/* 科技风荐书页面 */
.ai-recommendation {
  min-height: 100vh;
  position: relative;
  background: var(--dark-gradient);
  overflow-x: hidden;
}

.digital-human-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.2;
  filter: brightness(0.5) contrast(1.2);
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(0, 212, 255, 0.1) 0%, rgba(139, 0, 255, 0.1) 100%);
  backdrop-filter: blur(2px);
}

/* 科技风内容容器 */
.content-container {
  position: relative;
  z-index: 1;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  backdrop-filter: blur(10px);
}

/* 科技风页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary-neon);
  position: relative;
}

.back-button {
  position: absolute;
  top: 0;
  right: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--glass-bg);
  border: 2px solid var(--glass-border);
  color: var(--primary-neon);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  transition: all var(--transition-fast);
  z-index: 10;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.back-button:hover {
  background: rgba(0, 212, 255, 0.2);
  border-color: var(--primary-neon);
  transform: translateY(-2px);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6);
}

.back-button:active {
  transform: translateY(-1px) scale(0.98);
}

.page-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
  letter-spacing: 1px;
}

.page-subtitle {
  font-size: 16px;
  opacity: 0.8;
  margin: 0;
  color: var(--accent-cyan);
}

/* 科技风搜索区域 */
.search-section {
  margin-bottom: 30px;
}

.search-container {
  display: flex;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 16px 20px;
  border: 2px solid var(--glass-border);
  border-radius: 25px;
  font-size: 16px;
  background: rgba(0, 212, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
  outline: none;
  color: var(--primary-neon);
  transition: all var(--transition-fast);
}

.search-input::placeholder {
  color: rgba(0, 212, 255, 0.6);
}

.search-input:focus {
  border-color: var(--primary-neon);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
  background: rgba(0, 212, 255, 0.15);
}

.search-btn {
  padding: 12px 16px;
  background: transparent;
  border: 2px solid var(--primary-neon);
  border-radius: 20px;
  color: var(--primary-neon);
  cursor: pointer;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
  transition: all var(--transition-fast);
  min-width: 60px;
  position: relative;
  overflow: hidden;
}

.search-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.3;
  transition: left var(--transition-fast);
}

.search-btn:hover::before {
  left: 100%;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6);
  background: rgba(0, 212, 255, 0.1);
}

/* 科技风书籍网格 */
.books-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 100px;
  width: 100%;
}

.book-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border-radius: var(--glass-radius);
  padding: 0;
  box-shadow: var(--card-shadow);
  transition: all var(--transition-normal);
  cursor: pointer;
  overflow: hidden;
  border: 1px solid var(--glass-border);
  position: relative;
}

.book-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.1;
  transition: left var(--transition-normal);
  z-index: 1;
}

.book-card:hover::before {
  left: 100%;
}

.book-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: var(--hover-shadow);
  border-color: var(--primary-neon);
}

.book-cover {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: var(--tech-gradient);
}

.book-video-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius);
  background: #000;
}

.book-video-poster::-webkit-media-controls {
  display: none !important;
}

.book-video-poster::-webkit-media-controls-enclosure {
  display: none !important;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
}

.play-button {
  width: 70px;
  height: 70px;
  background: var(--glass-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-neon);
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
  backdrop-filter: blur(10px);
  border: 2px solid var(--primary-neon);
}

.book-card:hover .play-overlay {
  background: rgba(0, 212, 255, 0.2);
  border-color: var(--primary-neon);
}

.book-card:hover .play-button {
  transform: scale(1.1);
  background: rgba(0, 212, 255, 0.2);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
}

.book-info {
  padding: 16px 20px;
  background: rgba(0, 212, 255, 0.05);
  border-radius: 0 0 var(--border-radius) var(--border-radius);
}

.book-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-neon);
  margin: 0 0 8px 0;
  line-height: 1.3;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.book-author {
  font-size: 14px;
  color: var(--accent-cyan);
  margin: 0 0 12px 0;
  font-weight: 500;
  opacity: 0.8;
}

.book-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 12px;
  background: var(--tech-gradient);
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 212, 255, 0.3);
}

/* ==================== 书籍详情弹窗 ==================== */
.book-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.detail-container {
  position: relative;
  width: 100%;
  max-width: 1100px;
  max-height: 85vh;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.close-detail-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 24px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-detail-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.detail-content {
  display: flex;
  gap: 30px;
  padding: 30px;
  max-height: 85vh;
  overflow-y: auto;
}

.detail-left {
  flex: 1;
  min-width: 400px;
}

.detail-video-wrapper {
  position: relative;
  width: 100%;
  border-radius: 15px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.detail-video {
  width: 100%;
  height: auto;
  display: block;
}

.detail-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-title {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0;
  line-height: 1.3;
}

.detail-author {
  font-size: 16px;
  color: #666;
  margin: 0;
  font-weight: 500;
}

.detail-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.detail-tag {
  padding: 6px 14px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 15px;
  font-size: 13px;
  font-weight: 600;
}

.quote-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-left: 4px solid #667eea;
  padding: 16px 20px;
  border-radius: 8px;
  position: relative;
  margin: 8px 0;
}

.quote-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 36px;
  color: rgba(102, 126, 234, 0.3);
  line-height: 1;
}

.quote-text {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  font-style: italic;
  font-weight: 500;
  margin: 0;
  padding-left: 30px;
  text-align: justify;
}

.detail-section {
  border-top: 1px solid #e5e7eb;
  padding-top: 16px;
}

.section-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #667eea;
  margin: 0 0 12px 0;
}

.section-text {
  font-size: 15px;
  line-height: 1.8;
  color: #555;
  margin: 0;
  text-align: justify;
}

.recommendation-highlight {
  background: rgba(102, 126, 234, 0.05);
  border-left: 3px solid #667eea;
  padding: 12px 16px;
  border-radius: 8px;
}

.detail-actions {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.action-btn {
  padding: 12px 40px;
  border: none;
  border-radius: 20px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.close-btn-secondary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.close-btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(102, 126, 234, 0.5);
}

.audio-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.player-info {
  text-align: center;
  margin-bottom: 15px;
}

.player-info h4 {
  margin: 0;
  color: #333;
}

.player-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.control-btn {
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.control-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.video-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  background: #000;
  border-radius: 15px;
  overflow: hidden;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 24px;
  cursor: pointer;
  z-index: 2001;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-player {
  width: 100%;
  height: auto;
  max-height: 70vh;
}

.video-info {
  padding: 20px;
  background: #333;
  color: white;
}

.video-info h3 {
  margin: 0;
  font-size: 18px;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .content-container {
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
    flex-direction: column;
    gap: 8px;
  }
  
  .back-button {
    width: 36px;
    height: 36px;
    top: 5px;
    right: 5px;
  }
  
  .page-subtitle {
    font-size: 14px;
  }
  
  .search-container {
    flex-direction: row;
    gap: 8px;
  }
  
  .search-input {
    padding: 12px 16px;
    font-size: 14px;
  }
  
  .search-btn {
    padding: 12px 16px;
    min-width: 50px;
  }
  
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .book-cover {
    height: 140px;
  }
  
  .play-button {
    width: 50px;
    height: 50px;
  }
  
  .play-button svg {
    width: 25px;
    height: 25px;
  }
  
  .book-info {
    padding: 12px;
  }
  
  .book-title {
    font-size: 16px;
  }
  
  .book-author {
    font-size: 12px;
  }
  
  .tag {
    font-size: 11px;
    padding: 3px 10px;
  }
  
  /* 详情弹窗移动端优化 */
  .book-detail-modal {
    padding: 10px;
  }
  
  .detail-container {
    max-height: 90vh;
    border-radius: 15px;
  }
  
  .detail-content {
    flex-direction: column;
    padding: 15px;
    gap: 15px;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .detail-left {
    min-width: 100%;
    max-width: 100%;
  }
  
  .detail-video-wrapper {
    max-height: 35vh;
  }
  
  .detail-video {
    max-height: 35vh;
    object-fit: contain;
  }
  
  .detail-right {
    gap: 15px;
  }
  
  .detail-title {
    font-size: 20px;
  }
  
  .detail-author {
    font-size: 13px;
  }
  
  .detail-tag {
    font-size: 11px;
    padding: 4px 10px;
  }
  
  .section-heading {
    font-size: 14px;
  }
  
  .section-text {
    font-size: 13px;
    line-height: 1.6;
  }
  
  .action-btn {
    padding: 10px 30px;
    font-size: 14px;
  }
  
  
  .audio-player {
    padding: 15px;
  }
  
  .video-modal {
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .back-button {
    width: 32px;
    height: 32px;
    top: 3px;
    right: 3px;
  }
  
  .search-container {
    gap: 6px;
  }
  
  .search-input {
    padding: 10px 14px;
    font-size: 14px;
  }
  
  .search-btn {
    padding: 10px 12px;
    min-width: 45px;
  }
  
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .book-cover {
    height: 140px;
  }
  
  .play-button {
    width: 40px;
    height: 40px;
  }
  
  .play-button svg {
    width: 20px;
    height: 20px;
  }
  
  .book-info {
    padding: 8px 10px;
  }
  
  .book-title {
    font-size: 14px;
  }
  
  .book-author {
    font-size: 11px;
  }
  
  .tag {
    font-size: 10px;
    padding: 2px 8px;
  }
  
  /* 详情弹窗小屏优化 */
  .book-detail-modal {
    padding: 5px;
  }
  
  .detail-container {
    max-height: 92vh;
    border-radius: 12px;
  }
  
  .detail-content {
    padding: 12px;
    gap: 12px;
    max-height: 92vh;
  }
  
  .detail-video-wrapper {
    max-height: 30vh;
  }
  
  .detail-video {
    max-height: 30vh;
  }
  
  .detail-title {
    font-size: 18px;
  }
  
  .detail-author {
    font-size: 12px;
  }
  
  .detail-tag {
    font-size: 10px;
    padding: 3px 8px;
  }
  
  .section-heading {
    font-size: 13px;
  }
  
  .section-text {
    font-size: 12px;
    line-height: 1.5;
  }
  
  .action-btn {
    padding: 8px 20px;
    font-size: 13px;
  }
  
  .close-detail-btn {
    width: 32px;
    height: 32px;
    font-size: 20px;
    top: 10px;
    right: 10px;
  }
}
</style>

/* 科技风按钮样式 */
.action-btn {
  padding: 12px 40px;
  border: 2px solid var(--primary-neon);
  border-radius: 20px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all var(--transition-fast);
  background: transparent;
  color: var(--primary-neon);
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--neon-gradient);
  opacity: 0.3;
  transition: left var(--transition-fast);
  z-index: -1;
}

.action-btn:hover::before {
  left: 100%;
}

.close-btn-secondary {
  background: transparent;
  color: var(--primary-neon);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.close-btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.6);
  background: rgba(0, 212, 255, 0.1);
}

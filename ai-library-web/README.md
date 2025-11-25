# 钦州图书馆 · 前端（简洁版）

本项目基于 Vue 3 + Vite，已内置 Dify AI 流式问答能力。

运行步骤：

1. 安装 Node.js ≥ 18
2. 在项目根目录创建 `.env`（参考下方内容）
3. 安装依赖并启动开发服务器

建议的 `.env` 内容：

```
VITE_DIFY_BASE_PATH=/dify
VITE_DIFY_TARGET=http://124.71.97.68
VITE_DIFY_APP_KEY=app-ka994zy9N68cJgaEznXHqbfL #AI助手的key
```

**注意**：当前项目使用的是部署在服务器 `124.71.97.68` 上的 Dify 服务。

启动命令：

```
npm i
npm run dev
```

说明要点：

- Dify 服务地址：`http://124.71.97.68/v1` （已在 `src/services/dify.ts` 中配置）
- `src/services/dify.ts` 使用 SSE 流式接口，前端逐字显示答案
- Vite 开发服务器运行在端口 `5199`
- 支持微信浏览器访问，已优化缓存控制




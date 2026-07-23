/**
 * kuaipao.pro CORS Proxy Worker
 *
 * 部署到 Cloudflare Workers：
 * 1. 登录 https://dash.cloudflare.com/
 * 2. Workers 和 Pages → 创建 Worker
 * 3. 把本文件内容粘贴进去 → 部署
 * 4. 获得 https://你的子域名.workers.dev
 *
 * 用法：把 endpoint 填到 subtitle-translator 的自定义平台中
 *   Endpoint: https://你的子域名.workers.dev
 *   API Key:  你的 kuaipao.pro key
 *   模型:      claude-sonnet-5 / deepseek-v4-pro / gemini-3-pro-preview 等
 */

const KUAIPAO_BASE = 'https://kuaipao.pro/v1';
const MAX_RETRIES = 3;          // 429 时最多重试次数
const INITIAL_BACKOFF = 1000;   // 首次重试等待 1s，每次翻倍

export default {
  async fetch(request, env, ctx) {
    // 仅处理 POST
    if (request.method === 'OPTIONS') {
      return corsResponse(new Response(null, { status: 204 }));
    }
    if (request.method !== 'POST') {
      return corsResponse(new Response('Method not allowed', { status: 405 }));
    }

    // 从请求中提取模型、消息等参数
    let body;
    try {
      body = await request.json();
    } catch {
      return corsResponse(new Response(JSON.stringify({ error: { message: 'Invalid JSON body' } }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      }));
    }

    const model = body.model || '';
    const authHeader = request.headers.get('Authorization') || '';

    // 路由：根据模型名决定用哪个 kuaipao token
    // 优先用请求头里的 Authorization
    let apiKey = authHeader.replace(/^Bearer\s+/i, '').trim();
    if (!apiKey) {
      return corsResponse(new Response(JSON.stringify({ error: { message: 'Missing API key' } }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      }));
    }

    // 构造发往 kuaipao.pro 的请求
    const targetUrl = `${KUAIPAO_BASE}/chat/completions`;

    // 带重试的请求
    let lastError = null;
    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      try {
        const resp = await fetch(targetUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
          },
          body: JSON.stringify(body),
        });

        // 429 Too Many Requests → 指数退避重试
        if (resp.status === 429) {
          const retryAfter = parseInt(resp.headers.get('Retry-After') || '0');
          const wait = retryAfter > 0 ? retryAfter * 1000 : INITIAL_BACKOFF * Math.pow(2, attempt);
          await sleep(wait);
          lastError = `Rate limited, retry ${attempt + 1}/${MAX_RETRIES}`;
          continue;
        }

        // 其他状态直接透传
        const responseHeaders = new Headers(resp.headers);
        // 清理服务端返回的可能冲突的 CORS 头
        responseHeaders.delete('Access-Control-Allow-Origin');
        responseHeaders.set('Access-Control-Allow-Origin', '*');

        return new Response(resp.body, {
          status: resp.status,
          headers: responseHeaders,
        });

      } catch (err) {
        lastError = err.message;
        if (attempt < MAX_RETRIES - 1) {
          await sleep(INITIAL_BACKOFF * Math.pow(2, attempt));
        }
      }
    }

    // 所有重试都失败
    return corsResponse(new Response(JSON.stringify({
      error: { message: `Proxy error after ${MAX_RETRIES} retries: ${lastError}` }
    }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    }));
  },
};

function corsResponse(response) {
  const headers = new Headers(response.headers);
  headers.set('Access-Control-Allow-Origin', '*');
  headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  return new Response(response.body, {
    status: response.status,
    headers,
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

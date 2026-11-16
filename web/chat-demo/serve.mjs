import http from 'node:http'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
  '.txt': 'text/plain; charset=utf-8',
}

function resolveSafeFile(distDir, requestUrl) {
  const cleanUrl = (requestUrl || '/').split('?')[0].split('#')[0]
  let decodedPath = '/'
  try {
    decodedPath = decodeURIComponent(cleanUrl)
  } catch {
    decodedPath = '/'
  }

  const relativePath = decodedPath.replace(/^\/+/, '')
  const candidate = path.resolve(distDir, relativePath || 'index.html')

  if (!candidate.startsWith(distDir)) {
    return path.join(distDir, 'index.html')
  }
  if (fs.existsSync(candidate) && fs.statSync(candidate).isFile()) {
    return candidate
  }
  return path.join(distDir, 'index.html')
}

export function startStaticServer({ distCandidates, serviceName = 'minihouse-web' }) {
  const distDir =
    distCandidates.find((dir) => fs.existsSync(path.join(dir, 'index.html'))) ?? distCandidates[0]
  const port = Number(process.env.PORT || 8090)
  const host = process.env.HOST || '0.0.0.0'

  const server = http.createServer((req, res) => {
    const pathname = (req.url || '/').split('?')[0]
    if (pathname === '/health' || pathname === '/healthz') {
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' })
      res.end(JSON.stringify({ ok: true, service: serviceName }))
      return
    }

    const filePath = resolveSafeFile(distDir, req.url)
    if (!fs.existsSync(filePath)) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' })
      res.end('Build output not found. Run "pnpm build" or "npm run build" first.')
      return
    }

    const ext = path.extname(filePath).toLowerCase()
    const contentType = MIME_TYPES[ext] || 'application/octet-stream'
    const isHashedAsset = filePath.includes(`${path.sep}static${path.sep}`)
    const cacheControl = isHashedAsset ? 'public, max-age=31536000, immutable' : 'no-cache'

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': cacheControl,
    })
    fs.createReadStream(filePath).pipe(res)
  })

  return server.listen(port, host, () => {
    const addr = server.address()
    const actualPort = typeof addr === 'object' && addr ? addr.port : port
    console.log(`${serviceName} listening on http://${host}:${actualPort} (serving ${distDir})`)
  })
}

const isMain =
  process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url

if (isMain) {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  startStaticServer({
    distCandidates: [path.join(__dirname, 'dist')],
    serviceName: 'minihouse-chat-demo',
  })
}

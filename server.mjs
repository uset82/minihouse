import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { startStaticServer } from './web/chat-demo/serve.mjs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

startStaticServer({
  distCandidates: [
    path.join(__dirname, 'dist'),
    path.join(__dirname, 'web', 'chat-demo', 'dist'),
  ],
  serviceName: 'minihouse-web',
})

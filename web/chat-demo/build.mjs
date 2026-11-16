import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const dir = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(import.meta.url)

fs.rmSync(path.join(dir, 'dist'), { recursive: true, force: true })

const rspackPkgPath = require.resolve('@rspack/cli/package.json')
const rspackBin = path.join(path.dirname(rspackPkgPath), 'bin', 'rspack.js')

execFileSync(process.execPath, [rspackBin, 'build', '-c', 'rspack.config.ts'], {
  cwd: dir,
  stdio: 'inherit',
  env: { ...process.env, NODE_ENV: 'production' },
})

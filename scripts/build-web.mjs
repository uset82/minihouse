import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const chatDemoDir = path.join(rootDir, 'web', 'chat-demo')
const chatDemoDist = path.join(chatDemoDir, 'dist')
const rootDist = path.join(rootDir, 'dist')

function hasCommand(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' })
    return true
  } catch {
    return false
  }
}

function run(cmd, cwd, nodeEnv = 'production') {
  console.log(`> [${path.relative(rootDir, cwd) || '.'}] ${cmd}`)
  execSync(cmd, {
    cwd,
    stdio: 'inherit',
    env: { ...process.env, NODE_ENV: nodeEnv },
  })
}

const hasRspackLocal = fs.existsSync(
  path.join(chatDemoDir, 'node_modules', '@rspack', 'cli', 'package.json')
)
const hasRspackRoot = fs.existsSync(
  path.join(rootDir, 'node_modules', '@rspack', 'cli', 'package.json')
)

if (!hasRspackLocal && !hasRspackRoot) {
  if (hasCommand('pnpm')) {
    run('pnpm install --prod=false --frozen-lockfile', rootDir, 'development')
  } else {
    run('npm install --include=dev --no-audit --no-fund', chatDemoDir, 'development')
  }
}

run('node build.mjs', chatDemoDir, 'production')

fs.rmSync(rootDist, { recursive: true, force: true })
fs.cpSync(chatDemoDist, rootDist, { recursive: true })
console.log(`Copied production build from ${chatDemoDist} -> ${rootDist}`)

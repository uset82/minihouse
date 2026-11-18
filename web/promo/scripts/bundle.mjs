/*
 * Make the upload for Canner: the built site (dist/) plus the small static server in
 * deploy/ (byte ranges for the film, MIME types, real 404). Writes .bundle/, which is
 * git-ignored. Upload it with:  cd .bundle && canner deploy --slug=<project> --follow
 */
import { cpSync, existsSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const out = join(root, '.bundle');

if (!existsSync(join(dist, 'index.html'))) {
  console.error('dist/ has no index.html: run npm run build first');
  process.exit(1);
}

rmSync(out, { recursive: true, force: true });
cpSync(dist, out, { recursive: true });
for (const file of ['serve.mjs', 'package.json']) {
  cpSync(join(root, 'deploy', file), join(out, file));
}
console.log(`bundle ready: ${out}`);

/*
 * Static server for the built promo site on Canner (Node standard library only).
 *
 * Canner's own static server answers every file as a whole (no byte ranges) and sends
 * video and AVIF as application/octet-stream. Safari won't play a video without byte
 * ranges, so the concept film (DESIGN-GUIDE §6.15) needs this server. It also answers
 * missing pages with 404.html and a real 404 status.
 *
 * `npm run bundle` puts this file and package.json next to the built site in .bundle/;
 * Canner then runs `npm start`. Locally: npm run build && npm run bundle &&
 * node .bundle/serve.mjs  (PORT defaults to 8080).
 */
import { createReadStream, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('.', import.meta.url)));
const port = Number(process.env.PORT || 8080);
const host = process.env.HOST || '0.0.0.0';

const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.ico': 'image/x-icon',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.woff2': 'font/woff2',
  '.mp4': 'video/mp4',
};

// The server's own files are not part of the site. Canner also writes .env.production
// (environment variables) and may install node_modules/ into this folder: never serve a
// path with a part that starts with "." or is node_modules.
const hidden = new Set(['/serve.mjs', '/package.json', '/package-lock.json']);
const isPrivate = (path) => path.split('/').some((part) => part.startsWith('.') || part === 'node_modules');

/** The file for a URL path, or undefined. Folders serve their index.html. */
function locate(pathname) {
  let decoded;
  try {
    decoded = decodeURIComponent(pathname);
  } catch {
    return undefined;
  }
  if (hidden.has(decoded) || isPrivate(decoded)) return undefined;
  const full = normalize(join(root, decoded));
  if (full !== root && !full.startsWith(root + sep)) return undefined;
  try {
    const stat = statSync(full);
    if (stat.isFile()) return { file: full, size: stat.size };
    if (stat.isDirectory()) {
      const index = join(full, 'index.html');
      return { file: index, size: statSync(index).size };
    }
  } catch {
    return undefined;
  }
  return undefined;
}

function cacheFor(pathname) {
  if (pathname.startsWith('/_astro/')) return 'public, max-age=31536000, immutable';
  if (pathname.startsWith('/film/')) return 'public, max-age=3600';
  return 'no-cache';
}

/** Parse a single "bytes=start-end" range; undefined if absent, null if unsatisfiable. */
function parseRange(header, size) {
  if (!header) return undefined;
  const match = /^bytes=(\d*)-(\d*)$/.exec(header.trim());
  if (!match || (match[1] === '' && match[2] === '')) return null;
  let start;
  let end;
  if (match[1] === '') {
    start = Math.max(0, size - Number(match[2]));
    end = size - 1;
  } else {
    start = Number(match[1]);
    end = match[2] === '' ? size - 1 : Math.min(Number(match[2]), size - 1);
  }
  if (!Number.isFinite(start) || !Number.isFinite(end) || start > end || start >= size) return null;
  return { start, end };
}

const server = createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD' });
    res.end();
    return;
  }
  const pathname = (req.url || '/').split('?')[0];
  let found = locate(pathname);
  let status = 200;
  if (!found) {
    found = locate('/404.html');
    status = 404;
    if (!found) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }
  }

  const headers = {
    'Content-Type': types[extname(found.file).toLowerCase()] || 'application/octet-stream',
    'Cache-Control': status === 404 ? 'no-cache' : cacheFor(pathname),
    'Accept-Ranges': 'bytes',
    'X-Content-Type-Options': 'nosniff',
  };

  const range = status === 200 ? parseRange(req.headers.range, found.size) : undefined;
  if (range === null) {
    res.writeHead(416, { ...headers, 'Content-Range': `bytes */${found.size}` });
    res.end();
    return;
  }
  if (range) {
    res.writeHead(206, {
      ...headers,
      'Content-Range': `bytes ${range.start}-${range.end}/${found.size}`,
      'Content-Length': range.end - range.start + 1,
    });
    if (req.method === 'HEAD') res.end();
    else createReadStream(found.file, range).pipe(res);
    return;
  }

  res.writeHead(status, { ...headers, 'Content-Length': found.size });
  if (req.method === 'HEAD') res.end();
  else createReadStream(found.file).pipe(res);
});

server.listen(port, host, () => {
  console.log(`minihouse-promo listening on http://${host}:${port} (serving ${root})`);
});

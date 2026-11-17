// @ts-check
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://minihouse.canner.app',
  integrations: [sitemap()],
  server: {
    port: 4321,
    host: '127.0.0.1',
  },
});

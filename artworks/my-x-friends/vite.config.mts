import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  base: '/my-x-friends/',
  root: fileURLToPath(new URL('.', import.meta.url)),
  build: { emptyOutDir: true, outDir: '../../my-x-friends' },
  server: { host: '127.0.0.1' },
});

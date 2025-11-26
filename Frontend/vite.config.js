// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  root: __dirname,      // frontend root
  publicDir: 'pkg',     // dossier statique
  server: { open: true }
});

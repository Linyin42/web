import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: 'localhost', // Ensure access via localhost
    port: 5173, // Frontend running port
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Backend Flask service address
        changeOrigin: true, // Change origin to solve cross-origin issues
        rewrite: (path) => path.replace(/^\/api/, '') // Remove /api from request path
      },
      '/images': { // New image proxy for fetching crawled movie posters from backend
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
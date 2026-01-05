import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['.abra.me'],
    proxy: {
      '/api': 'http://localhost:8000'
    }
  },
  preview: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})

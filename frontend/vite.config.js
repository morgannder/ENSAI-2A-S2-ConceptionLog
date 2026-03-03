import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [['babel-plugin-react-compiler']],
      },
    }),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            // Decode %7B and %7D back to { } so FastAPI receives the literal path
            proxyReq.path = proxyReq.path.replace(/%7B/gi, '{').replace(/%7D/gi, '}');
          });
        },
      },
    },
  },
})

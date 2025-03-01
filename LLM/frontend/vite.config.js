import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,          // Change if needed
    proxy: {
      '/api': 'http://localhost:5001'  // Forward API requests to backend
    }
  }
});
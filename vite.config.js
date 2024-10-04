import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { sentryVitePlugin } from "@sentry/vite-plugin";
import path from 'path'

export default defineConfig({
  build: {
    sourcemap: true, // Source map generation must be turned on
  },
  plugins: [
    vue(),

    // Put the Sentry vite plugin after all other plugins
    sentryVitePlugin({
      org: "steven-eubank",
      project: "vue-store-pinia",
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { sentryVitePlugin } from "@sentry/vite-plugin";
import { codecovVitePlugin } from "@codecov/vite-plugin"; // Import the Codecov plugin
import path from 'path'

// Load environment variables
export default ({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '')

  console.log("Sentry Auth Token:", env.SENTRY_AUTH_TOKEN || "Token not found");
  console.log("Codecov Token:", env.VITE_CODECOV_TOKEN || "Token not found");

  return defineConfig({
    build: {
      sourcemap: true, // Source map generation must be turned on
    },
    plugins: [
      vue(),

      // Put the Sentry vite plugin after all other plugins
      sentryVitePlugin({
        org: "steven-eubank",
        project: "vue-store-pinia",
        authToken: env.SENTRY_AUTH_TOKEN,
        bundleSizeOptimizations: {
          // excludeDebugStatements: true,
          // excludePerformanceMonitoring: true, // Only if you added browserTracingIntegration
          // excludeReplayIframe: true,         // Only if you added replayIntegration
          // excludeReplayShadowDom: true,      // Only if you added replayIntegration
          // excludeReplayWorker: true,         // Only if you added replayIntegration
        },
      }),
      // Add the Codecov plugin
      codecovVitePlugin({
        enableBundleAnalysis: true,
        bundleName: "vue-store-pinia", // Replace with your bundle project name
        uploadToken: process.env.VITE_CODECOV_TOKEN,
      }),
    ],

    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    }
  })
}
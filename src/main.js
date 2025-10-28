import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import * as Sentry from '@sentry/vue'
import { createSentryPiniaPlugin } from "@sentry/vue";
import { createClient } from '@supabase/supabase-js'
import App from './App.vue'
import LandingPage from './pages/LandingPage.vue'
import ProductsPage from './pages/ProductsPage.vue'
import CheckoutPage from './pages/CheckoutPage.vue'
import AuthCallbackPage from './pages/AuthCallbackPage.vue'
import './global.css' // Import the global CSS file

const routes = [
  { path: '/', component: LandingPage },
  { path: '/products', component: ProductsPage },
  { path: '/checkout', component: CheckoutPage },
  { path: '/auth/callback', component: AuthCallbackPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const pinia = createPinia()

const app = createApp(App)

// Initialize Supabase client
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://sdmizzrivujzvxocsuhw.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkbWl6enJpdnVqenZ4b2NzdWh3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2NTExMDEsImV4cCI6MjA3NzIyNzEwMX0.8JVgE29qln0X2vskBrABBd3zI6VGFwAXbmHM3MPuw1U'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Determine the tunnel URL based on the environment
const isProduction = import.meta.env.PROD
const tunnelUrl = isProduction
  ? 'https://vue-store-pinia.onrender.com/tunnel'
  : 'http://localhost:8000/tunnel'

Sentry.init({
  app,
  dsn: import.meta.env.PUBLIC_SENTRY_DSN || 'https://4a85c87c7894458aff8578d0f2d2dd89@o673219.ingest.us.sentry.io/4508059881242624',
  integrations: [
    Sentry.httpClientIntegration({
      failedRequestStatusCodes: [[400, 600]], // Capture all status codes between 400 and 600
    }),
    Sentry.browserTracingIntegration({ router }),
    Sentry.replayIntegration(),
    // Send console.log, console.warn, and console.error calls as logs to Sentry
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error", "info", "debug"]
    }),
    // Instrument Supabase client for auth and database operations
    Sentry.supabaseIntegration(supabase, Sentry, {
      tracing: true,
      errors: true,
    }),
  ],
  tunnel: tunnelUrl, // Use the determined tunnel URL
  sendDefaultPii: true, // Enable sending of headers and cookies
  enableLogs: true, // Enable Sentry structured logs
  tracesSampleRate: 1.0,
  tracePropagationTargets: ['localhost', 'sdmizzrivujzvxocsuhw.supabase.co', /\/.*/],
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})

pinia.use(createSentryPiniaPlugin());
app.use(pinia)
app.use(router)
app.mount('#app')

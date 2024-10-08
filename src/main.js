import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import * as Sentry from '@sentry/vue'
import App from './App.vue'
import LandingPage from './pages/LandingPage.vue'
import ProductsPage from './pages/ProductsPage.vue'
import CheckoutPage from './pages/CheckoutPage.vue'
import './global.css' // Import the global CSS file

const routes = [
  { path: '/', component: LandingPage },
  { path: '/products', component: ProductsPage },
  { path: '/checkout', component: CheckoutPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const pinia = createPinia()

const app = createApp(App)

Sentry.init({
  app,
  dsn: import.meta.env.PUBLIC_SENTRY_DSN,
  integrations: [
    Sentry.browserTracingIntegration({ router }),
    Sentry.replayIntegration(),
  ],
  tracesSampleRate: 1.0,
  tracePropagationTargets: ['localhost', /\/.*/],
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})

app.use(pinia)
app.use(router)
app.mount('#app')

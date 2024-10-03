import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import LandingPage from './pages/LandingPage.vue'
import ProductsPage from './pages/ProductsPage.vue'
import CheckoutPage from './pages/CheckoutPage.vue'

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
app.use(pinia)
app.use(router)
app.mount('#app')

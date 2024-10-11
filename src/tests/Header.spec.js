import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import Header from '../components/Header.vue'

// Define the routes as in your main application
const routes = [
  { path: '/', component: { template: '<div>Home</div>' } },
  { path: '/products', component: { template: '<div>Products</div>' } },
  { path: '/checkout', component: { template: '<div>Checkout</div>' } }
]

// Create a mock router with the same routes
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create a Pinia instance
const pinia = createPinia()

test('renders header component', async () => {
  // Mount the component with the router and pinia
  const wrapper = mount(Header, {
    global: {
      plugins: [router, pinia]
    }
  })

  // Wait for the router to be ready
  await router.isReady()

  expect(wrapper.text()).toContain('Pineapple Paradise')
})
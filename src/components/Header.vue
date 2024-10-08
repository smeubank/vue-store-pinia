<template>
  <header>
    <nav class="left-nav">
      <router-link to="/">Home</router-link>
      <router-link to="/products">Products</router-link>
    </nav>
    <h1>Pineapple Paradise</h1>
    <nav class="right-nav">
      <router-link to="/checkout" class="cart-link">
        <i class="fas fa-shopping-cart"></i>
        <span v-if="cartCount > 0" class="cart-count">{{ cartCount }}</span>
      </router-link>
    </nav>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useCartStore } from '../store/cart'

const cartStore = useCartStore()
const cartCount = computed(() => cartStore.items.reduce((total, item) => total + item.quantity, 0))
</script>

<style scoped>
@import '@fortawesome/fontawesome-free/css/all.css';

header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #e0d8b4, #e2dcbb, #e5e0c1, #e8e3c7, #eae7ce, #edead4, #efeedb, #f2f1e1);
  z-index: 10;
}

.left-nav, .right-nav {
  display: flex;
  gap: 1rem;
}

.left-nav {
  margin-left: 1rem;
}

.right-nav {
  margin-right: 1rem;
  position: relative;
}

h1 {
  flex-grow: 1;
  text-align: center;
  margin: 0;
}

nav a {
  color: #333;
  text-decoration: none;
}

.cart-link {
  padding-right: 2rem; /* Increased padding from the right side of the screen */
  position: relative;
}

.cart-count {
  position: absolute;
  top: 0;
  left: 0;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 0.2rem 0.5rem;
  font-size: 0.8rem;
  transform: translate(-50%, -50%);
}
</style>

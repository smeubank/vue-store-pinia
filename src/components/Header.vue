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
      </router-link>
    </nav>
  </header>
</template>

<script setup>
// No additional setup needed for now
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
  background-color: rgba(255, 255, 255, 0.8); /* Slight transparency */
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
}
</style>

<template>
  <header>
    <h1>My Store</h1>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/products">Products</router-link> |
      <router-link to="/checkout">Checkout</router-link>
    </nav>
  </header>
</template>

<script setup>
// No additional setup needed for now
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f0f0f0;
}

nav a {
  margin-left: 1rem;
}
</style>

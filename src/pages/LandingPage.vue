<template>
  <div class="landing-page">
    <div class="hero">
      <h1>Welcome to Pineapple Paradise</h1>
      <p>Explore our amazing pineapple products!</p>
      <router-link to="/products" class="hero-button">View Products</router-link>
    </div>
  </div>
</template>

<script setup>
// You can add any necessary imports or logic here
</script>

<style scoped>
.landing-page {
  position: relative;
  text-align: center;
  color: white;
}

.hero {
  background-image: url('/hero-image.jpg'); /* Update with actual path */
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2); /* Adjusted tint opacity */
  z-index: -1;
}

.hero-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #ffcc00;
  color: #333;
  text-decoration: none;
  border-radius: 5px;
  z-index: 2;
}
</style>

<template>
  <div class="landing-page">
    <h1>Welcome to My Store</h1>
    <img src="/hero-image.jpg" alt="Hero Image" class="hero-image">
    <div class="navigation-card">
      <router-link to="/products">
        <h2>Explore Our Products</h2>
        <p>Find amazing deals on our wide range of products!</p>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.landing-page {
  text-align: center;
}

.hero-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 2rem;
}

.navigation-card {
  border: 1px solid #ddd;
  padding: 1rem;
  max-width: 400px;
  margin: 0 auto;
}

.navigation-card a {
  text-decoration: none;
  color: #333;
}
</style>

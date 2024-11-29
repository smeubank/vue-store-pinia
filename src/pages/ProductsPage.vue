<template>
  <div class="products-page">
    <div class="product-grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'

const products = ref([])

onMounted(async () => {
  const baseUrl = 'https://vue-store-pinia.onrender.com';
  // const baseUrl = 'http://localhost:8000';
  const response = await fetch(`${baseUrl}/products`);
  const data = await response.json();
  products.value = data.map(product => ({
    ...product,
    image: `${baseUrl}/static/images/products/${product.image}`
  }));
});
</script>

<style scoped>
.products-page {
  padding: 1rem;
  padding-top: 5rem;
  position: relative;
  z-index: 1;
  background: radial-gradient(
    circle at center,
    rgba(88, 236, 13, 0.1) 0%,
    transparent 70%
  );
  min-height: calc(100vh - 6rem);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  position: relative;
  z-index: 2;
}
</style>

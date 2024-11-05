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
  padding-top: 5rem; /* Add top padding to move cards lower */
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
</style>

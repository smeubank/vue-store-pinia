<template>
  <div class="products-page">
    <h2>Our Products</h2>
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
import { ref } from 'vue'
import ProductCard from '../components/ProductCard.vue'

// Sample product data
const products = ref([
  { id: 1, name: 'Product 1', price: '$19.99' },
  { id: 2, name: 'Product 2', price: '$29.99' },
  { id: 3, name: 'Product 3', price: '$39.99' },
  { id: 4, name: 'Product 4', price: '$49.99' },
  { id: 5, name: 'Product 5', price: '$59.99' },
  { id: 6, name: 'Product 6', price: '$69.99' },
  { id: 7, name: 'Product 7', price: '$79.99' },
  { id: 8, name: 'Product 8', price: '$89.99' }
])
</script>

<style scoped>
.products-page {
  padding: 1rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
</style>

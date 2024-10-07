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
import { ref } from 'vue'
import ProductCard from '../components/ProductCard.vue'

// Sample product data with image paths
const products = ref([
  { id: 1, name: 'Whole Pineapple', price: '$19.99', image: '/pineapple.jpg' },
  { id: 2, name: 'Canned Pineapple', price: '$29.99', image: '/canned-pineapple.jpg' },
  { id: 3, name: 'Pineapple Juice', price: '$39.99', image: '/pineapple-juice.jpg' },
  { id: 4, name: 'Pineapple Sauce', price: '$49.99', image: '/pineapple-sauce.jpg' },
  { id: 5, name: 'Sliced Pineapple', price: '$59.99', image: '/sliced-pineapple.jpg' },
  { id: 6, name: 'Pineapple Bar Soap', price: '$69.99', image: '/pineapple-bar-soap.jpg' },
  { id: 7, name: 'Pineapple State Flag', price: '$79.99', image: '/pineapple-state-flag.jpg' },
  { id: 8, name: 'Pineapple Hat', price: '$89.99', image: '/pineapple-hat.jpg' }
])
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

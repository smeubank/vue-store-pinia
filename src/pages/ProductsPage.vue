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
  const response = await fetch('http://localhost:8000/products')
  const data = await response.json()
  products.value = data.map(product => ({
    ...product,
    image: `http://localhost:8000/static/images/products/${product.image}`
  }))
})
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

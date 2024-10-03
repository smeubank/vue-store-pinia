<template>
  <div class="product-card">
    <h3>{{ product.name }}</h3>
    <p>{{ product.price }}</p>
    <button @click="addToCart">Add to Cart</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useCartStore } from '../store/cart'

const props = defineProps(['product'])
const cartStore = useCartStore()

function addToCart() {
  cartStore.addItem(props.product)
}
</script>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: center;
}
</style>

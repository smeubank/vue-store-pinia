<template>
  <div class="product-card">
    <h3>{{ product.name }}</h3>
    <p>{{ product.price }}</p>
    <button @click="addToCart" class="add-to-cart">Add to Cart</button>
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
  position: relative;
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: center;
  background-image: url('/path/to/product-image.jpg'); /* Update with actual path */
  background-size: cover;
  background-position: center;
  height: 200px;
  color: white;
}

.add-to-cart {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffcc00;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}
</style>

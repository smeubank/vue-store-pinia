<template>
  <div class="product-card">
    <h3>{{ product.name }}</h3>
    <img :src="product.image" :alt="product.name" class="product-image" />
    <div class="product-info">
      <p>{{ product.price }}</p>
      <button @click="addToCart" class="add-to-cart">Add to Cart</button>
    </div>
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
  background-size: cover;
  background-position: center;
  height: 350px; /* Adjusted height to accommodate image and text */
  color: black;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-image {
  width: 100%;
  height: 150px; /* Adjust height as needed */
  object-fit: contain; /* Ensures the image fits within the designated space */
  margin-bottom: 1rem;
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.add-to-cart {
  background-color: #ffcc00;
  color: #333;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 0.5rem; /* Add some space between price and button */
}
</style>

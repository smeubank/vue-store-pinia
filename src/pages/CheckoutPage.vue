<template>
  <div class="checkout-page">
    <h2>Checkout</h2>
    <div v-if="cartItems.length === 0">
      Your cart is empty.
    </div>
    <div v-else>
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <h3>{{ item.name }}</h3>
        <p>Price: {{ item.price }}</p>
        <p>Quantity: {{ item.quantity }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const { items: cartItems } = storeToRefs(cartStore)
</script>

<style scoped>
.checkout-page {
  padding: 1rem;
}

.cart-item {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
}
</style>

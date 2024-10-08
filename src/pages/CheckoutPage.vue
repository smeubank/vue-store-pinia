<template>
  <div class="checkout-page">
    <div v-if="cartItems.length === 0" class="empty-cart-card">
      <p>Your cart is empty. Go back and buy some pineapple stuff!</p>
    </div>
    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.name" class="cart-item-image" />
          <div class="cart-item-details">
            <h3>{{ item.name }}</h3>
            <p>{{ item.quantity }} x {{ item.price }} = ${{ (item.price.replace('$', '') * item.quantity).toFixed(2) }}</p>
          </div>
          <div class="cart-item-controls">
            <button @click="increaseQuantity(item.id)">▲</button>
            <button @click="decreaseQuantity(item.id)">▼</button>
          </div>
        </div>
      </div>
      <div class="cart-summary">
        <h3>Summary</h3>
        <div v-for="item in cartItems" :key="item.id" class="summary-item">
          <p>{{ item.quantity }} x {{ item.name }}: ${{ (item.price.replace('$', '') * item.quantity).toFixed(2) }}</p>
        </div>
        <p class="total">Total: ${{ totalCartValue }}</p>
        <button class="checkout-button">Checkout</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCartStore } from '../store/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const { items: cartItems } = storeToRefs(cartStore)

const totalCartValue = computed(() => {
  return cartItems.value.reduce((total, item) => {
    return total + item.price.replace('$', '') * item.quantity
  }, 0).toFixed(2)
})

function increaseQuantity(itemId) {
  const item = cartStore.items.find(i => i.id === itemId)
  if (item) {
    cartStore.addItem(item)
  }
}

function decreaseQuantity(itemId) {
  const item = cartStore.items.find(i => i.id === itemId)
  if (item && item.quantity > 1) {
    item.quantity -= 1
  } else {
    cartStore.removeItem(itemId)
  }
}
</script>

<style scoped>
.checkout-page {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  padding-top: 5rem; /* Add top padding to create space from the header */
}

.empty-cart-card {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ddd;
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.cart-content {
  display: flex;
  width: 100%;
}

.cart-items {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
}

.cart-item-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 1rem;
}

.cart-item-details {
  flex: 1;
}

.cart-item-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cart-summary {
  flex: 1;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-left: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.summary-item {
  margin-bottom: 0.5rem;
}

.total {
  font-weight: bold;
  margin-top: 1rem;
}

.checkout-button {
  background-color: #ffcc00;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
}
</style>

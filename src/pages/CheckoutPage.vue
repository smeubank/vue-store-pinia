<template>
  <div class="checkout-page">
    <h2>Checkout</h2>
    <div v-if="cartItems.length === 0">
      Your cart is empty.
    </div>
    <div v-else>
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <img :src="item.image" :alt="item.name" class="cart-item-image" />
        <div class="cart-item-details">
          <h3>{{ item.name }}</h3>
          <p>Total: ${{ (item.price.replace('$', '') * item.quantity).toFixed(2) }}</p>
        </div>
        <div class="cart-item-controls">
          <button @click="increaseQuantity(item.id)">▲</button>
          <button @click="decreaseQuantity(item.id)">▼</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import { storeToRefs } from 'pinia'

const cartStore = useCartStore()
const { items: cartItems } = storeToRefs(cartStore)

function increaseQuantity(itemId) {
  const item = cartStore.items.find(i => i.id === itemId)
  if (item) {
    cartStore.addItem(item)
  } else {
    // Introduce an error by trying to access a property of undefined
    console.log(item.undefinedProperty)
  }
}

function decreaseQuantity(itemId) {
  const item = cartStore.items.find(i => i.id === itemId)
  if (item && item.quantity > 1) {
    item.quantity -= 1
  } else {
    cartStore.removeItem(itemId)
    // Introduce an error by trying to access a property of undefined
    console.log(item.undefinedProperty)
  }
}
</script>

<style scoped>
.checkout-page {
  padding: 1rem;
}

.cart-item {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #e0d8b4, #e2dcbb, #e5e0c1, #e8e3c7, #eae7ce, #edead4, #efeedb, #f2f1e1);
}

.cart-item-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
  margin-right: 1rem;
}

.cart-item-details {
  flex-grow: 1;
}

.cart-item-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cart-item-controls button {
  background-color: #ffcc00;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}
</style>

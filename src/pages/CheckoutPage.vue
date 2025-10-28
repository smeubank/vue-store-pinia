<template>
  <div class="checkout-page">
    <div v-if="errorMessage" class="error-card">
      <img src="/pineapple-paradise-logo.png" alt="Pineapple Logo" class="logo" />
      <p>{{ errorMessage }}</p>
    </div>
    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.name" class="cart-item-image" />
          <div class="cart-item-details">
            <h3>{{ item.name }}</h3>
            <p>{{ item.quantity }} x ${{ parseFloat(item.price).toFixed(2) }} = ${{ (parseFloat(item.price) * item.quantity).toFixed(2) }}</p>
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
          <p>{{ item.quantity }} x {{ item.name }}: ${{ (parseFloat(item.price) * item.quantity).toFixed(2) }}</p>
        </div>
        <p class="total">Total: ${{ totalCartValue }}</p>
        <button class="checkout-button" @click="handleCheckout" :disabled="isCheckingOut">
          {{ isCheckingOut ? 'Processing...' : 'Checkout' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useCartStore } from '../store/cart'
import { storeToRefs } from 'pinia'
import * as Sentry from '@sentry/vue'
import { supabase } from '../main'

const cartStore = useCartStore()
const { items: cartItems } = storeToRefs(cartStore)
const errorMessage = ref('')
const isCheckingOut = ref(false)

onMounted(async () => {
  try {
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const productsResponse = await fetch(`${baseUrl}/products`);
    if (!productsResponse.ok) {
      throw new Error('Failed to fetch products');
    }
    const products = await productsResponse.json();

    const enrichedCartItems = cartItems.value.map(cartItem => {
      const product = products.find(p => p.id === cartItem.id);
      if (!product) {
        console.warn(`Product with ID ${cartItem.id} not found`);
        return cartItem;
      }
      return {
        ...cartItem,
        name: product.name,
        price: product.price, // Keep as number
        image: product.image
      };
    });

    cartStore.setItems(enrichedCartItems);
    console.log('Cart items enriched with product data:', enrichedCartItems);
  } catch (error) {
    errorMessage.value = "Since this website is a joke, the backend will shutdown due to inactivity. Reload this page in 60 seconds to enjoy pineapple goodness.";
  }
})

const totalCartValue = computed(() => {
  return cartItems.value.reduce((total, item) => {
    return total + parseFloat(item.price) * item.quantity
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

async function handleCheckout() {
  if (isCheckingOut.value) return
  
  isCheckingOut.value = true
  
  try {
    // Get current user or generate anonymous UUID
    const { data: { user } } = await supabase.auth.getUser()
    // Generate a consistent anonymous user ID (could be stored in localStorage for repeat visits)
    const userId = user?.id || crypto.randomUUID()
    
    console.log('Starting checkout process', { userId, itemCount: cartItems.value.length })
    Sentry.logger.info('Starting checkout process', { 
      userId, 
      itemCount: cartItems.value.length,
      totalValue: totalCartValue.value 
    })
    
    // Transform cart items to order items format
    const orderItems = cartItems.value.map(item => ({
      product_id: item.id,
      quantity: item.quantity,
      price_at_purchase: parseFloat(item.price)
    }))
    
    const orderData = {
      user_id: userId,
      items: orderItems
    }
    
    console.log('Submitting order to API', orderData)
    Sentry.logger.info('Submitting order to API', { orderData })
    
    // Call the FastAPI backend which will call the Edge Function
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${baseUrl}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to create order')
    }
    
    const result = await response.json()
    const orderId = result.order?.id
    
    console.log('✅ Order created successfully!', { orderId })
    Sentry.logger.info(Sentry.logger.fmt`Order created successfully! Order ID: ${orderId}`, { 
      orderId,
      userId,
      totalValue: totalCartValue.value,
      itemCount: cartItems.value.length
    })
    
    // Clear the cart
    cartStore.setItems([])
    
    // Show success message
    alert(`🎉 Order created successfully!\n\nOrder ID: ${orderId}\n\nCheck Sentry to see the distributed trace across:\n- Vue Frontend\n- FastAPI Backend\n- Supabase Edge Function\n- Supabase Database`)
    
  } catch (error) {
    console.error('❌ Checkout failed:', error.message)
    Sentry.logger.error(Sentry.logger.fmt`Checkout failed: ${error.message}`, { 
      error: error.message,
      stack: error.stack
    })
    Sentry.captureException(error)
    
    alert(`❌ Checkout failed: ${error.message}\n\nPlease make sure:\n1. The backend is running\n2. The Edge Function is deployed\n3. Check the console for details`)
  } finally {
    isCheckingOut.value = false
  }
}
</script>

<style scoped>
.checkout-page {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  padding-top: 5rem;
  position: relative;
  z-index: 1;
  background: radial-gradient(
    circle at center,
    rgba(88, 236, 13, 0.1) 0%,
    transparent 70%
  );
  min-height: calc(100vh - 6rem);
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
  position: relative;
  z-index: 2;
  align-items: flex-start;
  min-height: calc(100vh - 7rem);
}

.cart-items {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: calc(100vh - 7rem);
  overflow-y: auto;
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
  max-height: fit-content;
  align-self: flex-start;
  position: sticky;
  top: 6rem;
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

.checkout-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.logo {
  width: 50px;
  height: 50px;
}
</style>

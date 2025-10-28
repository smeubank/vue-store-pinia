<template>
  <header>
    <nav class="left-nav">
      <router-link to="/">Home</router-link>
      <router-link to="/products">Products</router-link>
    </nav>
    <h1>Pineapple Paradise</h1>
    <nav class="right-nav">
      <!-- Auth Section -->
      <div v-if="!loading" class="auth-section">
        <div v-if="user" class="user-info">
          <img v-if="user.user_metadata?.avatar_url" 
               :src="user.user_metadata.avatar_url" 
               :alt="user.user_metadata?.full_name || user.email"
               class="user-avatar" />
          <span class="user-name">{{ user.user_metadata?.full_name || user.email }}</span>
          <button @click="handleSignOut" class="sign-out-btn">Sign Out</button>
        </div>
        <button v-else @click="handleSignIn" class="sign-in-btn">
          <i class="fab fa-google"></i> Sign In with Google
        </button>
      </div>
      
      <!-- Cart Icon -->
      <router-link to="/checkout" class="cart-link">
        <i class="fas fa-shopping-cart"></i>
        <span v-if="cartCount > 0" class="cart-count">{{ cartCount }}</span>
      </router-link>
    </nav>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useCartStore } from '../store/cart'
import { useAuth } from '../composables/useAuth'

const cartStore = useCartStore()
const cartCount = computed(() => cartStore.items.reduce((total, item) => total + item.quantity, 0))

const { user, loading, signInWithGoogle, signOut } = useAuth()

const handleSignIn = async () => {
  try {
    await signInWithGoogle()
  } catch (error) {
    console.error('Sign in failed:', error)
    alert('Failed to sign in. Please try again.')
  }
}

const handleSignOut = async () => {
  try {
    await signOut()
  } catch (error) {
    console.error('Sign out failed:', error)
    alert('Failed to sign out. Please try again.')
  }
}
</script>

<style scoped>
@import '@fortawesome/fontawesome-free/css/all.css';

header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #e0d8b4, #e2dcbb, #e5e0c1, #e8e3c7, #eae7ce, #edead4, #efeedb, #f2f1e1);
  z-index: 10;
}

.left-nav, .right-nav {
  display: flex;
  gap: 1rem;
}

.left-nav {
  margin-left: 1rem;
}

.right-nav {
  margin-right: 1rem;
  position: relative;
}

h1 {
  flex-grow: 1;
  text-align: center;
  margin: 0;
}

nav a {
  color: #333;
  text-decoration: none;
}

.cart-link {
  padding-right: 2rem; /* Increased padding from the right side of the screen */
  position: relative;
}

.cart-count {
  position: absolute;
  top: 0;
  left: 0;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 0.2rem 0.5rem;
  font-size: 0.8rem;
  transform: translate(-50%, -50%);
}

/* Auth Styles */
.auth-section {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #333;
}

.user-name {
  font-size: 0.9rem;
  color: #333;
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sign-in-btn,
.sign-out-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.sign-in-btn {
  background-color: #4285f4;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sign-in-btn:hover {
  background-color: #357ae8;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.sign-out-btn {
  background-color: #f44336;
  color: white;
}

.sign-out-btn:hover {
  background-color: #d32f2f;
}
</style>

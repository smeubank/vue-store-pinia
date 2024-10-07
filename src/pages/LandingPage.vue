<template>
  <div class="landing-page">
    <div class="hero">
      <h1>Welcome to Pineapple Paradise</h1>
      <p>Explore our amazing pineapple products!</p>
      <router-link to="/products" class="hero-button">View Products</router-link>
    </div>
    <button @click="throwError" class="error-button">Simulate Error</button>
    <div v-if="showErrorModal" class="error-modal">
      <p>Oh no, there is an error! Would be nice if you had Sentry.</p>
      <button @click="closeModal">Close</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showErrorModal = ref(false)

function throwError() {
  // Throw an unhandled error
  throw new Error('Simulated unhandled error for Sentry demonstration')
}

function closeModal() {
  showErrorModal.value = false
}
</script>

<style scoped>
.landing-page {
  position: relative;
  text-align: center;
  color: white;
}

.hero {
  margin-top: 5rem; /* Add top margin to create space below the header */
  background-image: url('/hero-image.jpg'); /* Update with actual path */
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2); /* Adjusted tint opacity */
  z-index: -1;
}

.hero-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #ffcc00;
  color: #333;
  text-decoration: none;
  border-radius: 5px;
  z-index: 2;
}

.error-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #ff0000;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-image: url('/error-modal.png'); /* Update with actual path */
  background-size: cover;
  background-position: center;
  padding: 2rem;
  border: 1px solid #ddd;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  color: white; /* Ensure text is readable on the background */
}
</style>

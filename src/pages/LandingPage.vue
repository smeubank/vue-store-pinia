<template>
  <div class="landing-page">
    <div class="grid-container">
      <div class="card card-1">
        <img src="/pineapple-paradise-logo.png" alt="Pineapple Paradise Logo" class="logo" />
        <h2>Welcome to Paradise</h2>
      </div>
      <router-link to="/products" class="card card-2">
        <h3>View our products</h3>
      </router-link>
      <div class="card card-3" @click="throwError">
        <h3>Throw Error</h3>
      </div>
      <div class="card card-4" @click="simulateError">
        <h3>Simulate Error</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showErrorModal = ref(false)

function throwError() {
  throw new Error('Simulated unhandled error for Sentry demonstration')
}

function simulateError() {
  showErrorModal.value = true
}

function closeModal() {
  showErrorModal.value = false
}
</script>

<style scoped>
.landing-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 1rem;
  box-sizing: border-box;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: 1rem; /* Ensure equal padding between cards */
  justify-content: center; /* Center the grid horizontally */
  align-items: center; /* Center the grid vertically */
  height: 100vh; /* Make sure the grid fits within the viewport */
  width: 100vw; /* Ensure the grid takes the full width of the viewport */
  box-sizing: border-box; /* Include padding and border in the element's total width and height */
  padding: 1rem; /* Add padding around the grid */
}

.card {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  cursor: pointer;
  padding: 1rem; /* Ensure equal padding inside each card */
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Add a larger shadow on hover */
  transition: box-shadow 0.3s ease; /* Smooth transition for the shadow */
}

.card-1 {
  grid-area: 1 / 1 / 3 / 4; /* Corresponds to .div1 */
  margin-top: 3rem; /* Add padding above the first card */
  background: linear-gradient(135deg, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4);
  transition: background 0.3s ease; /* Smooth transition for hover effect */
  height: 350px; /* Set a fixed height to maintain the card size */
}

.card-1:hover {
  background: linear-gradient(135deg, #e0d8b4, #e2d9bc, #e4dbc3, #e7deca, #e9e1d1, #ece4d8, #efe8df, #f2ece6);
}

.card-2 {
  grid-area: 3 / 1 / 5 / 3; /* Corresponds to .div2 */
  background-color: #58ec0d; /* Set the initial color */
  transition: background 0.3s ease; /* Smooth transition for hover effect */
}

.card-2:hover {
  background: linear-gradient(135deg, #58ec0d, #87e800, #a5e427, #bae049, #cadd68, #d5da84, #ddd99d, #e0d8b4);
}

.card-3 {
  grid-area: 3 / 3 / 4 / 4; /* Corresponds to .div3 */
}

.card-4 {
  grid-area: 4 / 3 / 5 / 4; /* Corresponds to .div4 */
}

.logo {
  max-width: 10%; /* Adjust the size as needed */
  height: auto;
  border-radius: 50%; /* Make the image oval */
  object-fit: cover; /* Ensure the image covers the area */
  aspect-ratio: 1 / 1; /* Maintain a square aspect ratio for the oval effect */
}
</style>

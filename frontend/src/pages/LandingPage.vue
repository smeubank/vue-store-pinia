<template>
  <div class="landing-page">
    <div class="flex-container">
      <a href="https://docs.sentry.io/platforms/javascript/guides/vue/" target="_blank" class="card card-1">
        <img src="/pineapple-paradise-logo.png" alt="Pineapple Paradise Logo" class="logo" />
        <h2>Welcome to Paradise</h2>
        <p>This website is a demo of a few things:</p>
        <ul>
          <li>My poor taste in UI design - gradients everywhere</li>
          <li>How to use <a href="https://pinia.vuejs.org/" target="_blank">Pinia</a> for managing state in a Vue.js store</li>
          <li>How you can use <a href="https://docs.sentry.io/platforms/javascript/guides/vue/" target="_blank">Sentry's Vue SDK</a> and Pinia integrations for error monitoring and tracing to get performance insights.</li>
        </ul>
      </a>
      <div class="row">
        <router-link to="/products" class="card card-2">
          <h3>View our products <span class="icon">🔗</span></h3>
        </router-link>
        <div class="card card-3" @click="throwError">
          <h3>Throw Error</h3>
        </div>
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
@import url('https://fonts.googleapis.com/css2?family=Papyrus&display=swap');

.landing-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 1rem;
  box-sizing: border-box;
  font-family: 'Papyrus', sans-serif; /* Apply Papyrus font */
}

.flex-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 600px; /* Match the width of card 1 */
}

.row {
  display: flex;
  justify-content: space-between; /* Align cards to the edges */
  gap: 1rem;
  width: 100%;
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  cursor: pointer;
  padding: 1rem;
  transition: box-shadow 0.3s ease, background 0.3s ease;
  text-decoration: none; /* Remove underline from links */
  color: inherit; /* Inherit text color */
}

.card-1 {
  background: linear-gradient(135deg, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4, #e0d8b4);
  transition: background 0.3s ease;
  width: 100%; /* Full width of the container */
  max-width: 600px; /* Adjust as needed */
  height: auto; /* Adjust height to fit content */
  padding: 2rem; /* Add padding for better spacing */
}

.card-1:hover {
  background: linear-gradient(135deg, #e0d8b4, #d7c6a1, #cfb48f, #c7a180, #be8f72, #b57c67, #ac6a5e, #a15857);
}

.card-2 {
  background-color: #be9d61; /* Default color for card 2 */
  transition: background 0.3s ease;
  flex: 1; /* Make both cards equal size */
  height: 150px; /* Adjust as needed */
  text-decoration: none; /* Remove hyperlink appearance */
  color: inherit; /* Inherit text color from parent */
}

.card-2:hover {
  background: linear-gradient(135deg, #58ec0d, #87e800, #a5e427, #bae049, #cadd68, #d5da84, #ddd99d, #e0d8b4);
}

.card-3 {
  background-color: #5d7f7a; /* Standard color for card 3 */
  transition: background 0.3s ease;
  flex: 1; /* Make both cards equal size */
  height: 150px; /* Adjust as needed */
}

.card-3:hover {
  background: linear-gradient(135deg, #492471, #5e256e, #6f276a, #7e2b66, #8a3261, #943a5d, #9c4459, #a24f56);
}

ul {
  list-style-position: inside; /* Align bullet points and text */
  padding-left: 0; /* Remove default padding */
}

.icon {
  margin-left: 0.5rem; /* Add some space between text and icon */
}

.logo {
  max-width: 10%;
  height: auto;
  border-radius: 50%;
  object-fit: cover;
  aspect-ratio: 1 / 1;
}
</style>
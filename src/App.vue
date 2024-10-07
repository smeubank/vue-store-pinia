<template>
  <div id="app">
    <Header />
    <router-view></router-view>
    <button @click="throwError">Throw error</button>
    <div v-if="showErrorModal" class="error-modal">
      <p>Oh no, there is an error! Would be nice if you had Sentry.</p>
      <button @click="closeModal">Close</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from './components/Header.vue'

const showErrorModal = ref(false)

function throwError() {
  try {
    // Simulate an error
    throw new Error('Simulated error for Sentry demonstration')
  } catch (error) {
    console.error(error)
    showErrorModal.value = true
  }
}

function closeModal() {
  showErrorModal.value = false
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

#error-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 2rem;
  border: 1px solid #ddd;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
</style>

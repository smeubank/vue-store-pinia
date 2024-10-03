<template>
  <div id="app">
    <Header />
    <router-view></router-view>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}
</style>

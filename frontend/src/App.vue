<template>
  <router-view />
</template>

<script setup>

</script>

<style>
html, body {
  overflow-x: hidden; /* Prevent horizontal scroll */
  overflow-y: auto;   /* Allow vertical scroll */
  scrollbar-width: none; /* Firefox */
}

body::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Edge */
}
</style>

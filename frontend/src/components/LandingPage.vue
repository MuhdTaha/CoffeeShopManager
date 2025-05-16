<template>
    <div id="app">
      <router-view/>
      <!-- Header -->
      <header class="header">
        <img :src="logo" alt="Coffee Shop Logo" class="logo" />
        <nav>
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>
  
      <!-- Main Content -->
      <main>
        <div class="hero">
          <h1>Welcome to CaffeineCrew!</h1>
          <p>{{ message }}</p>
          <p></p>
          <div class="cta">
            <button @click="goToLogin">Log In</button>
            <button @click="goToSignup">Sign Up</button>
          </div>
        </div>
      </main>
  
      <!-- Footer -->
      <footer>
        <p>&copy; 2025 CaffeineCrew. All rights reserved.</p>
      </footer>
    </div>
</template>
  
<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import logo from '../assets/logo.png'
import axios from 'axios'
import colors from '../assets/colors.js'

const message = ref('Log in or sign up manage your coffee shop with ease!')
const router = useRouter()

const goToLogin = () => router.push('/login')
const goToSignup = () => router.push('/signup')

onMounted(async () => {
  const root = document.documentElement
  root.style.setProperty('--brown-light', colors.brownLight)
  root.style.setProperty('--brown-main', colors.brownMain)
  root.style.setProperty('--brown-dark', colors.brownDark)
})

</script>
  
<style scoped>
* {
margin: 0;
box-sizing: border-box;
}

html, body {
font-family: 'Arial', sans-serif;
color: var(--brown-dark);
background-color: var(--brown-light);
}

#app {
display: flex;
flex-direction: column;
align-items: center;
justify-content: space-between;
height: 100vh;
color: var(--brown-dark);
background-color: var(--brown-light);
}

.header {
background-color: var(--brown-light);
width: 100%;
padding: 20px 30px;
display: flex;
justify-content: space-between;
align-items: center;
color: var(--brown-dark);
font-size: large;
}

.header img.logo {
width: 100px;
height: auto;
}

nav ul {
display: flex;
list-style: none;
}

nav ul li {
margin-left: 20px;
}

nav ul li a {
color: var(--brown-dark);
text-decoration: none;
font-weight: bold;
}

.hero {
text-align: center;
padding: 50px 20px;
}

.hero h1 {
font-size: 4em;
margin-bottom: 20px;
}

.hero h2 {
font-size: 1.5m;
margin-bottom: 10px;
}

.hero p {
font-size: 1.3em;
margin-bottom: 30px;
}

.cta button {
background-color: var(--brown-dark);
color: white;
font-size: 1.3em;
padding: 10px 20px;
border: none;
margin: 10px;
border-radius: 8px;
cursor: pointer;
}

.cta button:hover {
background-color: var(--brown-main);
transition: background-color 0.3s ease;
color: var(--brown-dark);
}

footer {
text-align: center;
padding: 10px 20px;;
color: var(--brown-dark);
width: 100%;
}
</style>

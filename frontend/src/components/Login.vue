<template>
  <div>
    <!-- Header -->
    <header class="header">
      <img :src="logo" alt="Coffee Shop Logo" class="logo" />
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <!-- Login Form Section -->
    <div class="page-background">
      <div class="form-container">    
        <h2>LOGIN</h2>
        <form @submit.prevent="handleLogin">
          <label for="email">Email</label>
          <input type="email" v-model="email" required />

          <label for="password">Password</label>
          <input type="password" v-model="password" required />

          <button type="submit">Log In</button>
        </form>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <p class="signup-link">
          Don't have an account? <a href="/signup">Sign up now</a>
        </p>

        <button class="home-button" @click="goHome">Back to Home</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import logo from '../assets/logo.png'
import { useRouter } from 'vue-router'
import colors from '../assets/colors.js'
import axios from 'axios'

onMounted(async () => {
  const root = document.documentElement
  root.style.setProperty('--brown-light', colors.brownLight)
  root.style.setProperty('--brown-main', colors.brownMain)
  root.style.setProperty('--brown-dark', colors.brownDark)
})

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

async function handleLogin() {
  try {
    errorMessage.value = '' // Clear previous error message
    
    const response = await axios.post('http://127.0.0.1:5000/login', {
      email: email.value,
      password: password.value
    })
    
    // If we get here, the request was successful (status 200)
    console.log('Login successful:', response.data)
    
    // Store the token in localStorage
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('user', JSON.stringify(response.data.user))

    const role = response.data.user.role

    // Navigate based on role
    if (role === 'manager') {
      router.push('/manager-dashboard')
    } else if (role === 'barista') {
      router.push('/barista-dashboard')
    } else {
      errorMessage.value = 'Unrecognized user role. Access denied.'
    }
  } catch (error) {
    console.error('Error during login:', error)
    
    if (error.response) {
      // The server responded with an error status
      console.log('Server error:', error.response.data)
      errorMessage.value = error.response.data.error || 'Login failed. Please check your credentials.'
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage.value = 'No response from server. Please check your connection.'
    } else {
      // Something happened in setting up the request
      errorMessage.value = 'An error occurred during login. Please try again.'
    }
  }
}

function goHome() {
  router.push('/')
}

</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page-background {
  background-color: var(--brown-light);
  min-height: calc(100vh - 100px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  padding-top: 1.2rem;
  padding-bottom: 1rem;
  padding-left: 4rem;
  padding-right: 5rem; 
  width: fit-content;
  max-width: fit-content;
  background-color: var(--brown-dark);
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.header {
  background-color: var(--brown-light);
  width: 100%;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
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

nav ul li a:hover {
  color: var(--brown-main);
}

h2 {
  color: var(--brown-light);
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

p {
  color: var(--brown-light);
  font-size: 1rem;
}

.error-message {
  color: #ff6b6b;
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
}

a {
  color: white;
  text-decoration: underline;
}

a:hover {
  color: var(--brown-light);
  text-decoration: underline;
  text-decoration-color: var(--brown-main);
  transition: color 0.3s ease;
}

label {
  display: block;
  margin: 0.7rem 0;
  color: var(--brown-light);
}

input {
  width: 100%;
  padding: 0.7rem;
  margin-bottom: 1rem;
  border: 1px solid var(--brown-main);
  background-color: var(--brown-light);
  border-radius: 5px;
}

button {
  padding: 0.8rem 1.5rem;
  margin-top: 1.5rem;
  background-color: var(--brown-main);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: var(--brown-light);
  color: var(--brown-dark);
  transition: background-color 0.3s ease;
}

.home-button {
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: transparent;
  border: 2px solid var(--brown-main);
  color: var(--brown-light);
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.home-button:hover {
  background-color: var(--brown-main);
  color: white;
}
</style>
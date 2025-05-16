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

    <!-- Signup Form Section -->
    <div class="page-background">
    <div class="form-container">
      <h2>SIGN UP</h2>
      <form @submit.prevent="handleSignup">
        <!-- Row 1: Name + Email -->
        <div class="form-row">
          <div class="form-field">
            <label for="name">Name</label>
            <input type="text" v-model="name" required />
          </div>
          <div class="form-field">
            <label for="email">Email</label>
            <input type="email" v-model="email" required />
          </div>
        </div>

        <!-- Row 2: Password + SSN -->
        <div class="form-row">
          <div class="form-field">
            <label for="password">Password</label>
            <input type="password" v-model="password" required />
          </div>
          <div class="form-field">
            <label for="ssn">SSN</label>
            <input type="text" v-model="ssn" required maxlength="11" placeholder="XXX-XX-XXXX" />
          </div>
        </div>

        <!-- Employee Type -->
        <div class="employee-type">
          <label for="employeeType">Employee Type</label>
          <select v-model="employeeType" required>
            <option value="">Select type</option>
            <option value="manager">Manager</option>
            <option value="barista">Barista</option>
          </select>
        </div>

        <button type="submit">Sign Up</button>

        <p class="login-link">
          Already have an account? <a href="/login">Log in</a>
        </p>

        <button class="home-button" @click="goHome">Back to Home</button>
      </form>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import logo from '../assets/logo.png'
import colors from '../assets/colors.js'

const router = useRouter()

const name = ref('')
const email = ref('')
const ssn = ref('')
const password = ref('')
const employeeType = ref('')

onMounted(() => {
  const root = document.documentElement
  root.style.setProperty('--brown-light', colors.brownLight)
  root.style.setProperty('--brown-main', colors.brownMain)
  root.style.setProperty('--brown-dark', colors.brownDark)
})

function handleSignup() {
  console.log('Signup submitted:', {
    name: name.value,
    email: email.value,
    ssn: ssn.value,
    password: password.value,
    employeeType: employeeType.value
  })
  // TODO: Add API call to submit signup data
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
  padding-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  padding: 2rem 3rem;
  width: fit-content;
  background-color: var(--brown-dark);
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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

nav ul li a:hover {
  color: var(--brown-main);

}

h2 {
  color: var(--brown-light);
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
  color: var(--brown-light);
}

input,
select {
  width: 100%;
  padding: 0.7rem;
  margin-top: 0.3rem;
  border: 1px solid var(--brown-main);
  background-color: var(--brown-light);
  border-radius: 5px;
  font-size: 1rem;
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
  color: var(--brown-main);
}

.home-button {
  margin-top: 1rem;
  width: 100%;
  padding: 0.6rem 1.2rem;
  background-color: transparent;
  border: 2px solid var(--brown-main);
  color: var(--brown-light);
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.home-button:hover {
  background-color: var(--brown-main);
  color: white;
}

.login-link {
  color: var(--brown-light);
  margin-top: 1rem;
  text-align: center;
}

.login-link a {
  color: white;
  text-decoration: underline;
}

.login-link a:hover {
  color: var(--brown-light);
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.form-field {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.employee-type {
  text-align: center;
  margin: 1.5rem 0;
}

.employee-type select {
  margin-top: 0.5rem;
  padding: 0.5rem;
  width: 50%;
}

</style>

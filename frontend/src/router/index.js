import { createRouter, createWebHistory } from 'vue-router'

import LandingPage from '../components/LandingPage.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import ManagerDashboard from '../components/ManagerDashboard.vue'
import BaristaDashboard from '../components/BaristaDashboard.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/manager-dashboard', component: ManagerDashboard },
  { path: '/barista-dashboard', component: BaristaDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

<template>
  <div id="app">
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

    <!-- Sidebar + Content (Side-by-Side) -->
    <div class="main-layout">
      <!-- Sidebar -->
      <aside class="sidebar">
        <ul>
          <li
            :class="{ active: currentView === 'employees' }"
            @click="currentView = 'employees'"
          >
            Manage Employees
          </li>
          <li
            :class="{ active: currentView === 'inventory' }"
            @click="currentView = 'inventory'"
          >
            Inventory Management
          </li>
          <li
            :class="{ active: currentView === 'accounting' }"
            @click="currentView = 'accounting'"
          >
            Accounting Reports
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <main class="dashboard-content">
        <h2>Manager Dashboard</h2>
        <h3>Welcome, {{ managerName }}</h3>
        <p>Manage your employees, inventory, and accounting reports.</p>

        <!-- Employees View -->
        <section v-if="currentView === 'employees'">
          <h3>Current Baristas</h3>
          <table>
            <thead>
              <tr>
                <th>SSN</th>
                <th>Name</th>
                <th>Email</th>
                <th>Salary</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="barista in baristas" :key="barista.ssn">
                <td>{{ barista.ssn }}</td>
                <td>{{ barista.name }}</td>
                <td>{{ barista.email }}</td>
                <td>{{ barista.salary }}</td>
                <td>
                  <button class="action-btn" @click="openEditDialog(barista)">Edit</button>
                  <button class="action-btn" @click="openDeleteDialog(barista)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>

          <h3>Add New Employee</h3>
          <div class="form-grid">
            <input v-model="newEmployee.ssn" placeholder="SSN" />
            <input v-model="newEmployee.name" placeholder="Name" />
            <input v-model="newEmployee.email" placeholder="Email" />
            <input v-model="newEmployee.salary" placeholder="Salary" type="number" />
          </div>
          <button @click="addEmployee">Add Employee</button>
        </section>

        <section v-if="currentView === 'inventory'">
          <div class="inventory-container">
          <h3>Current Inventory</h3>
          <table class="inventory-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Unit</th>
                <th>Price per Unit</th>
                <th>Quantity in Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in inventory" :key="item.name">
                <td>{{ item.name }}</td>
                <td>{{ item.unit }}</td>
                <td>${{ item.price.toFixed(2) }}</td>
                <td>{{ item.quantity_in_stock }}</td>
                <td>
                  <button @click="openRefillDialog(item)">Refill</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Refill Dialog -->
          <div v-if="selectedItem" class="modal">
            <div class="modal-content">
              <h3>Refill {{ selectedItem.name }}</h3>
              <label for="refillQty">Quantity to Add:</label>
              <input type="number" v-model.number="refillQuantity" min="1" />
              <div class="modal-actions">
                <button @click="submitRefill">Submit</button>
                <button @click="cancelRefill">Cancel</button>
              </div>
            </div>
          </div>
        </div>
        </section>

        <section v-if="currentView === 'accounting'">
        <h3>Account Balance History</h3>
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in accountingHistory" :key="entry.time_stamp">
              <td>{{ new Date(entry.time_stamp).toLocaleString() }}</td>
              <td>${{ entry.balance.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </section>
      </main>
    </div>
  </div>

  <!-- Edit Dialog -->
  <div v-if="showEditDialog" class="modal">
    <div class="modal-content">
      <h3>Edit Employee</h3>
      <input v-model="editEmployee.name" placeholder="Name" />
      <input v-model="editEmployee.email" placeholder="Email" />
      <input v-model="editEmployee.salary" type="number" placeholder="Salary" />
      <div class="modal-actions">
        <button @click="saveEdit">Save</button>
        <button @click="closeEditDialog">Cancel</button>
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Dialog -->
  <div v-if="showDeleteDialog" class="modal">
    <div class="modal-content">
      <p>Are you sure you want to remove employee {{ deleteEmployee.name }} from the list?</p>
      <div class="modal-actions">
        <button @click="confirmDelete">Yes, Delete</button>
        <button @click="closeDeleteDialog">Cancel</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import logo from '../assets/logo.png'
import colors from '../assets/colors.js'
import axios from 'axios'

const currentView = ref('employees')
const baristas = ref([])
const newEmployee = ref({ ssn: '', name: '', email: '', salary: '' })
const managerName = ref('')

const fetchBaristas = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_baristas')
    baristas.value = response.data
  } catch (error) {
    console.error('Error fetching baristas:', error)
  }
}

const addEmployee = async () => {
  const { ssn, name, email, salary } = newEmployee.value

  if (!ssn || !name || !email || !salary) {
    alert('Please fill in all fields')
    return
  }

  try {
    await axios.post('http://127.0.0.1:5000/add_employee', newEmployee.value)
    await fetchBaristas()
    newEmployee.value = { ssn: '', name: '', email: '', salary: '' }
  } catch (error) {
    console.error('Error adding employee:', error)
  }
}

const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const editEmployee = ref({})
const deleteEmployee = ref({})

const openEditDialog = (employee) => {
  editEmployee.value = { ...employee } // shallow copy
  showEditDialog.value = true
}

const closeEditDialog = () => {
  showEditDialog.value = false
}

const saveEdit = async () => {
  try {
    await axios.put(`http://127.0.0.1:5000/update_employee/${editEmployee.value.ssn}`, editEmployee.value)
    await fetchBaristas()
    closeEditDialog()
  } catch (error) {
    console.error('Error saving edits:', error)
  }
}

const openDeleteDialog = (employee) => {
  deleteEmployee.value = employee
  showDeleteDialog.value = true
}

const closeDeleteDialog = () => {
  showDeleteDialog.value = false
}

const confirmDelete = async () => {
  try {
    await axios.delete(`http://127.0.0.1:5000/delete_employee/${deleteEmployee.value.ssn}`)
    await fetchBaristas()
    closeDeleteDialog()
  } catch (error) {
    console.error('Error deleting employee:', error)
  }
}

const inventory = ref([])
const selectedItem = ref(null)
const refillQuantity = ref(0)

// Fetch inventory data
const fetchInventory = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_inventory')
    inventory.value = response.data
  } catch (error) {
    console.error('Error fetching inventory:', error)
  }
}

// Open refill dialog for selected item
const openRefillDialog = (item) => {
  selectedItem.value = item
  refillQuantity.value = 0
}

// Submit refill to backend
const submitRefill = async () => {
  if (refillQuantity.value <= 0 || isNaN(refillQuantity.value)) {
    alert("Please enter a positive quantity")
    return
  }

  try {
    await axios.post('http://127.0.0.1:5000/refill_inventory', {
      inventory_name: selectedItem.value.name,
      quantity: refillQuantity.value
    })

    await fetchInventory()
    fetchAccountingHistory()
    selectedItem.value = null
    refillQuantity.value = 0
  } catch (error) {
    console.error('Error refilling inventory:', error)
  }
}

// Cancel refill dialog
const cancelRefill = () => {
  selectedItem.value = null
  refillQuantity.value = 0
}

const accountingHistory = ref([])

const fetchAccountingHistory = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/accounting_history')
    accountingHistory.value = response.data
  } catch (error) {
    console.error('Error fetching accounting history:', error)
  }
}


onMounted(() => {
  const root = document.documentElement
  root.style.setProperty('--brown-light', colors.brownLight)
  root.style.setProperty('--brown-main', colors.brownMain)
  root.style.setProperty('--brown-dark', colors.brownDark)

  const user = JSON.parse(localStorage.getItem('user'))
  if (user && user.name) {
    managerName.value = user.name
  }

  fetchBaristas()
  fetchInventory()
  fetchAccountingHistory()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

#app {
  background-color: var(--brown-light);
  min-height: 100vh;
}

.header {
  width: 100%;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--brown-dark);
}

.logo {
  width: 100px;
  height: auto;
}

nav ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
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

.main-layout {
  display: flex;
  flex-direction: row;
  padding: 20px;
  gap: 30px;
}

.sidebar {
  width: 220px;
  padding-top: 1rem;
  flex-shrink: 0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin-top: 5rem;
}

.sidebar li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  color: white;
  background-color: var(--brown-dark);
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.sidebar li:hover {
  background-color: var(--brown-main);
  color: var(--brown-dark);
  transform: translateX(5px);
}

.sidebar li.active {
  background-color: var(--brown-main);
  color: var(--brown-dark);
  font-weight: bold;
  border-left: 5px solid var(--brown-dark);
}

.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

h2 {
  color: var(--brown-dark);
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
}

h3 {
  color: var(--brown-dark);
  margin-top: 1rem;
}

p {
  margin-bottom: 1rem;
  color: var(--brown-dark);
}

table {
  width: auto;
  border-collapse: collapse;
  margin-top: 1rem;
  margin-bottom: 2rem;
}

th, td {
  border: 1px solid var(--brown-dark);
  padding: 10px;
  text-align: center;
}

th {
  background-color: var(--brown-main);
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

input,
select {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid var(--brown-dark);
  background-color: var(--brown-light);
  color: black;
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
  color: var(--brown-dark);
  border: 1px solid var(--brown-dark);
  transition: background-color 0.3s ease;
}

.form-grid {
  display: flex;
  width: 30%;
  gap: 15px;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: var(--brown-light);
  padding: 2rem;
  border-radius: 8px;
  min-width: 300px;
}

.modal-content input {
  margin-bottom: 12px;
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.action-btn, .inventory-table button{
  font-size: 1.1rem;
  padding: 6px 10px;
  margin: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.inventory-table button:hover {
  background-color: var(--brown-light);
  color: var(--brown-dark);
  border: 1px solid var(--brown-dark);
  transition: background-color 0.3s ease;
}
</style>

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

    <!-- Main Layout -->
    <div class="dashboard-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <ul>
          <li
            :class="{ active: currentView === 'createOrder' }"
            @click="currentView = 'createOrder'"
          >
            Create Order
          </li>
          <li
            :class="{ active: currentView === 'pastOrders' }"
            @click="currentView = 'pastOrders'"
          >
            Past Orders
          </li>
        </ul>

        <div class="sidebar-info">
          <p><strong>Balance:</strong> ${{ accountBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</p>
          <p><strong>Inventory:</strong></p>
          <ul>
            <li v-for="(qty, name) in inventory" :key="name">
              {{ name }}: {{ qty }}
            </li>
          </ul>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="main-content">
        <h2>Barista Dashboard</h2>
        <h3>Welcome, {{ baristaName }}</h3>
        <p>Create and manage all your coffee orders seamlessly!</p>

        <!-- Create Order View -->
        <section v-if="currentView === 'createOrder'" class="order-section">
          <div v-if="!orderPlaced">
            <div class="form-row">
              <div class="form-field">
                <label for="drink">Drink</label>
                
                <select v-model="selectedDrink">
                  <option disabled value="">Select a drink</option>
                  <option
                    v-for="drink in availableDrinks"
                    :key="drink.name"
                    :value="drink"
                  >
                    {{ drink.name }} - ${{ drink.price.toFixed(2) }}
                  </option>
                </select>
                
              </div>

              <div class="form-field">
                <label for="quantity">Quantity</label>
                <input type="number" min="1" v-model.number="quantity" />
              </div>

              <button @click="addToOrder">Add to Order</button>
            </div>

            <h4 style="margin-left: 1rem;">Order Summary</h4>
            <ul class="order-list" style="margin-left: 1rem;">
              <li v-for="(item, index) in order" :key="index" style="margin-bottom: 1rem;">
                <strong>{{ item.drink.name }}</strong> ({{ item.drink.type }}, {{ item.drink.temperature }}, {{ item.drink.size }} oz)  
                <br />
                Quantity: {{ item.quantity }}<br />
                Price: ${{ item.drink.price.toFixed(2) }} x {{ item.quantity }} = <strong>${{ (item.drink.price * item.quantity).toFixed(2) }}</strong><br />
              </li>
            </ul>
            <p v-if="order.length" style="margin-left: 1rem;"><strong>Total:</strong> ${{ orderTotal.toFixed(2) }}</p>

            <div class="form-field">
              <label for="payment">Payment Method</label>
              <select v-model="paymentMethod">
                <option disabled value="">Select payment method</option>
                <option>Cash</option>
                <option>Card</option>
              </select>
            </div>

            <button
              class="place-order-btn"
              @click="placeOrder"
              :disabled="!canPlaceOrder"
            >
              Place Order
            </button>
          </div>

          <div v-else>
            <h4>Order Placed!</h4>
            
            <ul>
              <li v-for="(item, index) in lastOrder" :key="index" style="margin-bottom: 1rem;">
                <strong>{{ item.quantity }}x {{ item.drink.name }}</strong><br />
                Type: {{ item.drink.type }}, Size: {{ item.drink.size }} oz, Temp: {{ item.drink.temperature }}<br />
                
                <strong>Instructions:</strong>
                <ul style="margin-left: 1rem;">
                  <li v-for="(step, stepIndex) in item.drink.instructions" :key="stepIndex">{{ step }}</li>
                </ul>

                <strong>Ingredients:</strong>
                <ul style="margin-left: 1rem;">
                  <li v-for="(ing, ingIndex) in item.drink.ingredients" :key="ingIndex">
                    {{ ing.quantity }} {{ ing.unit }} {{ ing.name }}
                  </li>
                </ul>
              </li>
            </ul>
            
            <p><strong>Total Paid:</strong> ${{ lastOrderTotal.toFixed(2) }}</p>
            <button @click="resetOrder">Create New Order</button>
          </div>
        </section>

        <!-- Past Orders View -->
        <section v-if="currentView === 'pastOrders'">
          <p>Past orders will go here.</p>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import logo from '../assets/logo.png'
import colors from '../assets/colors.js'
import axios from 'axios'

const currentView = ref('createOrder')

const inventory = reactive({})
const accountBalance = ref(0)

const fetchInventory = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/inventory')
    Object.assign(inventory, res.data)
  } catch (error) {
    console.error('Failed to load inventory:', error)
  }
}

const fetchAccountBalance = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/account_balance')
    accountBalance.value = res.data.balance
  } catch (error) {
    console.error('Failed to load account balance:', error)
  }
}

const availableDrinks = ref([])

const fetchAvailableDrinks = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/menu')
    availableDrinks.value = res.data
  } catch (error) {
    console.error('Failed to fetch drinks:', error)
  }
}

const baristaName = ref('')

onMounted(() => {
  const root = document.documentElement
  root.style.setProperty('--brown-light', colors.brownLight)
  root.style.setProperty('--brown-main', colors.brownMain)
  root.style.setProperty('--brown-dark', colors.brownDark)

  const user = JSON.parse(localStorage.getItem('user'))
  if (user && user.name) {
    baristaName.value = user.name
  }

  fetchInventory()
  fetchAccountBalance()
  fetchAvailableDrinks()
})

// Order state
const selectedDrink = ref('')
const quantity = ref(1)
const paymentMethod = ref('')
const order = ref([])
const lastOrder = ref([])
const orderPlaced = ref(false)

const orderTotal = computed(() =>
  order.value.reduce((sum, item) => sum + item.drink.price * item.quantity, 0)
)
const lastOrderTotal = computed(() =>
  lastOrder.value.reduce((sum, item) => sum + item.drink.price * item.quantity, 0)
)
const canPlaceOrder = computed(() => order.value.length > 0 && paymentMethod.value)

function addToOrder() {
  if (!selectedDrink.value || quantity.value <= 0) return

  const existingItem = order.value.find(
    item => item.drink.name === selectedDrink.value.name
  )

  if (existingItem) {
    existingItem.quantity += quantity.value
  } else {
    order.value.push({ drink: selectedDrink.value, quantity: quantity.value })
  }

  selectedDrink.value = ''
  quantity.value = 1
}

async function placeOrder() {
  if (!canPlaceOrder.value) return

  try {
    // Map payment method to match database constraints
    let dbPaymentMethod;
    switch(paymentMethod.value) {
      case 'Cash':
        dbPaymentMethod = 'cash';
        break;
      case 'Card':
        dbPaymentMethod = 'card';
        break;
    }

    // Create a new order in the orders table first
    const orderResponse = await axios.post('http://127.0.0.1:5000/api/create_order', {
      payment_method: dbPaymentMethod
    });
    
    const orderId = orderResponse.data.order_id;
    
    // Then add line items to the order
    const lineItems = order.value.map(item => ({
      order_id: orderId,
      menu_name: item.drink.name,
      quantity: item.quantity,
      price: item.drink.price.toString()
    }));
    
    // Add line items to the order
    await axios.post('http://127.0.0.1:5000/api/add_line_items', {
      line_items: lineItems
    });
    
    console.log('Order placed successfully!');
    
    // Save to last order & reset inputs
    lastOrder.value = [...order.value];
    order.value = [];
    paymentMethod.value = '';
    orderPlaced.value = true;
    
    // Refresh inventory and balance data after successful order
    fetchInventory();
    fetchAccountBalance();
  } catch (error) {
    console.error('Failed to place order:', error);
    
    // Show more detailed error information
    if (error.response) {
      // The server responded with a status code outside the 2xx range
      console.error('Error response data:', error.response.data);
      console.error('Error response status:', error.response.status);
      
      // Show the specific error message from the server if available
      if (error.response.data && error.response.data.error) {
        alert(`Order failed: ${error.response.data.error}`);
      } else {
        alert(`Order failed with status ${error.response.status}`);
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Error request:', error.request);
      alert('No response received from server. Please check if the server is running.');
    } else {
      // Something happened in setting up the request
      console.error('Error message:', error.message);
      alert(`Error setting up request: ${error.message}`);
    }
  }
}

function resetOrder() {
  selectedDrink.value = ''
  quantity.value = 1
  order.value = []
  paymentMethod.value = ''
  orderPlaced.value = false
}
</script>


<style scoped>
* {
  box-sizing: border-box;
}

#app {
  background-color: var(--brown-light);
  min-height: 100vh;
}

.dashboard-container {
  display: flex;
  padding: 20px;
}

.main-content {
  flex: 1;
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

h2 {
  color: var(--brown-dark);
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
}

h3, h4 {
  color: var(--brown-dark);
  margin-top: 1rem;
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
  color: var(--brown-dark);
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
  background-color: var(--brown-dark);
  color: var(--brown-light);
}

.sidebar {
  width: 200px;
  margin-right: 30px;
  padding-top: 70px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  margin-top: 1rem;
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

.order-section,
.instructions,
.account-info {
  margin-top: 1rem;
  padding-left: 1rem;
}

.sidebar-info {
  margin-top: 4rem;
  font-size: large;
  font-weight: bold;
  color: var(--brown-dark);
}

.sidebar-info ul {
  list-style: none;
  padding-left: 0;

}

.sidebar-info li {
  margin-top: -1rem;
  color: var(--brown-dark);
  background-color: var(--brown-light);
  border-radius: 5px;
  cursor: text;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.sidebar li:hover {
  background-color: var(--brown-light);
  color: var(--brown-dark);
  transform: translateX(0px);
}

.order-list {
  list-style: none;
  padding-left: 1.5rem;
  margin-top: 0.5rem;
}

.account-info ul {
  list-style: none;
  padding: 100px;
}

.form-row {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  align-items: flex-end;
  max-width: 600px;
}

.form-field {
  flex: 1;
  min-width: 120px;
  max-width: 250px;
}
</style>

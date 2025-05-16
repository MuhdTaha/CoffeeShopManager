# ☕ Coffee Shop Management App

This is a simple full-stack application for managing a coffee shop. Managers can log in to manage employees, inventory and see account history. Baristas can log in to create drink orders for their customers. 

This app is built with:

- Frontend: Vue.js 3
- Backend: Python (Flask)
- Database: PostgreSQL

## 🔧 Prerequisites

- Python 3.8+ 
- Node.js (v18 or later)
- PostgreSQL
- npm
- Vue CLI (for frontend dev server)

## 🗄️ Database Setup

### 1. Create a PostgreSQL database

You can use `pgAdmin` or the command line.

```bash
CREATE DATABASE coffeeshop;
```

### 2. Load the schema and sample data

In a terminal or psql shell:

```bash
psql -U postgres_username -d coffeeshop -f backend/schema.sql
```

## ⚙️ Configure Backend (Flask)

### 1. Install Python Dependencies

```bash
cd backend
npm install
node index.js
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend\requirements.txt
```

### 2. Set Database Configuration

Create a .env file in the backend/ directory:
```bash
touch .env
```

And add your PostgreSQL credentials:

```bash
DB_HOST=localhost
DB_NAME=coffeeshop
DB_USER=postgres_user
DB_PASSWORD=postgres_password
DB_PORT=5432
```

### 3. Run the Flask Server
```bash
python app.py
```
By default, the backend will be accessible at:
http://127.0.0.1:5000/

### 🌐 Configure Frontend (Vue.js)

```bash
cd frontend
npm install
npm run dev
```

This starts the frontend on `http://localhost:5173`.

## 📋 Features

- Employee login (email/password)
- Manage employees (add, update, delete)
- Manage inventory (refill stock, deduct balance)
- Create coffee orders (create order, payment method, instructions, inventory, balance)
- Auth via PostgreSQL users table (no password hashing)

## 📁 SQL Scripts

- `schema.sql`: Creates tables (`employees`, `inventory`, `menu`, etc.) and inserts sample data for testing app functionality

## 🧪 Sample Login

You can use these seeded accounts to test application functionality:

Manager: 
- Email: alice@example.com
- Password: temp123

Barista: 
- Email: bob@example.com
- Password: temp123

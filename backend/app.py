from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import uuid
import os   
from decimal import Decimal

app = Flask(__name__)
active_sessions = {}

CORS(app)

# Database configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )

# Manager Authentication (Login)
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT ssn, name, email, password FROM employees WHERE email = %s', (email,))
        employee = cur.fetchone()

        if not employee:
            cur.close()
            conn.close()
            return jsonify({"error": "Employee not found"}), 404
        
        ssn, name, email_db, password_db = employee

        if password != password_db:
            cur.close()
            conn.close()
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Determine the role of the employee
        cur.execute('SELECT 1 FROM managers WHERE ssn = %s', (ssn,))
        if cur.fetchone():
            role = "manager"
        else:
            cur.execute('SELECT 1 FROM baristas WHERE ssn = %s', (ssn,))
            if cur.fetchone():
                role = "barista"
            else:
                return jsonify({"error": "Role not found"}), 404

        cur.close()
        conn.close()
        
        if employee and employee[3] == password:  # Check password match
            # Generate a session token (using UUID for simplicity)
            session_token = str(uuid.uuid4())
            active_sessions[session_token] = {
                'ssn': ssn,
                'name': name,
                'email': email_db,
                'role': role
            }
            
            return jsonify({
            "message": "Login successful",
            "token": session_token,
            "user": {
                "ssn": ssn,
                "name": name,
                "email": email_db,
                "role": role
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Middleware to verify authentication using session token
def verify_token(token):
    if token in active_sessions:
        return active_sessions[token]
    return None

# Fetch Barista Information
@app.route('/get_baristas', methods=['GET'])
def get_baristas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT e.ssn, e.name, e.email, e.salary 
            FROM employees e 
            JOIN baristas b ON e.ssn = b.ssn
        ''')
        baristas = cur.fetchall()
        cur.close()
        conn.close()

        # Convert to list of dicts
        result = [
            {"ssn": b[0], "name": b[1], "email": b[2], "salary": b[3]}
            for b in baristas
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Manager Dashboard - Manage Employees
@app.route('/add_employee', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        ssn = data.get('ssn')
        name = data.get('name')
        email = data.get('email')
        salary = data.get('salary')
        password = "temp123"  # Temporary password
        
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert into employees table
        cur.execute('INSERT INTO employees (ssn, name, email, salary, password) VALUES (%s, %s, %s, %s, %s)',
                    (ssn, name, email, salary, password))
        
        # Insert into baristas table (assuming ssn is the only required field)
        cur.execute(
            'INSERT INTO baristas (ssn) VALUES (%s)',
            (ssn,)
        )

        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Employee added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/delete_employee/<ssn>', methods=['DELETE'])
def delete_employee(ssn):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Remove from baristas if applicable
        cur.execute('DELETE FROM baristas WHERE ssn = %s', (ssn,))
        
        # Remove from schedule if applicable
        cur.execute('DELETE FROM schedules WHERE ssn = %s', (ssn,))
        
        # Remove from employees
        cur.execute('DELETE FROM employees WHERE ssn = %s', (ssn,))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update_employee/<ssn>', methods=['PUT'])
def update_employee(ssn):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        salary = data.get('salary')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            UPDATE employees 
            SET name = %s, email = %s, salary = %s 
            WHERE ssn = %s
        ''', (name, email, salary, ssn))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Employee updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Manager Dashboard - Manage Inventory
@app.route('/get_inventory', methods=['GET'])
def get_inventory():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name, unit, price, quantity_in_stock FROM inventory ORDER BY name')
        rows = cur.fetchall()
        cur.close()
        conn.close()

        inventory_list = [
            {
                "name": row[0],
                "unit": row[1],
                "price": float(row[2]),
                "quantity_in_stock": float(row[3])
            }
            for row in rows
        ]

        return jsonify(inventory_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Manager Dashboard - Refill Inventory Item
@app.route('/refill_inventory', methods=['POST'])
def refill_inventory():
    try:
        data = request.get_json()
        inventory_name = data['inventory_name']
        quantity = data['quantity']
        
        # Get the current stock and price of the inventory item
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT quantity_in_stock, price FROM inventory WHERE name = %s', (inventory_name,))
        item = cur.fetchone()
        
        if not item:
            return jsonify({"error": "Inventory item not found"}), 404
        
        current_quantity = item[0]
        price = item[1]
        
        # Update the stock quantity and reduce the balance
        new_quantity = current_quantity + quantity
        new_balance = - (price * quantity)  # Negative because it's a cost
        
        # Update inventory stock
        cur.execute('UPDATE inventory SET quantity_in_stock = %s WHERE name = %s', (new_quantity, inventory_name))
        
        # Get the current balance from the accounting table
        cur.execute('SELECT balance FROM accounting ORDER BY time_stamp DESC LIMIT 1')
        current_balance = cur.fetchone()[0]
        
        # Update accounting balance
        updated_balance = current_balance + new_balance
        cur.execute('INSERT INTO accounting (time_stamp, balance) VALUES (NOW(), %s)', (updated_balance,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Inventory refilled and balance updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Manager Dashboard - View Accounting History
@app.route('/accounting_history', methods=['GET'])
def get_accounting_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounting ORDER BY time_stamp DESC")
    rows = cur.fetchall()
    conn.close()
    cur.close()

    history = [
        {'time_stamp': row[0], 'balance': float(row[1])}
        for row in rows
    ]
    return jsonify(history)


# Barista Dashboard - Get Inventory
@app.route('/api/inventory')
def inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, quantity_in_stock, unit FROM inventory')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    inventory = {
        row[0]: f"{round(row[1])} {row[2]}"
        for row in rows
    }

    return jsonify(inventory)

# Barista Dashboard - Get Balance
@app.route('/api/account_balance')
def get_account_balance():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT balance FROM accounting ORDER BY time_stamp DESC LIMIT 1')
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            balance = float(result[0])
        else:
            balance = 0.0

        return jsonify({'balance': balance}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Barista Dashboard - Get Menu Items
@app.route('/api/menu')
def get_menu():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get all menu items
    cur.execute('''
        SELECT m.name, m.size, m.type, m.price, m.temperature, r.recipe_id
        FROM menu m
        JOIN recipe r ON m.name = r.menu_name
    ''')
    menu_items = cur.fetchall()

    menu = []

    for name, size, type_, price, temperature, recipe_id in menu_items:
        # Get preparation steps
        cur.execute('''
            SELECT name FROM preparation_step
            WHERE recipe_id = %s
            ORDER BY position ASC
        ''', (recipe_id,))
        steps = [row[0] for row in cur.fetchall()]
        
        # Get ingredients
        cur.execute('''
            SELECT i.inventory_name, i.quantity, i.unit
            FROM ingredient i
            WHERE i.recipe_id = %s
        ''', (recipe_id,))
        ingredients = [
            {
                'name': row[0],
                'quantity': float(row[1]),
                'unit': row[2]
            }
            for row in cur.fetchall()
        ]

        menu.append({
            'name': name,
            'size': float(size),
            'type': type_,
            'price': float(price),
            'temperature': temperature,
            'instructions': steps,
            'ingredients': ingredients
        })

    cur.close()
    conn.close()

    return jsonify(menu)

# Barista Dashboard - Create Order
@app.route('/api/create_order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        payment_method = data.get('payment_method')
        
        # Validate payment method
        if payment_method not in ['cash', 'card']:
            return jsonify({"error": "Invalid payment method. Must be 'cash' or 'card'"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert new order
        cur.execute(
            'INSERT INTO orders (time_stamp, payment_method) VALUES (NOW(), %s) RETURNING order_id',
            (payment_method,)
        )
        
        order_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Order created", "order_id": order_id}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/add_line_items', methods=['POST'])
def add_line_items():
    try:
        data = request.get_json()
        line_items = data.get('line_items', [])
        
        if not line_items:
            return jsonify({"error": "No line items provided"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        total_amount = 0
        
        # Process each line item
        for item in line_items:
            order_id = item.get('order_id')
            menu_name = item.get('menu_name')
            quantity = item.get('quantity')
            price = item.get('price')
            
            # Validate data
            if not all([order_id, menu_name, quantity, price]):
                return jsonify({"error": "Missing required line item data"}), 400
            
            # Ensure price is treated as a decimal
            price = Decimal(price)  # Convert price to Decimal
            
            # Insert line item
            cur.execute(
                'INSERT INTO lineitem (order_id, menu_name, quantity, price) VALUES (%s, %s, %s, %s)',
                (order_id, menu_name, quantity, price)
            )
            
            # Update inventory (deduct ingredients)
            cur.execute('SELECT recipe_id FROM recipe WHERE menu_name = %s', (menu_name,))
            result = cur.fetchone()
            
            if not result:
                conn.rollback()
                return jsonify({"error": f"Recipe not found for menu item: {menu_name}"}), 404
                
            recipe_id = result[0]
            
            # Get ingredients for this recipe
            cur.execute('SELECT inventory_name, quantity FROM ingredient WHERE recipe_id = %s', (recipe_id,))
            ingredients = cur.fetchall()
            
            # Check and update inventory
            for inv_name, req_quantity in ingredients:
                # Check if enough stock
                cur.execute('SELECT quantity_in_stock FROM inventory WHERE name = %s', (inv_name,))
                stock = cur.fetchone()
                
                if not stock or stock[0] < req_quantity * quantity:
                    conn.rollback()
                    return jsonify({"error": f"Not enough {inv_name} in stock"}), 400
                
                # Update inventory
                cur.execute(
                    'UPDATE inventory SET quantity_in_stock = quantity_in_stock - %s WHERE name = %s',
                    (req_quantity * quantity, inv_name)
                )
            
            # Calculate total amount
            total_amount += price * quantity
        
        # Update accounting balance
        cur.execute('SELECT balance FROM accounting ORDER BY time_stamp DESC LIMIT 1')
        current_balance = cur.fetchone()[0]
        new_balance = current_balance + total_amount
        
        cur.execute('INSERT INTO accounting (time_stamp, balance) VALUES (NOW(), %s)', (new_balance,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Line items added successfully", "total": total_amount}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Running the Flask App
if __name__ == '__main__':
    app.run(debug=True)

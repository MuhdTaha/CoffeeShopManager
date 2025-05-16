-- 
-- Part 1: Employee Management + Accounting
-- employees, managers, baristas, schedules, accounting
-- Muhammad Taha
-- 

-- drop tables if they exist
DROP TABLE IF EXISTS employees, managers, baristas, schedules, accounting, menu, recipe, preparation_step, inventory, ingredient, orders, lineitem, promotions, promotion_items CASCADE;

-- employees table
CREATE TABLE employees (
    ssn CHAR(9) PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    password TEXT NOT NULL DEFAULT 'temp123',
);

-- managers table
CREATE TABLE managers (
    ssn CHAR(9) PRIMARY KEY REFERENCES employees(ssn),
    ownership_percentage NUMERIC(5,2) CHECK (ownership_percentage >= 0 AND ownership_percentage <= 100)
);

-- baristas table
CREATE TABLE baristas (
    ssn CHAR(9) PRIMARY KEY REFERENCES employees(ssn)
);

-- schedules table
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    ssn CHAR(9) REFERENCES baristas(ssn),
    day_of_week TEXT CHECK (day_of_week IN ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- accounting table
CREATE TABLE accounting (
    time_stamp TIMESTAMP PRIMARY KEY,
    balance NUMERIC(12,2) NOT NULL
);

-- indexes
CREATE INDEX idx_employees_email ON employees(email);
CREATE INDEX idx_schedules_day ON schedules(day_of_week);

-- 
-- Testing Data for Part 1
-- 

-- insert sample data into employees
INSERT INTO employees (ssn, name, email, salary, password) VALUES
('123456789', 'Alice Johnson', 'alice@example.com', 50000.00, 'temp123'),
('987654321', 'Bob Smith', 'bob@example.com', 60000.00, 'temp123'),
('555666777', 'Charlie Doe', 'charlie@example.com', 45000.00, 'temp123');

-- insert sample data into managers
INSERT INTO managers (ssn, ownership_percentage) VALUES
('123456789', 25.00);

-- insert sample data into baristas
INSERT INTO baristas (ssn) VALUES
('987654321'),
('555666777');

-- insert sample data into schedules
INSERT INTO schedules (ssn, day_of_week, start_time, end_time) VALUES
('987654321', 'Mon', '08:00:00', '14:00:00'),
('987654321', 'Wed', '10:00:00', '16:00:00'),
('555666777', 'Fri', '09:00:00', '13:00:00');

-- insert sample data into accounting
INSERT INTO accounting (time_stamp, balance) VALUES
(NOW() - INTERVAL '2 days', 15000.00),
(NOW() - INTERVAL '1 day', 14500.00),
(NOW(), 15200.00);

--
-- Part 2: Menu, Recipes, Inventory
-- menu, recipes, prep_steps, ingredients, inventory
-- Hector Salto
--

CREATE TABLE menu (
    name TEXT PRIMARY KEY,
    size NUMERIC(5, 2) NOT NULL,
    type TEXT CHECK (type IN ('tea', 'coffee', 'softdrink')),
    price NUMERIC(6, 2) NOT NULL,
    temperature TEXT CHECK (temperature IN ('hot', 'cold')) NOT NULL
);

CREATE TABLE recipe (
    recipe_id SERIAL PRIMARY KEY,
    menu_name TEXT UNIQUE REFERENCES menu(name)
);

CREATE TABLE preparation_step (
    step_id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(recipe_id),
    position INTEGER NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE inventory (
    name TEXT PRIMARY KEY,
    unit TEXT NOT NULL,
    price NUMERIC(6, 2) NOT NULL,
    quantity_in_stock NUMERIC(10, 2) NOT NULL
);

CREATE TABLE ingredient (
    ingredient_id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipe(recipe_id),
    inventory_name TEXT REFERENCES inventory(name),
    quantity NUMERIC(8, 3) NOT NULL,
    unit TEXT NOT NULL
);

-- Index
CREATE INDEX idx_recipe_menu ON recipe(menu_name);

--
-- Testing Data for Part 2
--

INSERT INTO menu (name, size, type, price, temperature) VALUES
('Espresso', 2.0, 'coffee', 2.50, 'hot'),
('Iced Latte', 12.0, 'coffee', 4.50, 'cold'),
('Black Tea', 8.0, 'tea', 3.00, 'hot'),
('Lemonade', 16.0, 'softdrink', 2.00, 'cold');

INSERT INTO recipe (menu_name) VALUES
('Espresso'),
('Iced Latte'),
('Black Tea'),
('Lemonade');

INSERT INTO preparation_step (recipe_id, position, name) VALUES
(1, 1, 'Grind coffee beans'),
(1, 2, 'Brew under pressure'),
(1, 3, 'Pour into coffee cup'),
(2, 1, 'Brew espresso'),
(2, 2, 'Pour over ice'),
(2, 3, 'Add milk'),
(3, 1, 'Pour hot water into cup'),
(3, 2, 'Steep black tea in hot water'),
(4, 1, 'Squeeze lemon'),
(4, 2, 'Mix with sugar and water'),
(4, 3, 'Pour over ice');

INSERT INTO inventory (name, unit, price, quantity_in_stock) VALUES
('Coffee Beans', 'lb', 10.00, 100.0),
('Milk', 'oz', 0.30, 200.0),
('Sugar', 'oz', 0.05, 500.0),
('Lemon', 'amount', 0.50, 50.0),
('Water', 'oz', 0.01, 1000.0);

INSERT INTO ingredient (recipe_id, inventory_name, quantity, unit) VALUES
(1, 'Coffee Beans', 0.5, 'oz'),
(1, 'Water', 2.0, 'oz'),
(2, 'Coffee Beans', 0.5, 'oz'),
(2, 'Water', 2.0, 'oz'),
(2, 'Milk', 6.0, 'oz'),
(2, 'Sugar', 1.0, 'oz'),
(3, 'Water', 8.0, 'oz'),
(3, 'Sugar', 0.5, 'oz'),
(4, 'Lemon', 1.0, 'amount'),
(4, 'Water', 10.0, 'oz'),
(4, 'Sugar', 2.0, 'oz');

--
-- Part 3: Orders, LineItems + Promotions
-- orders, lineitems, promotion, promotion_items
-- Peter Siegler
--

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    time_stamp TIMESTAMP NOT NULL DEFAULT NOW(),
    payment_method TEXT CHECK (payment_method IN ('cash', 'credit card', 'app')) NOT NULL
);

CREATE TABLE lineitem (
    lineitem_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    menu_name TEXT REFERENCES menu(name),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC(6,2) NOT NULL
);

CREATE TABLE promotions (
    promotion_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    day_of_week TEXT CHECK (day_of_week IN ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE promotion_items (
    promotion_item_id SERIAL PRIMARY KEY,
    promotion_id INTEGER REFERENCES promotions(promotion_id),
    menu_name TEXT REFERENCES menu(name),
    promo_price NUMERIC(6,2) NOT NULL
);

-- Testing Data for Part 3

INSERT INTO orders (time_stamp, payment_method) VALUES
(NOW(), 'cash'),
(NOW() - INTERVAL '1 hour', 'credit card');

INSERT INTO lineitem (order_id, menu_name, quantity, price) VALUES
(1, 'Espresso', 2, 2.50),
(1, 'Black Tea', 1, 3.00),
(2, 'Iced Latte', 1, 4.50);

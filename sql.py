import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="new_username6",
    password="new_password6",
    database="new_database6"
)

# Create a cursor object
cursor = db.cursor()

# Step 1: Drop and Create Database
cursor.execute("DROP DATABASE IF EXISTS new_database6;")
cursor.execute("CREATE DATABASE new_database6;")
cursor.execute("USE new_database6;")

# Step 2: Create Tables
cursor.execute("""
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    phone VARCHAR(15) NOT NULL,
    address VARCHAR(100),
    registration_date DATE
);
""")

cursor.execute("""
CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(50),
    contact_email VARCHAR(50),
    contact_phone VARCHAR(15),
    address VARCHAR(100)
);
""")

cursor.execute("""
CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(50),
    category_id INT,
    price DECIMAL(10, 2),
    stock_quantity INT,
    supplier_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
""")

cursor.execute("""
CREATE TABLE OrderDetails (
    order_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    price_at_purchase DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
""")

cursor.execute("""
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    payment_date DATE,
    payment_method VARCHAR(50),
    amount DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
""")

# Step 3: Insert Sample Data
# Inserting data into Customers
cursor.executemany("""
INSERT INTO Customers (name, email, phone, address, registration_date)
VALUES (%s, %s, %s, %s, %s);
""", [
    ('Alice Brown', 'alice@example.com', '1234567890', '123 Elm Street', '2024-01-15'),
    ('Bob Smith', 'bob@example.com', '1234567891', '456 Maple Avenue', '2024-02-20'),
    ('Charlie Davis', 'charlie@example.com', '1234567892', '789 Oak Lane', '2024-03-10'),
    ('Diana Green', 'diana@example.com', '1234567893', '101 Pine Road', '2024-01-25'),
    ('Ethan White', 'ethan@example.com', '1234567894', '202 Cedar Street', '2024-03-15'),
    ('Fiona Black', 'fiona@example.com', '1234567895', '303 Birch Avenue', '2024-02-10'),
    ('George Blue', 'george@example.com', '1234567896', '404 Walnut Drive', '2024-03-20'),
    ('Hannah Gold', 'hannah@example.com', '1234567897', '505 Chestnut Lane', '2024-01-05'),
    ('Ian Silver', 'ian@example.com', '1234567898', '606 Ash Street', '2024-02-25'),
    ('Julia Violet', 'julia@example.com', '1234567899', '707 Spruce Road', '2024-03-05')
])

# Inserting data into Suppliers
cursor.executemany("""
INSERT INTO Suppliers (supplier_name, contact_email, contact_phone, address)
VALUES (%s, %s, %s, %s);
""", [
    ('Tech Supplies Inc.', 'contact@techsupplies.com', '9876543210', '1 Tech Park'),
    ('Home Essentials Co.', 'support@homeessentials.com', '9876543211', '2 Home Street'),
    ('Office Depot', 'sales@officedepot.com', '9876543212', '3 Office Lane'),
    ('Green Gadgets', 'info@greengadgets.com', '9876543213', '4 Gadget Avenue'),
    ('Smart Electronics', 'support@smartelectronics.com', '9876543214', '5 Smart Road'),
    ('Kitchen Wonders', 'hello@kitchenwonders.com', '9876543215', '6 Kitchen Street'),
    ('Furniture Mart', 'contact@furnituremart.com', '9876543216', '7 Furniture Way'),
    ('Book Haven', 'sales@bookhaven.com', '9876543217', '8 Book Alley'),
    ('Fashion World', 'info@fashionworld.com', '9876543218', '9 Fashion Lane'),
    ('Toy Universe', 'support@toyuni.com', '9876543219', '10 Toy Street')
])

cursor.executemany("""
INSERT INTO Categories (category_name)
VALUES (%s);
""", [
    ('Electronics',),
    ('Home Goods',),
    ('Books',),
    ('Furniture',),
    ('Fashion',),
    ('Toys',),
    ('Kitchenware',),
    ('Office Supplies',),
    ('Outdoor',),
    ('Fitness',)
])

# Inserting data into Products
cursor.executemany("""
INSERT INTO Products (product_name, category_id, price, stock_quantity, supplier_id)
VALUES (%s, %s, %s, %s, %s);
""", [
    ('Smartphone', 1, 699.99, 50, 1),
    ('Laptop', 1, 1199.99, 30, 1),
    ('Microwave Oven', 2, 299.99, 20, 2),
    ('Fiction Book', 3, 19.99, 100, 8),
    ('Office Chair', 4, 99.99, 40, 3),
    ('T-shirt', 5, 15.99, 150, 9),
    ('Toy Car', 6, 12.99, 200, 10),
    ('Blender', 7, 49.99, 60, 6),
    ('Printer', 8, 89.99, 25, 3),
    ('Camping Tent', 9, 199.99, 15, 4)
])

# Inserting data into Orders
cursor.executemany("""
INSERT INTO Orders (customer_id, order_date, total_amount)
VALUES (%s, %s, %s);
""", [
    (1, '2024-04-01', 719.98),
    (2, '2024-04-05', 299.99),
    (3, '2024-04-10', 1299.99),
    (4, '2024-04-15', 15.99),
    (5, '2024-04-20', 99.99),
    (6, '2024-04-25', 49.99),
    (7, '2024-04-30', 199.99),
    (8, '2024-05-01', 119.99),
    (9, '2024-05-05', 299.99),
    (10, '2024-05-10', 12.99)
])

# Inserting data into OrderDetails
cursor.executemany("""
INSERT INTO OrderDetails (order_id, product_id, quantity, price_at_purchase)
VALUES (%s, %s, %s, %s);
""", [
    (1, 1, 1, 699.99),
    (1, 4, 1, 19.99),
    (2, 3, 1, 299.99),
    (3, 2, 1, 1299.99),
    (4, 6, 1, 15.99),
    (5, 5, 1, 99.99),
    (6, 8, 1, 49.99),
    (7, 10, 1, 199.99),
    (8, 9, 1, 119.99),
    (9, 3, 1, 299.99)
])

# Inserting data into Payments
cursor.executemany("""
INSERT INTO Payments (order_id, payment_date, payment_method, amount)
VALUES (%s, %s, %s, %s);
""", [
    (1, '2024-04-02', 'Credit Card', 719.98),
    (2, '2024-04-06', 'PayPal', 299.99),
    (3, '2024-04-11', 'Credit Card', 1299.99),
    (4, '2024-04-16', 'Cash', 15.99),
    (5, '2024-04-21', 'Credit Card', 99.99),
    (6, '2024-04-26', 'PayPal', 49.99),
    (7, '2024-05-01', 'Credit Card', 199.99),
    (8, '2024-05-02', 'Debit Card', 119.99),
    (9, '2024-05-06', 'PayPal', 299.99),
    (10, '2024-05-11', 'Credit Card', 12.99)
])

# Commit the changes to the database
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()


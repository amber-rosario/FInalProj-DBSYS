import mysql.connector
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta

# Function to execute queries and display results
def execute_query(query, title="Query Results"):
    db = mysql.connector.connect(
        host="localhost",
        user="new_username6",
        password="new_password6",
        database="new_database6"
    )

    # Create a cursor object
    cursor = db.cursor()
    # Execute the query and fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get column names from the cursor description
    columns = [column[0] for column in cursor.description]

    # Load data into DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Display the Data
    print(f"\n{title}")
    print(tabulate(df, headers='keys', tablefmt='grid'))

    cursor.close()
    db.close()

# 1. List payments by customers in alphabetical order
payments_by_customers_query = '''
    SELECT customers.name AS CustomerName, payments.payment_date AS PaymentDate, payments.amount AS Amount
    FROM payments
    JOIN orders ON payments.order_id = orders.order_id
    JOIN customers ON orders.customer_id = customers.customer_id
    ORDER BY customers.name ASC;
'''

# 2. Find customers who registered within the past year
registered_within_past_year_query = '''
    SELECT name AS CustomerName, registration_date
    FROM customers
    WHERE registration_date >= CURDATE() - INTERVAL 1 YEAR;
'''

# 3. Display orders along with payment details
orders_with_payment_details_query = '''
    SELECT orders.order_id, orders.order_date, payments.payment_date, payments.amount, payments.payment_method
    FROM orders
    JOIN payments ON orders.order_id = payments.order_id;
'''

# 4. List products with a price between $10 and $100
products_between_10_and_100_query = '''
    SELECT product_name, price
    FROM products
    WHERE price BETWEEN 10 AND 100;
'''

# 5. Show products along with their category names
products_with_category_names_query = '''
    SELECT products.product_name, categories.category_name
    FROM products
    JOIN categories ON products.category_id = categories.category_id;
'''

# 6. Calculate the total quantity of all products in stock
total_quantity_in_stock_query = '''
    SELECT SUM(stock_quantity) AS TotalStockQuantity
    FROM products;
'''

# 7. Calculate the total value of unsold stock for each category
unsold_stock_value_per_category_query = '''
    SELECT categories.category_name, SUM(products.stock_quantity * products.price) AS UnsoldStockValue
    FROM products
    JOIN categories ON products.category_id = categories.category_id
    GROUP BY categories.category_name;
'''

# 8. Analyze annual revenue for each product category over the past 1 year
annual_revenue_per_category_query = '''
    SELECT categories.category_name, SUM(orderdetails.quantity * products.price) AS AnnualRevenue
    FROM orderdetails
    JOIN products ON orderdetails.product_id = products.product_id
    JOIN categories ON products.category_id = categories.category_id
    WHERE orderdetails.order_id IN (
        SELECT order_id FROM orders WHERE order_date >= CURDATE() - INTERVAL 1 YEAR
    )
    GROUP BY categories.category_name;
'''

# 9. Rank customers based on total spending, average order value, and number of orders
rank_customers_query = '''
    SELECT customers.name AS CustomerName,
           SUM(orderdetails.quantity * products.price) AS TotalSpending,
           AVG(orderdetails.quantity * products.price) AS AvgOrderValue,
           COUNT(DISTINCT orders.order_id) AS NumberOfOrders
    FROM customers
    JOIN orders ON customers.customer_id = orders.customer_id
    JOIN orderdetails ON orders.order_id = orderdetails.order_id
    JOIN products ON orderdetails.product_id = products.product_id
    GROUP BY customers.customer_id
    ORDER BY TotalSpending DESC;
'''

# 10. Identify customers who haven't placed orders in the last 6 months and are at risk of churn
at_risk_customers_query = '''
    SELECT customers.name AS CustomerName, 
           MAX(orders.order_date) AS LastOrderDate
    FROM customers
    JOIN orders ON customers.customer_id = orders.customer_id
    GROUP BY customers.customer_id
    HAVING MAX(orders.order_date) <= CURDATE() - INTERVAL 6 MONTH;
'''

# 11. Calculate how much stock needs to be reordered to meet demand for the next 60 days
reorder_stock_for_60_days_query = '''
    SELECT product_name, stock_quantity, AVG(orderdetails.quantity) AS DailySales, 
           (AVG(orderdetails.quantity) * 60) AS ReorderAmount
    FROM products
    JOIN orderdetails ON products.product_id = orderdetails.product_id
    GROUP BY products.product_id;
'''

# 12. Identify product pairs frequently purchased together in the same order
frequent_product_pairs_query = '''
    SELECT A.product_id AS Product1, B.product_id AS Product2, COUNT(*) AS PairCount
    FROM orderdetails A
    JOIN orderdetails B ON A.order_id = B.order_id AND A.product_id != B.product_id
    GROUP BY A.product_id, B.product_id
    ORDER BY PairCount DESC
    LIMIT 10;
'''

# 13. Calculate the reorder point for each product based on sales trends and lead time (e.g., 7 days)
reorder_point_query = '''
    SELECT products.product_name, 
           AVG(orderdetails.quantity) * 7 AS ReorderPoint
    FROM products
    JOIN orderdetails ON products.product_id = orderdetails.product_id
    GROUP BY products.product_id;
'''

# 14. Determine how much revenue each supplier contributes to a specific product category
revenue_by_supplier_and_category_query = '''
    SELECT suppliers.supplier_name, categories.category_name, 
           SUM(orderdetails.quantity * products.price) AS Revenue
    FROM orderdetails
    JOIN products ON orderdetails.product_id = products.product_id
    JOIN suppliers ON products.supplier_id = suppliers.supplier_id
    JOIN categories ON products.category_id = categories.category_id
    GROUP BY suppliers.supplier_id, categories.category_id;
'''

# 15. Find 10 customers who placed orders for the same products
customers_same_products_query = '''
    SELECT customers.name AS CustomerName, products.product_name
    FROM customers
    JOIN orders ON customers.customer_id = orders.customer_id
    JOIN orderdetails ON orders.order_id = orderdetails.order_id
    JOIN products ON orderdetails.product_id = products.product_id
    GROUP BY customers.customer_id, products.product_id
    HAVING COUNT(DISTINCT products.product_id) > 1
    LIMIT 10;
'''

# 16. Show each category's percentage contribution to the overall sales revenue
category_percentage_revenue_query = '''
    SELECT categories.category_name, 
           SUM(orderdetails.quantity * products.price) / (SELECT SUM(orderdetails.quantity * products.price) FROM orderdetails JOIN products ON orderdetails.product_id = products.product_id) * 100 AS CategoryPercentage
    FROM orderdetails
    JOIN products ON orderdetails.product_id = products.product_id
    JOIN categories ON products.category_id = categories.category_id
    GROUP BY categories.category_name;
'''

# 17. Determine the most popular payment method based on the number of payments
popular_payment_method_query = '''
    SELECT payment_method, COUNT(*) AS PaymentCount
    FROM payments
    GROUP BY payment_method
    ORDER BY PaymentCount DESC
    LIMIT 1;
'''

# 18. Create a sales report showing each product, its category, total quantity sold, and revenue generated
sales_report_query = '''
    SELECT products.product_name, categories.category_name, 
           SUM(orderdetails.quantity) AS TotalQuantitySold, 
           SUM(orderdetails.quantity * products.price) AS TotalRevenue
    FROM orderdetails
    JOIN products ON orderdetails.product_id = products.product_id
    JOIN categories ON products.category_id = categories.category_id
    GROUP BY products.product_name, categories.category_name;
'''

# 19. List suppliers who provide products with the minimum price in the database
suppliers_with_min_price_query = '''
    SELECT suppliers.supplier_name
    FROM suppliers
    JOIN products ON suppliers.supplier_id = products.supplier_id
    WHERE products.price = (SELECT MIN(price) FROM products);
'''

# 20. Determine which category has generated the highest total revenue
highest_revenue_category_query = '''
    SELECT categories.category_name, 
           SUM(orderdetails.quantity * products.price) AS TotalRevenue
    FROM orderdetails
    JOIN products ON orderdetails.product_id = products.product_id
    JOIN categories ON products.category_id = categories.category_id
    GROUP BY categories.category_name
    ORDER BY TotalRevenue DESC
    LIMIT 1;
'''

# Execute all queries
def main():
    execute_query(payments_by_customers_query, "Payments by Customers (Alphabetical Order)")
    execute_query(registered_within_past_year_query, "Customers Registered in the Past Year")
    execute_query(orders_with_payment_details_query, "Orders with Payment Details")
    execute_query(products_between_10_and_100_query, "Products with Price Between $10 and $100")
    execute_query(products_with_category_names_query, "Products with Category Names")
    execute_query(total_quantity_in_stock_query, "Total Quantity in Stock")
    execute_query(unsold_stock_value_per_category_query, "Unsold Stock Value Per Category")
    execute_query(annual_revenue_per_category_query, "Annual Revenue Per Category")
    execute_query(rank_customers_query, "Rank Customers by Spending, Average Order Value, and Number of Orders")
    execute_query(at_risk_customers_query, "At-Risk Customers (No Orders in Last 6 Months)")
    execute_query(reorder_stock_for_60_days_query, "Stock Reorder for Next 60 Days")
    execute_query(frequent_product_pairs_query, "Frequent Product Pairs")
    execute_query(reorder_point_query, "Reorder Point for Each Product")
    execute_query(revenue_by_supplier_and_category_query, "Revenue by Supplier and Category")
    execute_query(customers_same_products_query, "Customers Who Placed Orders for the Same Products")
    execute_query(category_percentage_revenue_query, "Category's Percentage Contribution to Revenue")
    execute_query(popular_payment_method_query, "Most Popular Payment Method")
    execute_query(sales_report_query, "Sales Report by Product")
    execute_query(suppliers_with_min_price_query, "Suppliers with Minimum Price Products")
    execute_query(highest_revenue_category_query, "Category with Highest Revenue")

if __name__ == "__main__":
    main()

import mysql.connector
import pandas as pd
from tabulate import tabulate

try:
    # MySQL connection
    db = mysql.connector.connect(
        host="localhost",
        user="new_username6",
        password="new_password6",
        database="new_database6"
    )

    # Create a cursor object
    cursor = db.cursor()

    # Query for fetching the required data
    query = '''
        SELECT
            orders.order_id AS OrderID,
            customers.customer_id AS CustomerID,
            customers.name AS CustomerName,
            customers.email AS Email,
            customers.phone AS Phone,
            customers.address AS Address,
            products.product_id AS ProductID,
            products.product_name AS ProductName,
            categories.category_name AS Category,
            orderdetails.quantity AS Quantity,
            orderdetails.price_at_purchase AS PriceAtPurchase,
            orders.order_date AS OrderDate,
            orders.total_amount AS TotalAmount
        FROM
            orders
        INNER JOIN
            customers ON orders.customer_id = customers.customer_id
        INNER JOIN
            orderdetails ON orders.order_id = orderdetails.order_id
        INNER JOIN
            products ON orderdetails.product_id = products.product_id
        INNER JOIN
            categories ON products.category_id = categories.category_id
    '''

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows from the executed query
    rows = cursor.fetchall()

    if rows:
        # Get column names from the cursor description
        columns = [column[0] for column in cursor.description]

        # Load data into a pandas DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Display the data in a tabular format
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print("No data found.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if cursor:
        cursor.close()
    if db:
        db.close()

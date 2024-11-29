import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from db_connect import connect_to_database


# categories fetch
def fetch_categories():
    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT ProductCategoryID, ProductCategoryName FROM ProductCategoryView")
        categories = cursor.fetchall()

        # category dropdown values 
        category_dropdown['values'] = [f"{row[0]} - {row[1]}" for row in categories]
        if categories:
            category_dropdown.current(0)
        else:
            messagebox.showinfo("No Data", "No product categories found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch categories: {err}")
    finally:
        connection.close()

# Update products of the selected category and percentage change
def update_products():
    selected_category = category_dropdown.get()
    percentage_change = percentage_entry.get()

    if not selected_category:
        messagebox.showwarning("Input Error", "Please select a product category.")
        return
    if not percentage_change or not percentage_change.replace('.', '', 1).isdigit():
        messagebox.showwarning("Input Error", "Please enter a valid numeric percentage.")
        return

    product_category_id = int(selected_category.split(" - ")[0])
    percentage_change = float(percentage_change)

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.callproc('UpdateProductDetails', (product_category_id, percentage_change))
        connection.commit()
        messagebox.showinfo("Success", f"Products updated successfully for category ID {product_category_id}.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to update products: {err}")
    finally:
        connection.close()

# Display updated products
def show_updated_products():
    selected_category = category_dropdown.get()
    if not selected_category:
        messagebox.showwarning("Input Error", "Please select a product category.")
        return

    product_category_id = int(selected_category.split(" - ")[0])

    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT ProductID, ProductName, Weight, StandardCost, Size FROM Product WHERE ProductCategoryID = %s", (product_category_id,))
        products = cursor.fetchall()

        # Clear the list
        for row in product_tree.get_children():
            product_tree.delete(row)

        # Populate the updated products
        for product in products:
            product_tree.insert("", "end", values=product)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch updated products: {err}")
    finally:
        connection.close()

# Display all products 
def show_all_products():
    connection = connect_to_database()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT ProductID, ProductName, Weight, StandardCost, Size FROM Product")
        products = cursor.fetchall()

        # Clear the treeview
        for row in product_tree.get_children():
            product_tree.delete(row)

        # Populate the treeview with all products
        for product in products:
            product_tree.insert("", "end", values=product)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch all products: {err}")
    finally:
        connection.close()

# Main application window
root = Tk()
root.title("Product Management Application")
root.geometry("800x600")

Label(root, text="Select Product Category:", font=("Arial", 12)).pack(pady=10)

category_dropdown = ttk.Combobox(root, state="readonly", width=50)
category_dropdown.pack(pady=5)

Button(root, text="Fetch Categories", command=fetch_categories).pack(pady=5)

Label(root, text="Enter Percentage Change (%):", font=("Arial", 12)).pack(pady=10)

percentage_entry = Entry(root, width=20, font=("Arial", 12))
percentage_entry.pack(pady=5)

Button(root, text="Update Products", command=update_products, bg="green", fg="white").pack(pady=5)

Label(root, text="Updated Products:", font=("Arial", 12)).pack(pady=20)

columns = ("ProductID", "ProductName", "Weight", "StandardCost", "Size")
product_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    product_tree.heading(col, text=col)
    product_tree.column(col, width=150)

product_tree.pack(pady=10)

Button(root, text="Show Updated Product", command=show_updated_products).pack(side=LEFT, padx=10, pady=5)

Button(root, text="Show All Products", command=show_all_products).pack(side=LEFT, pady=5)

root.mainloop()

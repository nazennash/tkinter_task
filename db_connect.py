import mysql.connector
from tkinter import messagebox
# connect to mysql
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="nash",  
            database="kartik"  
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None
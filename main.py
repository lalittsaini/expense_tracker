import tkinter as tk
from tkinter import messagebox
import mysql.connector


# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "lalit",
    "database": "expense_tracker",
}

# Create a connection to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(100) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        category VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
""")

# Function to register a new user
def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()
    email = register_email_entry.get()

    if not (username and password and email):
        messagebox.showerror("Error", "Please fill in all required fields.")
    else:
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

# Function to login a user
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not (username and password):
        messagebox.showerror("Error", "Please fill in all required fields.")
    else:
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Success", "Login successful.")
                # Open the expense viewer window
                view_expenses_window(user[0])
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

# Function to view expenses for a user
def view_expenses_window(user_id):
    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")
    view_window.geometry("500x500")

    main_frame = tk.Frame(view_window)
    main_frame.pack(pady=20)

    # Get expenses from database
    cursor.execute("SELECT * FROM expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()

    # Calculate total expense
    total_expense = sum(float(expense[3]) for expense in expenses)

    # Display expenses
    for i, expense in enumerate(expenses):
        tk.Label(main_frame, text=f"Name: {expense[2]}, Amount: {expense[3]}, Category: {expense[4]}, Date: {expense[5]}", font=("Gilroy", 10)).pack()

    # Display total expense
    tk.Label(main_frame, text=f"Total Expense: {total_expense:.2f}", font=("Gilroy", 12)).pack(pady=10)

    # Add expense button
    tk.Button(main_frame, text="Add Expense", command=lambda: add_expense_window(user_id), bg='blue', fg='white', font=("Gilroy", 12)).pack(pady=10)

    # Close button
    tk.Button(main_frame, text="Close", command=view_window.destroy, bg='blue', fg='white', font=("Gilroy", 12)).pack(pady=20)

# Function to add a new expense
def add_expense_window(user_id):
    add_window = tk.Toplevel(root)
    add_window.title("Add Expense")
    add_window.geometry("500x500")

    main_frame = tk.Frame(add_window)
    main_frame.pack(pady=20)

    # Name
    name_frame = tk.Frame(main_frame)
    name_frame.pack(pady=10)
    tk.Label(name_frame, text="Name", font=("Gilroy", 12), width=10).pack(side=tk.LEFT)
    name_entry = tk.Entry(name_frame, font=("Gilroy", 12), width=25)
    name_entry.pack(side=tk.LEFT, padx=10)

    # Amount
    amount_frame = tk.Frame(main_frame)
    amount_frame.pack(pady=10)
    tk.Label(amount_frame, text="Amount", font=("Gilroy", 12), width=10).pack(side=tk.LEFT)
    amount_entry = tk.Entry(amount_frame, font=("Gilroy", 12), width=25)
    amount_entry.pack(side=tk.LEFT, padx=10)

    # Category
    category_frame = tk.Frame(main_frame)
    category_frame.pack(pady=10)
    tk.Label(category_frame, text="Category", font=("Gilroy", 12), width=10).pack(side=tk.LEFT)
    categories = ["Food", "Transportation", "Housing", "Entertainment", "Other"]
    selected_category = tk.StringVar()
    category_dropdown = tk.OptionMenu(category_frame, selected_category, *categories)
    category_dropdown.config(font=("Gilroy", 12), width=20)
    category_dropdown.pack(side=tk.LEFT, padx=10)

    # Date
    date_frame = tk.Frame(main_frame)
    date_frame.pack(pady=10)
    tk.Label(date_frame, text="Date", font=("Gilroy", 12), width=10).pack(side=tk.LEFT)
    date_entry = tk.Entry(date_frame, font=("Gilroy", 12), width=25)
    date_entry.pack(side=tk.LEFT, padx=10)

    # Add expense button
    tk.Button(main_frame, text="Add Expense", command=lambda: add_expense(user_id, name_entry, amount_entry, selected_category, date_entry), bg='blue', fg='white', font=("Gilroy", 12)).pack(pady=20)
# Function to add a new expense
def add_expense(user_id):
    name = add_name_entry.get()
    amount = add_amount_entry.get()
    category = add_category_entry.get()
    date = add_date_entry.get()

    if not (name and amount and category and date):
        messagebox.showerror("Error", "Please fill in all required fields.")
    else:
        try:
            cursor.execute("INSERT INTO expenses (user_id, name, amount, category, date) VALUES (%s, %s, %s, %s, %s)", (user_id, name, amount, category, date))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1000x500")

# Register window
register_window = tk.Frame(root, width=500, height=500, bg='white')
register_window.pack(side=tk.LEFT, fill="y")

# Create a canvas inside the register_window frame
register_canvas = tk.Canvas(register_window, width=500, height=500)
register_canvas.pack(fill="both", expand=True)

tk.Label(register_window, text="Register", width=20, font=("Zilla Slab", 20)).place(x=90, y=13)
tk.Label(register_window, text="Hello,", fg='blue', font=("Zilla Slab", 20)).place(x=70, y=53)
tk.Label(register_window, text="Welcome!", fg='blue', font=("CoalhandLuke TRIAL", 30)).place(x=70, y=87)

tk.Label(register_window, text="Username", font=("gilroy", 12)).place(x=70, y=150)
register_username_entry = tk.Entry(register_window)
register_username_entry.place(x=240, y=150)
tk.Label(register_window, text="Password", font=("gilroy", 12)).place(x=70, y=200)
register_password_entry = tk.Entry(register_window, show="*")
register_password_entry.place(x=240, y=200)
tk.Label(register_window, text="Email", font=("gilroy", 12)).place(x=70, y=250)
register_email_entry = tk.Entry(register_window)
register_email_entry.place(x=240, y=250)
tk.Button(register_window, text="Register", bg='blue', fg='white', command=register_user, font=("gilroy", 12)).place(x=170, y=300)

# Login window
border_frame = tk.Frame(root, width=1, height=500, bg='grey')
border_frame.place(x=495, y=0)
login_window = tk.Frame(root, width=500, height=500)
login_window.place(x=500, y=0)
tk.Label(login_window, text="Login", width=20, font=("Zilla Slab", 20)).place(x=90, y=13)
tk.Label(login_window, text="Username", font=("gilroy", 12)).place(x=70, y=150)
login_username_entry = tk.Entry(login_window)
login_username_entry.place(x=240, y=150)

# Password entry
tk.Label(login_window, text="Password", font=("gilroy", 12)).place(x=70, y=200)
login_password_entry = tk.Entry(login_window, show="*")
login_password_entry.place(x=240, y=200)

# Login button
tk.Button(login_window, text="Login", bg='blue', fg='white', font=("gilroy", 12), command=login_user).place(x=170, y=300)

root.mainloop()
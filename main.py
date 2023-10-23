import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@!$hu2005",
    database="electricity_bills")

total_bill = 0

cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS appliances (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, appliance_name VARCHAR(255), watts_consumed INT, hours_used INT, bill_limit INT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS bill_history (id INT AUTO_INCREMENT PRIMARY KEY, appliance_name VARCHAR(255), unit_consumption FLOAT, total_bill FLOAT, date TIMESTAMP)")

# Add Appliance Window
add_appliance_window = None

# List to store appliance data
appliances_data = []


def show_frame(frame):
    # Hide all frames
    for child in root.winfo_children():
        child.grid_remove()
    # Show the specified frame
    frame.grid(row=0, column=0, sticky="nsew")



def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Registration Error", "Username already exists. Please choose another username.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            messagebox.showinfo("Registration", "User registered successfully!")
            login_frame.grid(row=0, column=0, sticky="nsew")
            reg_frame.grid_forget()
            # show_frame(login_frame)  # Show the login frame after successful registration

    except mysql.connector.Error as err:
        messagebox.showerror("Registration Error", f"Error: {err}")
        db.rollback()


def login():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()

    if username and password:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                appliance_management_frame.grid(row=0, column=0, sticky="nsew")
                login_frame.grid_forget()
            else:
                messagebox.showerror("Login Error", "Invalid credentials. Please try again.")

        except mysql.connector.Error as err:
            messagebox.showerror("Login Error", f"Error: {err}")
    else:
        messagebox.showerror("Login Error", "Please enter both username and password.")


def open_add_appliance_window():
    global add_appliance_window
    add_appliance_window = tk.Toplevel(appliance_management_frame)
    add_appliance_window.title("Add Appliance")
    add_appliance_window.geometry("400x300")

    appliance_name_label = tk.Label(add_appliance_window, text="Appliance Name:")
    appliance_name_label.grid(row=0, column=0, sticky="w")
    appliance_name_entry = tk.Entry(add_appliance_window)
    appliance_name_entry.grid(row=0, column=1)

    watts_consumed_label = tk.Label(add_appliance_window, text="Watts Consumed:")
    watts_consumed_label.grid(row=1, column=0, sticky="w")
    watts_consumed_entry = tk.Entry(add_appliance_window)
    watts_consumed_entry.grid(row=1, column=1)

    hours_used_label = tk.Label(add_appliance_window, text="Hours Used:")
    hours_used_label.grid(row=2, column=0, sticky="w")
    hours_used_entry = tk.Entry(add_appliance_window)
    hours_used_entry.grid(row=2, column=1)

    bill_limit_label = tk.Label(add_appliance_window, text="Bill Limit:")
    bill_limit_label.grid(row=3, column=0, sticky="w")
    bill_limit_entry = tk.Entry(add_appliance_window)
    bill_limit_entry.grid(row=3, column=1)

    save_button = tk.Button(add_appliance_window, text="Save",
                            command=lambda: save_appliance(appliance_name_entry.get(), watts_consumed_entry.get(),
                                                           hours_used_entry.get(), bill_limit_entry.get()))
    save_button.grid(row=4, column=0, columnspan=2)


def save_appliance(appliance_name, watts_consumed, hours_used, bill_limit):
    try:
        appliance_data = {
            "appliance_name": appliance_name,
            "watts_consumed": int(watts_consumed),
            "hours_used": int(hours_used),
            "bill_limit": int(bill_limit),
        }
        appliances_data.append(appliance_data)
        add_appliance_window.destroy()
        messagebox.showinfo("Success", "Appliance added successfully!")

    except ValueError:
        messagebox.showerror("Error",
                             "Please enter valid numeric values for Watts Consumed, Hours Used, and Bill Limit.")


# Calculate Total Bill
def calculate_total_bill():
    total_unit_consumption = 0
    total_bill = 0
    bill_limit = 0
    print(appliances_data)
    for appliance in appliances_data:
        watts_consumed = appliance["watts_consumed"]
        hours_used = appliance["hours_used"]
        bill_limit = appliance["bill_limit"]
        unit_consumption = (watts_consumed * hours_used * 30) / 1000  # Assuming 30 days in a month
        total_unit_consumption += unit_consumption
        appliance["unit_consumption"] = unit_consumption
    print(total_unit_consumption)
    while total_unit_consumption > 0:
        if total_unit_consumption <= 100:
            total_bill += 0  # First 100 units are free
        elif total_unit_consumption <= 400:
            total_bill += total_unit_consumption * 4.5
        elif total_unit_consumption <= 500:
            total_bill += 300 * 4.5 + (total_unit_consumption - 400) * 6
        elif total_unit_consumption <= 600:
            total_bill += 300 * 4.5 + 100 * 6 + (total_unit_consumption - 500) * 8
        elif total_unit_consumption <= 800:
            total_bill += 300 * 4.5 + 100 * 6 + 100 * 8 + (total_unit_consumption - 600) * 9
        elif total_unit_consumption <= 1000:
            total_bill += 300 * 4.5 + 100 * 6 + 100 * 8 + 200 * 9 + (total_unit_consumption - 800) * 10
        else:
            total_bill += 300 * 4.5 + 100 * 6 + 100 * 8 + 200 * 9 + 200 * 10 + (total_unit_consumption - 1000) * 11

        total_unit_consumption = 0
    print(total_bill)
    print(bill_limit)
    if total_bill > bill_limit:
        messagebox.showwarning("Bill Exceeded", "The total bill amount exceeds the set limit. Please reduce usage.")
    else:
        messagebox.showinfo("Bill Calculation", f"The total monthly bill for all appliances is {total_bill} INR.")


# Store and Display Bill History
def store_bill_history(total_bill):
    try:
        for appliance in appliances_data:
            cursor = db.cursor()
            date = datetime.now().date()
            query = "INSERT INTO bill_history (appliance_name, unit_consumption, total_bill, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (appliance['appliance_name'], appliance['unit_consumption'], total_bill, date))
            db.commit()
            messagebox.showinfo("Bill History", "Bill history stored successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def calculate_individual_bill(unit_consumption):
    total_bill = 0
    while unit_consumption > 0:
        if unit_consumption <= 100:
            total_bill += 0
        elif unit_consumption <= 400:
            total_bill += unit_consumption * 4.5
        elif unit_consumption <= 500:
            total_bill += 400 * 4.5 + (unit_consumption - 400) * 6
        elif unit_consumption <= 600:
            total_bill += 400 * 4.5 + 100 * 6 + (unit_consumption - 500) * 8
        elif unit_consumption <= 800:
            total_bill += 400 * 4.5 + 100 * 6 + 100 * 8 + (unit_consumption - 600) * 9
        elif unit_consumption <= 1000:
            total_bill += 400 * 4.5 + 100 * 6 + 100 * 8 + 200 * 9 + (unit_consumption - 800) * 10
        else:
            total_bill += 400 * 4.5 + 100 * 6 + 100 * 8 + 200 * 9 + 200 * 10 + (unit_consumption - 1000) * 11

        unit_consumption = 0

    return total_bill


def display_bill_history(bill_history_data):
    bill_history_window = tk.Toplevel(root)
    bill_history_window.title("Bill History")
    bill_history_window.geometry("400x400")

    bill_history_tree = ttk.Treeview(bill_history_window,
                                     columns=("Appliance Name", "Unit Consumption", "Total Bill", "Date"))
    bill_history_tree.heading("#1", text="Appliance Name")
    bill_history_tree.heading("#2", text="Unit Consumption")
    bill_history_tree.heading("#3", text="Total Bill")
    bill_history_tree.heading("#4", text="Date")
    bill_history_tree.pack(fill="both", expand=True)

    for item in bill_history_data:
        bill_history_tree.insert("", "end", values=item)


# Display Pie Chart
def display_pie_chart():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT appliance_name, unit_consumption FROM bill_history")
        data = cursor.fetchall()

        if data:
            appliance_names = [item[0] for item in data]
            unit_consumption = [item[1] for item in data]

            fig, ax = plt.subplots()
            ax.pie(unit_consumption, labels=appliance_names, autopct='%1.1f%%')
            ax.set_title("Appliance Consumption")

            # Create a Tkinter canvas for the pie chart
            canvas = FigureCanvasTkAgg(fig, master=appliance_management_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=2, column=0, columnspan=2)
        else:
            messagebox.showinfo("Pie Chart", "No data available for pie chart.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


root = tk.Tk()
root.title("Electricity Bill Management System")
root.geometry("800x600")

# Styles for ttk
style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 10])

# Notebook for different frames
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# Register Frame
reg_frame = ttk.Frame(notebook)
notebook.add(reg_frame, text="Register")

reg_label = tk.Label(reg_frame, text="User Registration")
reg_label.grid(row=0, column=0, columnspan=2)

reg_username_label = tk.Label(reg_frame, text="Username:")
reg_username_label.grid(row=1, column=0, sticky="w")
reg_username_entry = tk.Entry(reg_frame)
reg_username_entry.grid(row=1, column=1)

reg_password_label = tk.Label(reg_frame, text="Password:")
reg_password_label.grid(row=2, column=0, sticky="w")
reg_password_entry = tk.Entry(reg_frame, show="*")
reg_password_entry.grid(row=2, column=1)
reg_button = tk.Button(reg_frame, text="Register", command=register_user)
reg_button.grid(row=3, column=0, columnspan=2)

# Login Frame
login_frame = ttk.Frame(notebook)
notebook.add(login_frame, text="Login")

login_label = tk.Label(login_frame, text="User Login")
login_label.grid(row=0, column=0, columnspan=2)

login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.grid(row=1, column=0, sticky="w")
login_username_entry = tk.Entry(login_frame)
login_username_entry.grid(row=1, column=1)

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.grid(row=2, column=0, sticky="w")
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=2, column=1)
login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2)

# Main Frame for Appliance Management
appliance_management_frame = ttk.Frame(notebook)
notebook.add(appliance_management_frame, text="Appliance Management")

add_appliance_button = tk.Button(appliance_management_frame, text="Add Appliance", command=open_add_appliance_window)
add_appliance_button.grid(row=2, column=0, columnspan=2)
bill_history_button = tk.Button(appliance_management_frame, text="Store and Display Bill History",
                                command=lambda: store_bill_history(total_bill))
bill_history_button.grid(row=1, column=0, columnspan=2)

calculate_button = tk.Button(appliance_management_frame, text="Calculate Bill", command=calculate_total_bill)
calculate_button.grid(row=0, column=0, columnspan=2)

root.mainloop()

pie_chart_button = tk.Button(appliance_management_frame, text="Display Pie Chart", command=display_pie_chart)
pie_chart_button.grid(row=3, column=0, columnspan=2)

# show_frame(reg_frame)

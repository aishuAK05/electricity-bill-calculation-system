# ⚡ Electricity Bill Management System

A Python-based application for managing and calculating electricity bills, built with **Tkinter** for the GUI, **MySQL** for data storage, and **Matplotlib** for data visualization.

This project allows users to:
- Register/Login
- Add appliances with power usage details
- Calculate total bills
- Store bill history
- View energy consumption breakdown via a pie chart

---

## 📌 Features

- **User Registration & Login** – Securely register new users and authenticate existing ones.
- **Appliance Management** – Add appliances with:
  - Name
  - Watts consumed
  - Hours used per day
  - Monthly bill limit
- **Bill Calculation** – Automatically calculate total monthly bills based on:
  - Tiered electricity rates
  - Monthly unit consumption
- **Bill Limit Warning** – Get notified if the bill exceeds a set limit.
- **Bill History Storage** – Save and retrieve bill history from MySQL.
- **Consumption Visualization** – Display a pie chart of appliance-wise energy usage.
- **MySQL Database Integration** – Store all user, appliance, and billing data.

---

## 🛠️ Tech Stack

- **Python** – Core programming language
- **Tkinter** – GUI framework for user interaction
- **MySQL** – Database for storing user, appliance, and billing records
- **Matplotlib** – For generating pie charts
- **Datetime** – To record bill history dates

---

## 📂 Database Schema

### **users**
| Field     | Type           | Description         |
|-----------|---------------|---------------------|
| id        | INT (PK)      | Auto-increment ID    |
| username  | VARCHAR(255)  | User’s login name    |
| password  | VARCHAR(255)  | User’s password      |

### **appliances**
| Field           | Type           | Description                |
|-----------------|---------------|----------------------------|
| id              | INT (PK)      | Auto-increment ID           |
| user_id         | INT           | Linked to users table       |
| appliance_name  | VARCHAR(255)  | Appliance name              |
| watts_consumed  | INT           | Power consumption in watts  |
| hours_used      | INT           | Hours used per day          |
| bill_limit      | INT           | Monthly bill limit          |

### **bill_history**
| Field           | Type           | Description              |
|-----------------|---------------|--------------------------|
| id              | INT (PK)      | Auto-increment ID         |
| appliance_name  | VARCHAR(255)  | Appliance name            |
| unit_consumption| FLOAT         | Units consumed            |
| total_bill      | FLOAT         | Bill amount               |
| date            | DATETIME      | Bill calculation date     |

---

## 💰 Electricity Bill Calculation Logic

The bill is calculated based on slab rates:

| Units Range        | Rate per Unit |
|--------------------|--------------|
| 0–100              | Free         |
| 101–400            | ₹4.5         |
| 401–500            | ₹6           |
| 501–600            | ₹8           |
| 601–800            | ₹9           |
| 801–1000           | ₹10          |
| >1000              | ₹11          |

**Note:** Each higher slab includes the charges from previous slabs.

---

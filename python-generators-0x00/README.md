# 0. Getting Started with Python Generators

## 🎯 Objective
This project creates a generator that streams rows from an SQL database one by one using Python and MySQL.

---

## 🧠 Key Concepts
- **Generators**: Used to handle large datasets efficiently.
- **Database Connection**: Using MySQL to connect, create, and populate data.
- **Functions Implemented**:
  - `connect_db()` – Connects to the MySQL database server.
  - `create_database(connection)` – Creates the `ALX_prodev` database if it doesn’t exist.
  - `connect_to_prodev()` – Connects to the `ALX_prodev` database.
  - `create_table(connection)` – Creates a table `user_data` if not present.
  - `insert_data(connection, data)` – Inserts data from a CSV file (`user_data.csv`).

---

## 🧩 Files Included
| File | Description |
|------|--------------|
| `seed.py` | Handles database setup and insertion logic |
| `0-main.py` | Main script that runs and tests the setup |
| `user_data.csv` | Contains user data for populating the database |
| `README.md` | This file — explains the project |

---

## 🧪 Example Output
When you run `0-main.py`, it should print something like:


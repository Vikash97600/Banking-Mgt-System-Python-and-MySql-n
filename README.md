🏦 Project Overview: Simple Banking System using Python and MySQL
This project is a console-based banking system implemented in Python using MySQL as the backend database. It simulates core banking functionalities for both customers and a manager.

🔧 Key Features:
Database Setup:

Creates a database BankingDB with two tables:

Customers – stores customer details and balances.

Manager_Login – for manager login authentication.

Core Functionalities:

Account Creation: Validates Aadhar (12 digits) and phone number before account creation.

Deposit/Withdrawal: Enables customers to deposit or withdraw money with balance checks.

Balance Check: Allows users to check their current account balance.

View Account: Lets users view their own account details.

Close Account: Deletes a customer account by account number.

Manager Panel: A secure login system for the bank manager to view all customer data using the tabulate library.

Error Handling:

Robust exception handling for MySQL connectivity and input validation.

🧑‍💻 Technologies Used:
Python 3.13

MySQL Connector (mysql-connector-python)

Tabulate (for pretty-printing tables in the console)

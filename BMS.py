import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS BankingDB")
     
    except Error as e:
        print(f"Error occured while creating database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='BankingDB'
        )
        cursor = connection.cursor()

        create_table_Customers = """
        CREATE TABLE IF NOT EXISTS Customers (
            AccountNo INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Email VARCHAR(100) UNIQUE NOT NULL,
            Aadhar_No VARCHAR(12) UNIQUE NOT NULL,
            Phone VARCHAR(10) UNIQUE NOT NULL,
            Balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
            Account_Type VARCHAR(30) NOT NULL
        );
        """
        cursor.execute(create_table_Customers)

        create_table_Login = """
        CREATE TABLE IF NOT EXISTS Manager_Login (
            Username VARCHAR(100) NOT NULL,
            Password VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_table_Login)

    except Error as e:
        print(f"Error occured while creating table: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='BankingDB'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Connection error: {e}")
        return None

def create_account(name, email, aadhar, phone, account_type, initial_deposit):
    try:
        if not (aadhar.isdigit() and len(aadhar) == 12):
            print("Dear customer, You have entered an invalid Aadhar number. It must be 12 digits.")

        if not (phone.isdigit() and 10 <= len(phone) <= 15):
            print("Dear customer, You have entered an invalid phone number. It must be 10-15 digits.")
            
        connection = connect_to_db()
        cursor = connection.cursor()
        query = """
        INSERT INTO Customers (Name, Email, Aadhar_No, Phone, Account_Type, Balance)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, aadhar, phone, account_type, initial_deposit))
        connection.commit()
        print(f"Dear {name}, Your account has been created successfully!")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def deposit_money(account_no, amount):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "UPDATE Customers SET Balance = Balance + %s WHERE AccountNo = %s"
        cursor.execute(query, (amount, account_no))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Dear customer, ₹{amount} has been deposited into account number {account_no}.")
        else:
            print("Account not found.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def withdraw_money(account_no, amount):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT Balance FROM Customers WHERE AccountNo = %s", (account_no,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if balance >= amount:
                cursor.execute("UPDATE Customers SET Balance = Balance - %s WHERE AccountNo = %s", (amount, account_no))
                connection.commit()
                print(f"Dear customer, You have successfully withdrawn ₹{amount} from account number {account_no}.")
            else:
                print("Dear customer, You have insufficient balance to withdraw money.")
        else:
            print("Dear customer, Your Account not found.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def check_balance(account_no):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT Balance FROM Customers WHERE AccountNo = %s", (account_no,))
        result = cursor.fetchone()
        if result:
            print(f"Dear customer, Your account number {account_no} current balance is ₹{result[0]}")
        else:
            print("Dear customer, Your Account not found.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def close_account(account_no):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Customers WHERE AccountNo = %s", (account_no,))
        connection.commit()
        print(f"Dear customr, Your Account number {account_no} closed successfully.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



def view_all_customers():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Customers")
        results = cursor.fetchall()
        if results:
            print("\nCustomer Details:")
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Dear customer, No records found.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def check_manager_login(username, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "SELECT * FROM Manager_Login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
                view_all_customers()
        else:
            print("Dear Manager, You have entered the invalid username or password.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



def view_personal_account_detail(account_no,name):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Customers WHERE AccountNo = %s and Name = %s", (account_no,name))
        results = cursor.fetchall()
        if results:
            print("\nCustomer Details:")
            headers = [desc[0] for desc in cursor.description]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Dear customer, No records found.")
    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main_function():
    create_database()
    while True:
        print("\n--- WELCOME TO THE UNION BANK OF INDIA ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Personal Account Details")
        print("6. Close Account")
        print("7. View All Customers (Manager Only)")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            aadhar = input("Enter Aadhar number (12 digits): ")
            phone = input("Enter phone number (10 digits): ")
            account_type = input("Enter the type of account(Saving / Current / PPF): ")
            try:
                initial_deposit = float(input("Enter initial deposit: "))
                create_account(name, email, aadhar, phone, account_type, initial_deposit)
            except ValueError:
                print("Invalid deposit amount.")

        elif choice == '2':
            try:
                account_no = int(input("Enter account number: "))
                amount = float(input("Enter amount to deposit: "))
                deposit_money(account_no, amount)
            except ValueError:
                print("Invalid input such as account number or amount.")

        elif choice == '3':
            try:
                account_no = int(input("Enter account number: "))
                amount = float(input("Enter amount to withdraw: "))
                withdraw_money(account_no, amount)
            except ValueError:
                print("Invalid input such as account number or amount.")

        elif choice == '4':
            try:
                account_no = int(input("Enter account number: "))
                check_balance(account_no)
            except ValueError:
                print("Invalid account number.")

        elif choice == '5':
            try:
                account_no = int(input("Enter account number: "))
                name = input("Enter name: ")
                view_personal_account_detail(account_no, name)
            except ValueError:
                print("Invalid account number.")

        elif choice == '6':
            try:
                account_no = int(input("Enter account number: "))
                close_account(account_no)
            except ValueError:
                print("Invalid account number.")

        elif choice == '7':
            username = input("Enter username of manager: ")
            password = input("Enter password: ")
            check_manager_login(username,password)

        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_function()

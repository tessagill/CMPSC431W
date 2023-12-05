# Create database 
# Run first to set up DB 

import sqlite3

def create_users_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS User')
    create_users_table = """CREATE TABLE User(
                            userID VARCHAR(30) NOT NULL,
                            fname VARCHAR(30) NOT NULL,
                            lname VARCHAR(30) NOT NULL,
                            email VARCHAR(30) NOT NULL,
                            total_balance FLOAT NOT NULL,
                            PRIMARY KEY(userID)
                            );
                            """
    cursor.execute(create_users_table) 
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO User VALUES ('Tessa.Gill', 'Tessa', 'Gill', 'tsg5227@psu.edu', 100000)''') 
    cursor.execute('''INSERT INTO User VALUES ('Jared.Cole','Jared', 'Cole', 'jcc6066@psu.edu', 150000)''') 
    cursor.execute('''INSERT INTO User VALUES ('John.Smith','John', 'Smith', 'johnsmith@example.com', 50000)''') 
    cursor.execute('''INSERT INTO User VALUES ('Sarah.Smith','Sarah', 'Smith', 'sarahsmith@example.com', 200000)''') 

    connection.commit()
    connection.close()

def create_hourly_income_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS hourly_income')
    create_hourly_income_table = """CREATE TABLE hourly_income(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            hourly_wages FLOAT NOT NULL,
                            hours_worked FLOAT NOT NULL,
                            PRIMARY KEY(userID),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_hourly_income_table) 
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO hourly_income VALUES ('Tessa.Gill', 25, 40)''') 
    cursor.execute('''INSERT INTO hourly_income VALUES ('John.Smith', 20, 40)''') 

    connection.commit()
    connection.close()


def create_annual_income_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS annual_income')
    create_annual_income_table = """CREATE TABLE annual_income(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            annual_pay FLOAT NOT NULL,
                            PRIMARY KEY(userID),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_annual_income_table) 
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO annual_income VALUES ('Jared.Cole', 100000)''') 
    cursor.execute('''INSERT INTO annual_income VALUES ('Sarah.Smith', 150000)''') 

    connection.commit()
    connection.close()

def create_transactions_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS transactions')
    create_transactions_table = """CREATE TABLE transactions(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            tranID INT NOT NULL,
                            amount FLOAT NOT NULL,
                            date_of_purchase DATE,
                            category VARCHAR(30),
                            store_name VARCHAR(30),
                            PRIMARY KEY(userID, tranID),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_transactions_table) 
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO Transactions VALUES('Tessa.Gill', 1, 100, 2023-01-01 , 'Groceries', 'Wegnmans');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Tessa.Gill', 2, 34,  2023-01-04, 'Clothes', 'Lululemon');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Tessa.Gill', 3, 75,  2023-01-08, 'Gift', 'Amazon');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Jared.Cole', 1, 250, 2023-01-13, 'Groceries', 'Trader Joes');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Jared.Cole', 2, 85, 2023-01-18, 'Fast Food', 'Chick Fil A');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Jared.Cole', 3, 87, 2023-01-23, 'Clothes', 'Amazon');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('John.Smith', 1, 2000, 2023-01-01, 'Furniture', 'IKEA');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('John.Smith', 2, 250, 2023-01-01, 'Furniture', 'Wayfair');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('John.Smith', 3, 75, 2023-01-01, 'Groceries', 'Giant');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Sarah.Smith', 1, 200, 2023-01-12, 'Groceries', 'Wegnmans');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Sarah.Smith', 2, 40, 2023-01-12, 'Gas', 'Wawa');''') 
    cursor.execute('''INSERT INTO Transactions VALUES('Sarah.Smith', 3, 20, 2023-01-15, 'Movies', 'AMC');''') 



    connection.commit()
    connection.close()


def create_debt_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS debt')
    create_debt_table = """CREATE TABLE debt(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            debt_amount FLOAT NOT NULL,
                            debt_type VARCHAR(30) NOT NULL,
                            interest_rate FLOAT NOT NULL,
                            min_payment FLOAT NOT NULL,
                            PRIMARY KEY(userID, debt_type),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_debt_table)
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO debt VALUES ('Tessa.Gill', 20000, 'Student', 2.2, 750)''')
    cursor.execute('''INSERT INTO debt VALUES ('Jared.Cole', 5000, 'Student', 2.2, 200)''') 
    cursor.execute('''INSERT INTO debt VALUES ('Jared.Cole', 10000, 'credit card', 6.7, 100)''') 
    cursor.execute('''INSERT INTO debt VALUES ('Jared.Cole', 3000, 'personal', 5.3, 200)''') 
    cursor.execute('''INSERT INTO debt VALUES ('John.Smith', 2350000, 'Mortgage', 0.8, 1300)''') 

    connection.commit()
    connection.close()


def create_investments_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS investments')
    create_investments_table = """CREATE TABLE investments(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            portfolio_total FLOAT NOT NULL,
                            risk_score FLOAT NOT NULL,
                            PRIMARY KEY(userID, portfolio_total),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_investments_table)
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO investments VALUES ('John.Smith', 50000, 15)''') 
    cursor.execute('''INSERT INTO investments VALUES ('Sarah.Smith', 25000, 10)''') 

    connection.commit()
    connection.close()

def create_planned_payments_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS planned_payments')
    create_planned_payments_table = """CREATE TABLE planned_payments(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            Date_by VARCHAR(10) NOT NULL,
                            Title VARCHAR(30) NOT NULL,
                            Amount FLOAT NOT NULL,
                            Recurring BOOL NOT NULL,
                            PRIMARY KEY(userID, title),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_planned_payments_table)
    # Queries to INSERT records. 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Tessa.Gill', '1', 'Rent', 1200, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Tessa.Gill', '15', 'Netflix', 20, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Tessa.Gill', '30', 'Utilities', 75, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Jared.Cole', '1', 'Rent', 1000, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Jared.Cole', '15', 'Utilites', 150, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('John.Smith', '1', 'Rent', 750, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('John.Smith', '01-11-2024', 'Vacation', 1500, FALSE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Sarah.Smith', '15', 'Rent', 2000, TRUE)''') 
    cursor.execute('''INSERT INTO planned_payments VALUES ('Sarah.Smith', '15', 'Netflix', 20, TRUE)''') 

    connection.commit()
    connection.close()
    
    
def create_budget_table():
    # Connect to sqlite and connect to tableSearch database
    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    cursor.execute('DROP TABLE IF EXISTS budget')
    create_budget_table = """CREATE TABLE budget(
                            userID VARCHAR(30) NOT NULL REFERENCES User(userID),
                            type VARCHAR(30) NOT NULL,
                            Allocated_amount FLOAT NOT NULL,
                            Creation_date DATE NOT NULL,
                            PRIMARY KEY (userID, type, creation_date),
                            FOREIGN KEY (userID) 
                                REFERENCES User(userID)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                            );
                            """
    cursor.execute(create_budget_table)
    connection.commit()
    connection.close()

#private function to run first to create BD
def _initialize_tables():
    create_users_table()
    create_hourly_income_table()
    create_annual_income_table()
    create_transactions_table()
    create_debt_table()
    create_investments_table()
    create_planned_payments_table()
    create_budget_table()

    connection = sqlite3.connect('finances.db')
    # Cursor object
    cursor = connection.cursor()
    # Start us with a clean slate and rebuilds a User table if it already exists
    get_all = connection.execute("""SELECT * FROM planned_payments""")
    result = get_all.fetchall()
    print('\n'.join([str(item) for item in result]))
    connection.close()



def main():
    _initialize_tables()

if __name__ == '__main__':
    main()

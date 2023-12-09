import mysql.connector as mysql


class User:
    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.total_balance = 0

    def generateUserID(self):
        self.userID = self.fname + '.' + self.lname
        return self.userID

    def addUser(userID, fname, lname, email, total_balance): 
        connection = mysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'Mississippi32', 
        database = 'finances'
        )
        cursor = connection.cursor()

        # Start a transaction
        connection.execute("BEGIN TRANSACTION")

        # Check if the userID already exists in the UserTable
        # Check with first name and last name because the combination of them may be duplicates
        cursor.execute("SELECT COUNT(*) FROM User WHERE fname = ? AND lname = ?", (fname, lname,))
        user_count = cursor.fetchone()

        try:
        # userID does not exist, proceed with the INSERT
            cursor.execute(f"""INSERT INTO User VALUES ('{userID}', '{fname}', '{lname}', '{email}', '{total_balance}') """)
            connection.commit()
            print("User added successfully.")

        #else:s
        except:
        # userID already exists, rollback the transaction
            connection.rollback()
            print("Error: userID already exists. Rolling back transaction. ")
            
        connection.close()
        return user_count[0]


    def searchUserID(userID):
        connection = mysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'Mississippi32', 
        database = 'finances'
        )
        cursor = connection.cursor()

        get_user_info = """ SELECT * FROM User WHERE userID = ? """
        cursor.execute(get_user_info, (userID,)) 
        result = cursor.fetchone()
        connection.close()

        if result: 
            user_output = {"userID:": userID, 
                           "first name:" : result[1], 
                           "last name:" : result[2], 
                           "email:" : result[3], 
                           "total_balance:" : result[4]
            }
            print ("Welcome "+ result[1] + " " + result[2])
            return userID
            
        else: 
            print ("UserID does not exist. Please try again.")
            return ("UserID does not exist")



class HourlyPaidUser:
    def __init__(self, userID, hourly_wages, hours_worked):
        self.userID = userID
        self.hourly_wages = hourly_wages
        self.hours_worked = hours_worked
        
        connection = mysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'Mississippi32', 
        database = 'finances'
        )
        cursor = connection.cursor()
        add_hourly_user = f""" INSERT INTO hourly_income VALUES ('{userID}', '{hourly_wages}', '{hours_worked}')"""
        cursor.execute(add_hourly_user)
        connection.commit()

    def calculateBiWeeklyPay(self):
        return self.hourly_wages * self.hours_worked * 2


class AnnuallyPaidUser:
    def __init__(self, userID, salary):
        self.userID = userID
        self.salary = salary

        connection = mysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'Mississippi32', 
        database = 'finances'
        )
        cursor = connection.cursor()
        add_salaried_user = f""" INSERT INTO annual_income VALUES ('{userID}', '{salary}')"""
        cursor.execute(add_salaried_user)
        connection.commit()

    def calculateBiWeeklyPay(self):
        return self.salary/26

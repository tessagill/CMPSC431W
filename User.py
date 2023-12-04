import sqlite3


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
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()

        # Start a transaction
        connection.execute("BEGIN TRANSACTION")

        # Check if the userID already exists in the UserTable
        # Check with first name and last name because the combination of them may be duplicates
        cursor.execute("SELECT COUNT(*) FROM User WHERE fname = ? AND lname = ?", (fname, lname,))
        user_count = cursor.fetchone()
        #print(user_count[0])

        #cursor.execute(f"""INSERT INTO User VALUES ('{userID}', '{fname}', '{lname}', '{email}', '{total_balance}') """)

        #if user_count[0] == 0:
        try:
        # userID does not exist, proceed with the INSERT
            cursor.execute(f"""INSERT INTO User VALUES ('{userID}', '{fname}', '{lname}', '{email}', '{total_balance}') """)
            connection.commit()
            print("User added successfully.")
            # get_all = connection.execute("""SELECT * FROM User""")
            # result = get_all.fetchall()
            # for row in result:
            #     print(row)

        #else:s
        except:
        # userID already exists, rollback the transaction
            connection.rollback()
            print("Error: userID already exists. Rolling back transaction. ")
            
        connection.close()
        return user_count[0]


    def searchUserID(userID):
        connection = sqlite3.connect('finances.db')
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
            # get_annual_income_info = """ SELECT * FROM annual_income WHERE userID = ?"""
            # cursor.execute(get_annual_income_info, (userID,))
            # result_annual = cursor.fetchone()
            # if result_annual:
            #     return AnnuallyPaidUser(result[1], result[2], result[3], result_annual[1])

            # get_hourly_income_info = """ SELECT * FROM hourly_income WHERE userID = ?"""
            # cursor.execute(get_hourly_income_info, (userID,))
            # result_hourly = cursor.fetchone()
            # if result_hourly:
            #     return HourlyPaidUser(result[1], result[2], result[3], result_hourly[1], result_hourly[2])
            
        else: 
            print ("UserID does not exist. Please try again.")
            return ("UserID does not exist")



class HourlyPaidUser:
    def __init__(self, userID, hourly_wages, hours_worked):
        self.userID = userID
        self.hourly_wages = hourly_wages
        self.hours_worked = hours_worked
        
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        add_hourly_user = f""" INSERT INTO hourly_income VALUES ('{userID}', '{hourly_wages}', '{hours_worked}')"""
        cursor.execute(add_hourly_user)
        connection.commit()
        # get_all = connection.execute("""SELECT * FROM Hourly_income""")
        # result = get_all.fetchall()
        # for row in result:
        #     print(row)
        # connection.close()


    def calculateBiWeeklyPay(self):
        return self.hourly_wages * self.hours_worked * 2


class AnnuallyPaidUser:
    def __init__(self, userID, salary):
        self.userID = userID
        self.salary = salary

        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        add_salaried_user = f""" INSERT INTO annual_income VALUES ('{userID}', '{salary}')"""
        cursor.execute(add_salaried_user)
        connection.commit()
        #get_all = connection.execute("""SELECT * FROM Annual_Income""")
        # result = get_all.fetchall()
        # for row in result:
        #     print(row)
        # connection.close()   



    def calculateBiWeeklyPay(self):
        return self.salary/26

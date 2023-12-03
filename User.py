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
        add_user = """ INSERT INTO User VALUES ('{userID}', '{fname}', '{lanme}', '{email}', '{total_balance}')"""
        cursor.execute(add_user)
        connection.close()


    def searchUserID(userID):
        """
        Should return a class object of HourlyPaidUser or AnnuallyPaidUser or an error message indicating that
        the user could not be found information on the user including fname, lname, email, and to try a new userID
        """ 
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
        add_hourly_user = """ INSERT INTO hourly_income VALUES ('{userID}', '{hourly_wages}', '{hours_worked}')"""
        cursor.execute(add_hourly_user)
        connection.close()

    def calculateBiWeeklyPay(self):
        return self.hourly_wages * self.hours_worked * 2


class AnnuallyPaidUser:
    def __init__(self, userID, salary):
        #super().__init__(fname, lname, email)
        self.userID = userID
        self.salary = salary

        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        add_salaried_user = """ INSERT INTO annual_income VALUES ('{userID}', '{salary}')"""
        cursor.execute(add_salaried_user)
        connection.close()   

    def calculateBiWeeklyPay(self):
        return self.salary/26

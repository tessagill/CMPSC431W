import sqlite3


class User:
    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def generateUserID(self):
        self.userID = self.fname + '.' + self.lname
        return self.userID

    def addUser(userID, fname, lname, email, total_balance):
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        add_user = """ INSERT INTO User VALUES ('{userID}', '{fname}', '{lanme}', '{email}', '{total_balance})"""
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

        if result: 
            user_output = {"userID:": userID, 
                           "first name:" : result[1], 
                           "last name:" : result[2], 
                           "email:" : result[3], 
                           "total_balance:" : result[4]
            }
            get_annual_income_info = """ SELECT * FROM annual_income WHERE userID = ?"""
            cursor.execute(get_annual_income_info, (userID,))
            result_annual = cursor.fetchone()
            if result_annual:
                return AnnuallyPaidUser(result[1], result[2], result[3], result_annual[1])

            get_hourly_income_info = """ SELECT * FROM hourly_income WHERE userID = ?"""
            cursor.execute(get_hourly_income_info, (userID,))
            result_hourly = cursor.fetchone()
            if result_hourly:
                return HourlyPaidUser(result[1], result[2], result[3], result_hourly[1], result_hourly[2])
            
        else: 
            print ("UserID does not exist")

        connection.close()


class HourlyPaidUser(User):
    def __init__(self, fname, lname, email, hourly_wages, hours_worked):
        super().__init__(fname, lname, email)
        self.hourly_wages = hourly_wages
        self.hours_worked = hours_worked

    def calculateBiWeeklyPay(self):
        return self.hourly_wages * self.hours_worked * 2


class AnnuallyPaidUser(User):
    def __init__(self, fname, lname, email, salary):
        super().__init__(fname, lname, email)
        self.salary = salary
    
    def calculateBiWeeklyPay(self):
        return self.salary/26

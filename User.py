class User:
    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def generateUserID(self):
        self.userID = self.fname + '.' + self.lname
        return self.userID
        
    def searchUserID(userID):
        """
        Should return a class object of HourlyPaidUser or AnnuallyPaidUser or an error message indicating that
        the user could not be found information on the user including fname, lname, email, and to try a new userID
        """
        pass


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


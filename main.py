from User import *
from verifyInput import *
from commands import *

def getUser():
    start = getValidInput('\nAre you a new or existing user? ', options=['new', 'existing'])

    if start.lower() == 'new':
        clear()
        print('Welcome!')
        fname = input('Enter your first name: ')
        lname = input('Enter your last name: ')
        email = input('Enter your email: ')
        newUser = User(fname, lname, email)
        userID = newUser.generateUserID()
        print(f'\nHi {fname} {lname}! Your unique userID is {userID}')
        print('\nLet\'s get you started so you can start to take control of your money!')
        incomeType = getValidInput('\nIs your income hourly or salaried?\n', options=['hourly', 'salaried'])
        
        if incomeType == 'hourly':
            hourly_wage = getValidInput('\nEnter your hourly pay: ', number=True)
            hours_worked = getValidInput('\nEnter your weekly hours worked: ', number=True)
            newUser = HourlyPaidUser(newUser.fname, newUser.lname, newUser.email, hourly_wage, hours_worked)
        elif incomeType == 'salaried':
            salary = getValidInput('\nEnter your annual pay: ', number=True)
            newUser = HourlyPaidUser(newUser.fname, newUser.lname, newUser.email, salary)
        
        return newUser
        

    elif start.lower() == 'existing':
        userID = input('Enter your UserID: ')
        user = User.searchUserID(userID)
        return user


def main():
    getUser()
    while True:
        listCommands()
        pass





if __name__ == '__main__':
    main()
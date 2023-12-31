from User import *
from verifyInput import *
from commands import *
import mysql.connector as mysql

def getUser():
    start = getValidInput('\nAre you a new or existing user? ', options=['new', 'existing'])

    if start == 'new':
        clear()
        print('Welcome!')
        fname = input('Enter your first name: ')
        lname = input('Enter your last name: ')
        email = input('Enter your email: ')
        total_balance = input('Enter your current savings: ')
        newUser = User(fname, lname, email)
        userID = newUser.generateUserID()
        user_count = User.addUser(userID, fname, lname, email, total_balance)
        if user_count == 0:
            print(f'\nHi {fname} {lname}! Your unique userID is {userID}')
            print('\nLet\'s get you started so you can start to take control of your money!')
            incomeType = getValidInput('\nIs your income hourly or salaried?\n', options=['hourly', 'salaried'])
        
            if incomeType == 'hourly':
                hourly_wage = getValidInput('\nEnter your hourly pay: ', decimal=True)
                hours_worked = getValidInput('\nEnter your weekly hours worked: ', decimal=True)
                HourlyPaidUser(userID, hourly_wage, hours_worked)
            elif incomeType == 'salaried':
                salary = getValidInput('\nEnter your annual pay: ', decimal=True)
                AnnuallyPaidUser(userID, salary)
            return userID
        
        elif user_count != 0: 
            option = getValidInput('\nWould you like to log in or generate a unique ID? ', options=['log in', 'generate'])
            if option == 'log in':
                getUser()
            else: #generate unique user ID by adding what number of that name they are 
                userID = userID + str(user_count+1) 
                print(f'\nHi {fname} {lname}! Your unique userID is {userID}')
                print('\nLet\'s get you started so you can start to take control of your money!')
                incomeType = getValidInput('\nIs your income hourly or salaried?\n', options=['hourly', 'salaried'])
        
                if incomeType == 'hourly':
                    hourly_wage = getValidInput('\nEnter your hourly pay: ', decimal=True)
                    hours_worked = getValidInput('\nEnter your weekly hours worked: ', decimal=True)
                    HourlyPaidUser(userID, hourly_wage, hours_worked)
                elif incomeType == 'salaried':
                    salary = getValidInput('\nEnter your annual pay: ', decimal=True)
                    AnnuallyPaidUser(userID, salary)
            return userID
        
    elif start == 'existing':
        logged_in = False
        while logged_in == False:
            userID = input('Enter your UserID: ')
            if User.searchUserID(userID) != "UserID does not exist":
                logged_in = True 
        return userID


def main():
    user = getUser() # retrieves new or existing user
    while True:
        #clear()
        listCommands()
        command = input("Enter action: ").lower()
        print()

        # ALL COMMANDS
        if command == "create new debt":
            createNewDebt(user)
        elif command == "create planned payment":
            createNewPlannedPayment(user)
        elif command == "create transaction":
            createNewTransaction(user)
        elif command == "create investment portfolio":
            createNewInvestment(user)
        elif command == "update income":
            updateIncome(user) 
        elif command == "update debt":
            updateDebt(user)
        elif command == "update investments":
            updateInvestments(user)
        elif command == "update planned payments":
            updatePlannedPayments(user)
        elif command == "view debt payoff timeline":
            viewDebtPayoffTimeline(user)
        elif command == "view expenses by category":
            viewExpensesByCategory(user)
        elif command == "view budget":
            viewBudget(user)
        elif command == "exit":
            break
        else:
            print("Unknown command")


if __name__ == '__main__':
    main()

from User import *
from verifyInput import *
from commands import *

def getUser():
    start = getValidInput('\nAre you a new or existing user? ', options=['new', 'existing'])

    if start == 'new':
        clear()
        print('Welcome!')
        fname = input('Enter your first name: ')
        lname = input('Enter your last name: ')
        email = input('Enter your email: ')
        newUser = User(fname, lname, email)
        userID = newUser.generateUserID()
        User.addUser(userID, )
        print(f'\nHi {fname} {lname}! Your unique userID is {userID}')
        print('\nLet\'s get you started so you can start to take control of your money!')
        incomeType = getValidInput('\nIs your income hourly or salaried?\n', options=['hourly', 'salaried'])
        
        if incomeType == 'hourly':
            hourly_wage = getValidInput('\nEnter your hourly pay: ', decimal=True)
            hours_worked = getValidInput('\nEnter your weekly hours worked: ', decimal=True)
            newUser = HourlyPaidUser(newUser.fname, newUser.lname, newUser.email, hourly_wage, hours_worked)
        elif incomeType == 'salaried':
            salary = getValidInput('\nEnter your annual pay: ', decimal=True)
            newUser = HourlyPaidUser(newUser.fname, newUser.lname, newUser.email, salary)
        
        return newUser
        

    elif start == 'existing':
        userID = input('Enter your UserID: ')
        user = User.searchUserID(userID)
        return user


def main():
    user = getUser() # retrieves new or existing user
    while True:
        clear()
        listCommands()
        command = input().lower()
        print()

        # ALL COMMANDS
        if command == "create new debt":
            createNewDebt(user)
        elif command == "create recurring payment":
            createNewRecurring(user)
        elif command == "create upcoming payment":
            createNewUpcomingPayment(user)
        elif command == "create transaction":
            createNewTransaction(user)
        elif command == "create new budget":
            print("Handling CREATE new budget")
        elif command == "update income":
            user = updateIncome(user) # returns the updated user object with new income
        elif command == "update debt":
            updateDebt(user)
        elif command == "update investments":
            print("Handling UPDATE investments")
        elif command == "update recurring":
            print("Handling UPDATE recurring")
        elif command == "update planned payments":
            print("Handling UPDATE planned payments")
        elif command == "view debt payoff timeline":
            print("Handling VIEW debt payoff timeline")
        elif command == "view predicted month's spending":
            print("Handling VIEW predicted month's spending")
        elif command == "view expenses by category":
            print("Handling VIEW expenses by category")
        elif command == "view budget":
            print("Handling VIEW budget")
        else:
            print("Unknown command")







if __name__ == '__main__':
    main()

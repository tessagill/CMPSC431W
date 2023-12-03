from verifyInput import *
from datetime import datetime
from User import *
from Debt import *
from Investments import *
from PlannedPayments import *
from Transactions import *
from Budget import *

def listCommands():
    print("""
LIST OF COMMANDS: CASE-INSENSITIVE         

CREATE new debt
CREATE recurring payment
CREATE upcoming payment
CREATE transaction
CREATE new budget

UPDATE income
UPDATE debt
UPDATE investments
UPDATE recurring
UPDATE planned payments

VIEW debt payoff timeline
VIEW predicted month's spending
VIEW expenses by category
VIEW budget
""")


def createNewDebt(user):
    """
    Adds a debt instance and asks what type and what amount
    """
    debtType = getValidInput('What type of debt are you adding? student loan, credit card, personal, medical, mortage, miscellaneous: ', 
                  options=['student loan', 'credit card', 'personal', 'medical', 'mortage', 'miscellaneous'])
    amount = getValidInput('How much money in dollars is this debt? ', decimal=True)
    interestRate = getValidInput('What is the annual interest rate? ', decimal=True)
    minPayment = getValidInput('What is the minimum monthly payment? ', decimal=True)

    # SQL command to enter data here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_debt = """ INSERT INTO User VALUES ('{user.userID}', '{debtType}', '{amount}', '{interestRate}', '{total_balance})"""
    cursor.execute(add_debt)
    connection.close()
    print(f'\n{user.UserID}, your {debtType} debt of {amount:.2f}, with interest rate {interestRate}% and minimum payment ${minPayment} has been added.')
    input('\nPress ENTER to continue')

def createNewRecurring(user):
    """
    Adds a new recurring payment instance and asks for payment details
    """
    name = input('What should this recurring payment be called? ')
    amount = getValidInput('How much is this payment? ', decimal=True)
    date_by = getValidInput('What day of the month is it due? ', integer=True, intRange=[1, 31])

    print(f'\nYour recurring payment, {name}, of ${amount:.2f} due the {date_by} of every month has been added.')
    input('\nPress ENTER to continue')

def createNewUpcomingPayment(user):
    """
    Adds an upcoming payment instance and asks for payment details
    """
    name = input('What should this upcoming payment be called? ')
    amount = getValidInput('How much is this payment? ', decimal=True)
    date = getValidInput('What date is it due? (Please enter in MM-DD-YYYY format)\n', isDate=True)

    print(f'\nYour upcoming payment, {name}, of ${amount:.2f} on {date} has been added.')
    input('\nPress ENTER to continue')


def createNewTransaction(user):
    """
    Adds a new transaction instance and asks for transaction details
    """
    amount = getValidInput('Enter transaction amount in dollars: ', decimal=True)
    current_date = datetime.now().date()
    type = getValidInput('Enter transaction type: ',
                options=['utilities', 'travel', 'rent', 'entertainment', 'debt payment', 'groceries'])
    name = input('Enter the merchant\'s name: ')
    #tranID = generateTranID() # some sort of SQL command that generates a new unique ID?, or we can have it generated upon insertion

    #SQL command to enter transaction here

    print(f'\nYour {type} transaction from {name} of ${amount:.2f} has been added')
    input('\nPress ENTER to continue')

def updateIncome(user):
    """
    Updates the current user's income and returns the user object back
    """
    newIncome = getValidInput('What do you want to update your income to? ', decimal=True)

    # SQL command to update income

    print(f'{user.fname} your income has been updated to ${newIncome:.2f}')
    input('\nPress ENTER to continue')


def updateDebt(user):
    """
    Updates the current user's selected debt or deletes it
    """

    # retrieve types of debt where user.userID is the same, then put it as debtTypes list
    debtTypes = ['credit card', 'personal']

    selectedType = getValidInput(f'Which debt type do you want to modify?\ncurrent debt: {", ".join(debtTypes)}\n', options=debtTypes)

    # SQL command to retrieve debt instance of selectedType and put it into debt object
    amount = 99.99 # this amount will be changed but is temporary
    print(f'We retrieved your {selectedType} debt of ${amount:.2f}\n')

    option = getValidInput('Do you want to change the debt amount, interest rate, minimum payment or simply delete it? ', 
                  options=['debt amount', 'amount', 'min payment', 'minimum payment', 'delete'])
    
    if option == 'debt amount' or option == 'amount':
        newAmount = getValidInput('What amount should it be? ', decimal=True)
        # SQL command to update the new debt amount
        print(f'Your {selectedType} debt amount has been successfully updated to ${newAmount:.2f}.')
    elif option == 'min payment' or option == 'minimum payment':
        newMinPayment = getValidInput('What is the new minimum payment ', decimal=True)
        # SQL command to update new minimum payment
        print(f'Your {selectedType} debt minumum payment has been successfully updated to ${newMinPayment:.2f}.')
    elif option == 'delete':
        # SQL command to delete instance
        print(f'Your {selectedType} debt has been successfully deleted.')
    
    input('\nPress ENTER to continue')

def updateInvestments(user):
    """
    Updates the current user's selected investment or deletes it
    """

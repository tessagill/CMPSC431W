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
CREATE planned payment
CREATE transaction
CREATE new budget

UPDATE income
UPDATE debt
UPDATE investments
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
    add_debt = """ INSERT INTO Debt VALUES ('{user}', '{debtType}', '{amount}', '{interestRate}', '{total_balance})"""
    cursor.execute(add_debt)
    connection.close()
    print(f'\n{user.UserID}, your {debtType} debt of {amount:.2f}, with interest rate {interestRate}% and minimum payment ${minPayment} has been added.')
    input('\nPress ENTER to continue')

def createNewPlannedPayment(user):
    """
    Adds a new recurring payment instance and asks for payment details
    """
    name = input('What should this recurring payment be called? ')
    amount = getValidInput('How much is this payment? ', decimal=True)
    date_by = getValidInput('What day of the month is it due? Enter number  1-31 ', integer=True, intRange=[1, 31])
    recurring = getValidInput('Is this a recurring payment? ', bool = True)

    # SQL command to enter data here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_planned_payment = """ INSERT INTO planned_payments VALUES ('{user}', '{date_by}', '{name}', '{amount}', '{recurring}' """
    cursor.execute(add_planned_payment)
    connection.close()

    if recurring == True:
        print(f'\nYour recurring payment, {name}, of ${amount:.2f} due the {date_by} of every month has been added.')
    
    elif recurring == False: 
        print(f'\nYour planned payment, {name}, of ${amount:.2f} due by {date_by} has been added.')

    input('\nPress ENTER to continue')

# def createNewUpcomingPayment(user):
#     """
#     Adds an upcoming payment instance and asks for payment details
#     """
#     name = input('What should this upcoming payment be called? ')
#     amount = getValidInput('How much is this payment? ', decimal=True)
#     date = getValidInput('What date is it due? (Please enter in MM-DD-YYYY format)\n', isDate=True)

#     print(f'\nYour upcoming payment, {name}, of ${amount:.2f} on {date} has been added.')
#     input('\nPress ENTER to continue')


def createNewTransaction(user):
    """
    Adds a new transaction instance and asks for transaction details
    """
    amount = getValidInput('Enter transaction amount in dollars: ', decimal=True)
    current_date = datetime.now().date()
    category = getValidInput('Enter transaction type (utilites, travel, rent, entertainment, dept payment, groceries, clothes, gift, fast food, misc.) ): ',
                options=['utilities', 'travel', 'rent', 'entertainment', 'debt payment', 'groceries', 'clothes', 'gift'])
    store_name = input('Enter the merchant\'s name: ')
    #tranID = generateTranID() # some sort of SQL command that generates a new unique ID?, or we can have it generated upon insertion

    #SQL command to enter transaction here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_planned_payment = """ INSERT INTO transactions VALUES ('{user}', '{tranID}', '{amount}', '{category}', '{store_name})"""
    cursor.execute(add_planned_payment)
    connection.close()

    print(f'\nYour {category} transaction from {store_name} of ${amount:.2f} has been added')
    input('\nPress ENTER to continue')

def updateIncome(user):
    """
    Updates the current user's income and returns the user object back
    """
    newIncome = getValidInput('What do you want to update your income to? ', decimal=True)
    # Add statement to do this with hourly workers
    # SQL command to update income
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    update_income = """ UPDATE Annual_income SET annual_pay = {newIncome} WHERE userID = {user}"""
    cursor.execute(update_income)
    connection.close()
    
    print(f'\nYour income has been updated to ${newIncome:.2f}')
    input('\nPress ENTER to continue')


def updateDebt(user):
    """
    Updates the current user's selected debt or deletes it
    """

    # retrieve types of debt where user.userID is the same, then put it as debtTypes list
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_debts = """ SELECT debt_type FROM Debt WHERE userID = '{user}' )"""
    debtTypes = [item[0] for item in cursor.fetchall(get_debts)]
    connection.close()

    selectedType = getValidInput(f'Which debt type do you want to modify?\ncurrent debt: {", ".join(debtTypes)}\n', options=debtTypes)

    # SQL command to retrieve debt instance of selectedType and put it into debt object
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    selected_debt = """ SELECT * FROM Debt WHERE userID = '{user}' AND type = '{selectedType}' )"""
    result = cursor.fetchone(selected_debt)
    connection.close()

    amount = result[1] # debt amount of selected type 
    print(f'We retrieved your {selectedType} debt of ${amount:.2f}\n')

    option = getValidInput('Do you want to change the debt amount, interest rate, minimum payment or simply delete it? ', 
                  options=['debt amount', 'amount', 'min payment', 'minimum payment', 'delete'])
    
    if option == 'debt amount' or option == 'amount':
        newAmount = getValidInput('What amount should it be? ', decimal=True)

        # SQL command to update the new debt amount
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        update_debt_amt = """ UPDATE debt SET debt_amount = {newAmount} WHERE userID = '{user}'"""
        cursor.execute(update_debt_amt)
        connection.close()  

        print(f'Your {selectedType} debt amount has been successfully updated to ${newAmount:.2f}.')

    elif option == 'min payment' or option == 'minimum payment':
        newMinPayment = getValidInput('What is the new minimum payment ', decimal=True)

        # SQL command to update new minimum payment
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        update_min_amount = """ UPDATE debt SET min_payment = {newMinPayment} WHERE userID = '{user}'"""
        cursor.execute(update_min_amount)
        connection.close()  

        print(f'Your {selectedType} debt minumum payment has been successfully updated to ${newMinPayment:.2f}.')

    elif option == 'delete':
        # SQL command to delete instance
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        delete_debt = """ DELETE FROM debt WHERE userID = '{user}' AND debt_type = '{selectedType}' """
        cursor.execute(delete_debt)
        connection.close()  

        print(f'Your {selectedType} debt has been successfully deleted.')
    
    input('\nPress ENTER to continue')

def updateInvestments(user):
    """
    Updates the current user's selected investment or deletes it
    """
    # retrieves user's investment portfolio 
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_investment = """ SELECT * FROM Investments WHERE userID = '{user}' )"""
    result = cursor.fetchall(get_investment)
    connection.close()

    option = getValidInput('Do you want to change the risk score or simply delete the investment from your account? ', 
                  options=['risk score', 'delete'])
    
    if option == 'risk score':
        newPercent = getValidInput('What is your new risk score? ', decimal=True)

        # SQL command to update the new risk score
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        update_risk_score = """ UPDATE Investments SET risk_percent = {newPercent} WHERE userID = '{user}' """
        cursor.execute(update_risk_score)
        connection.close()  

        print(f'Your risk score has successfully been updated to {newPercent:.2f} %.')

    elif option == 'delete':
        # SQL command to delete instance
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        delete_investment = """ DELETE FROM Investments WHERE userID = '{user}' AND portfolio_total = '{result[2]}' """
        cursor.execute(delete_investment)
        connection.close()  

        print(f'Your investment portfolio has successfully been deleted.')
    
    input('\nPress ENTER to continue')

def updatePlannedPayments(user):
    """
    Updates the current user's selected planned payment or deletes it
    """  
    # retrieve the planned payment the use wants to alter
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_planned_payments = """ SELECT Title FROM planned_payments WHERE userID = '{user}' )"""
    pp = [item[0] for item in cursor.fetchall(get_planned_payments)]
    connection.close()

    selectedType = getValidInput(f'Which planned payment do you want to modify?\ncurrent planned payments: {", ".join(pp)}\n', options=pp)

    option = getValidInput('Do you want to change the payment amount, due date, or simply delete it? ', 
                  options=['payment amount', 'amount', 'due date', 'date', 'delete'])
    
    if option == 'payment amount' or option == 'amount':
        newAmount = getValidInput('What is your new payment amount? ', decimal=True)

        # SQL command to update the payment amount
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        update_payment_amt = """ UPDATE Planned_payments SET Amount = {newAmount} WHERE userID = '{user}' AND type = '{selectedType}' """
        cursor.execute(update_payment_amt)
        connection.close() 

        print(f'Your payment amount has successfully been updated to {newAmount:.2f} %.')

    if option == 'due date' or option == 'date':
        newDate = getValidInput('What is the new date of payment? ', integer=True, intRange=[1, 31])

        # SQL command to update the due date  
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        update_date = """ UPDATE Planned_payments SET Date = {newDate} WHERE userID = '{user}' AND type = '{selectedType}' """
        cursor.execute(update_date)
        connection.close() 

        print(f'The date of your payment has successfully been updated to the {newAmount} day of the month.')

    elif option == 'delete':
        # SQL command to delete instance
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        delete_planned_payment = """ DELETE FROM planned_payments WHERE userID = '{user}' AND type = '{selectedType}' """
        cursor.execute(delete_planned_payment)
        connection.close()  

        print(f'Your planned payment has successfully been deleted.')
    
    input('\nPress ENTER to continue')


def viewExpensesByCategory(user):
    """
    Returns sorted list of expenses
    """
    #SQL command
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    viewExpenses = """SELECT category, sum(amount)
                      FROM Transactions
                      WHERE userID = ?
                      GROUP BY userID, category
                      ORDER BY sum(amount) DESC"""

    cursor.execute(viewExpenses, (user,))
    result = cursor.fetchall()
    connection.close()

    print(f'\nYour expenses in descending order are:\n ')
    for row in result:
        print(f'{row[0]}: ${row[1]}\n')
    input('\nPress ENTER to continue')

def viewBudget(user):
    """
    Returns budget table with combined income, savings, and expenses
    """
    annualSalary = isAnnual(user)

    if annualSalary == True: 
        #SQL command to create budget for salary user
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        viewBudget = """SELECT u.userID AS userID, ROUND(a.annual_pay/12, 2) AS monthlySalary, sum(t.amount) AS
                        total_transactions, sum(d.min_payment) AS total_debt_monthly_payments,
                        sum(pp.amount) AS total_planned_expenses, 
                        ROUND((ROUND(a.annual_pay/12, 2) - sum(t.amount) - sum(d.min_payment) - sum(pp.amount)), 2) AS remainingAmount
                    FROM User u
                        LEFT JOIN Annual_income a
                        ON u.userID = a.userID
                        LEFT JOIN Transactions t
                        ON u.userID = t.userID
                        LEFT JOIN Debt d
                        ON u.userID = d.userID
                        LEFT JOIN Planned_Payments pp
                        ON u.userID = pp.userID
                    WHERE u.userID = ?
                    """

        cursor.execute(viewBudget, (user,))
        result = cursor.fetchall()
        connection.close()

    else:
        #SQL command to create budget for hourly paid user
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        viewBudget = """SELECT u.userID AS userID, ROUND(h.hourly_wages * h.hours_worked * 4, 2) AS monthlySalary, sum(t.amount) AS
                        total_transactions, sum(d.min_payment) AS total_debt_monthly_payments,
                        sum(pp.amount) AS total_planned_expenses, 
                        ROUND((ROUND(h.hourly_wages * h.hours_worked * 4, 2) - sum(t.amount) - sum(d.min_payment) - sum(pp.amount)), 2) AS remainingAmount
                    FROM User u
                        LEFT JOIN hourly_income h
                        ON u.userID = h.userID
                        LEFT JOIN Transactions t
                        ON u.userID = t.userID
                        LEFT JOIN Debt d
                        ON u.userID = d.userID
                        LEFT JOIN Planned_Payments pp
                        ON u.userID = pp.userID
                    WHERE u.userID = ?
                    """

        cursor.execute(viewBudget, (user,))
        result = cursor.fetchall()
        connection.close()

    print(f'\nYour budget is:\n ')
    for row in result:
        print(f'Monthly Income: ${row[1]}\nTransactions: ${row[2]}\nDebt Payments: ${row[3]}\nPlanned Payments: ${row[4]}\nRemaining Amount: ${row[5]}')
    input('\nPress ENTER to continue')

def isAnnual(user):
    #SQL command to check if a user is paid annually 
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()

    check= "SELECT COUNT(*) FROM annual_income WHERE userID = ?"
    cursor.execute(check, (user,))
    count = cursor.fetchone()[0]

    connection.close()
    if count != 0:
        return True 
    else: 
        return False

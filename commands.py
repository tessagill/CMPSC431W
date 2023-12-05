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
CREATE investment portfolio

UPDATE income
UPDATE debt
UPDATE investments
UPDATE planned payments

VIEW debt payoff timeline
VIEW expenses by category
VIEW budget
          
EXIT 
""")


def createNewDebt(user):
    """
    Adds a debt instance and asks what type and what amount
    """
    debtType = getValidInput('What type of debt are you adding? (student loan, credit card, personal, medical, mortgage, miscellaneous): ', 
                  options=['student loan', 'credit card', 'personal', 'medical', 'mortgage', 'miscellaneous'])
    amount = getValidInput('How much money in dollars is this debt? $', decimal=True)
    interestRate = getValidInput('What is the annual interest rate? ', decimal=True)
    minPayment = getValidInput('What is the minimum monthly payment? $', decimal=True)

    # SQL command to enter data here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_debt = f"""INSERT INTO Debt VALUES ('{user}', {amount}, '{debtType}', {interestRate}, {minPayment})"""
    print(add_debt)
    cursor.execute(add_debt)
    connection.commit()
    connection.close()
    print(f'\n{user}, your {debtType} debt of ${amount:.2f}, with interest rate {interestRate}% and minimum payment ${minPayment:.2f} has been added.')
    input('\nPress ENTER to continue')

def createNewPlannedPayment(user):
    """
    Adds a new recurring payment instance and asks for payment details
    """
    name = input('What should this recurring payment be called? ')
    amount = getValidInput('How much is this payment? ', decimal=True)
    recurring = getValidInput('Is this a recurring payment? ', options=['yes', 'no'])
    recurring = True if recurring == 'yes' else False # convert to boolean
    if recurring:
        date = getValidInput('What day of the month is it due? Enter number 1-31 ', integer=True, intRange=[1, 31])
    else:
        date = getValidInput('What date is it due? (Please enter in MM-DD-YYYY format) ', isDate=True)

    # SQL command to enter data here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_planned_payment = f""" INSERT INTO planned_payments VALUES ('{user}', '{date}', '{name}', {amount}, {recurring} """
    cursor.execute(add_planned_payment)
    connection.commit()
    connection.close()

    if recurring == True:
        print(f'\nYour recurring payment, {name}, of ${amount:.2f} due the {date} of every month has been added.')
    else: 
        print(f'\nYour planned payment, {name}, of ${amount:.2f} due by {date} has been added.')

    input('\nPress ENTER to continue')


def createNewTransaction(user):
    """
    Adds a new transaction instance and asks for transaction details
    """
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    amount = getValidInput('Enter transaction amount in dollars: ', decimal=True)
    category = getValidInput('Enter transaction type (utilites, travel, rent, entertainment, debt payment, groceries, clothes, gift, fast food, misc.): ',
                options=['utilities', 'travel', 'rent', 'entertainment', 'debt payment', 'groceries', 'clothes', 'gift', 'fast food', 'misc.'])
    store_name = input('Enter the merchant\'s name: ')
    tran_count = cursor.execute(f"SELECT COUNT(*) FROM Transactions WHERE userID = '{user}'").fetchone()
    tranID = tran_count[0] + 1


    #SQL command to enter transaction here
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    add_transaction = f""" INSERT INTO transactions VALUES ('{user}', {tranID}, {amount}, CURRENT_TIMESTAMP, '{category}', '{store_name}')"""
    cursor.execute(add_transaction)
    connection.commit()
    connection.close()

    print(f'\nYour {category} transaction from {store_name} of ${amount:.2f} has been added')
    input('\nPress ENTER to continue')

def createNewInvestment(user):
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_investment = f""" SELECT * FROM Investments WHERE userID = '{user}' """
    if cursor.execute(get_investment).fetchone() is not None:
        print('You already have an investment. Use the UPDATE command to edit or delete it.')
        connection.close()
        input('\nPress ENTER to continue')
        return

    portfolioTotal = getValidInput('What is the portfolio size you have? $', decimal=True)
    riskScore = getValidInput('What is your preferred risk percent? (0-100 where 0 is not risky at all and 100 is as risky as possible) ', decimal=True)

    # SQL command to enter data here
    add_investment = f"""INSERT INTO Investments VALUES ('{user}', {portfolioTotal}, {riskScore})"""
    cursor.execute(add_investment)
    connection.commit()
    connection.close()
    print(f'\n{user}, your investment portfolio of ${portfolioTotal:.2f}, with risk percent {riskScore}% has been added.')
    input('\nPress ENTER to continue')


def updateIncome(user):
    """
    Updates the current user's income and returns the user object back
    """
    incomeType = getValidInput('Is your new income hourly or salaried? ', options=['hourly', 'salaried'])

    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()

    if incomeType == 'salaried':
        newIncome = getValidInput('What do you want to update your annual income to? ', decimal=True)
        if isAnnual(user):
            update_income = f""" UPDATE annual_income SET annual_pay = {newIncome} WHERE userID = '{user}'"""
            cursor.execute(update_income)
        else:
            delete_hourly = f""" DELETE FROM hourly_income WHERE userID = '{user}'"""
            cursor.execute(delete_hourly)
            add_salaried_user = f""" INSERT INTO annual_income VALUES ('{user}', {newIncome})"""
            cursor.execute(add_salaried_user)
        print(f'\nYour annual income has been updated to ${newIncome:.2f}')

    else:
        hourly_wage = getValidInput('\nEnter your new hourly pay: ', decimal=True)
        hours_worked = getValidInput('\nEnter your weekly hours worked: ', decimal=True)
        
        if isAnnual(user):
            delete_annual = f""" DELETE FROM annual_income WHERE userID = '{user}'"""
            cursor.execute(delete_annual)
            add_hourly_user = f""" INSERT INTO hourly_income VALUES ('{user}', {hourly_wage}, {hours_worked})"""
            cursor.execute(add_hourly_user)
        else:
            update_income = f""" UPDATE hourly_income SET hourly_wages = {hourly_wage}, hours_worked = {hours_worked} WHERE userID = '{user}'"""
            cursor.execute(update_income)
        print(f'Your hourly income has been updated to ${hourly_wage:.2f} with {hours_worked} hours a week.')
    
    connection.commit()
    connection.close()
    
    input('\nPress ENTER to continue')


def updateDebt(user):
    """
    Updates the current user's selected debt or deletes it
    """

    # retrieve types of debt where user.userID is the same, then put it as debtTypes list
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_debts = cursor.execute(f""" SELECT debt_type FROM Debt WHERE userID = '{user}' """).fetchall()
    debtTypes = [item[0] for item in get_debts]

    if len(debtTypes) == 0:
        print('You have no debts added. Create a new one to be able to update.')
        connection.close()
        input('\nPress ENTER to continue')
        return

    selectedType = getValidInput(f'Which debt type do you want to modify?\ncurrent debts: {", ".join(debtTypes)}\n', options=debtTypes, caseSensitive=True)

    # SQL command to retrieve debt instance of selectedType and put it into debt object
    selected_debt = f""" SELECT * FROM Debt WHERE userID = '{user}' AND debt_type = '{selectedType}'"""
    result = cursor.execute(selected_debt).fetchone()

    amount = result[1] # debt amount of selected type 
    print(f'We retrieved your {selectedType} debt of ${amount:.2f}\n')

    option = getValidInput('Do you want to change the debt amount, interest rate, minimum payment or simply delete it? ', 
                  options=['debt amount', 'amount', 'interest rate', 'min payment', 'minimum payment', 'delete'])
    
    if option == 'debt amount' or option == 'amount':
        newAmount = getValidInput('What amount should it be? ', decimal=True)

        # SQL command to update the new debt amount
        update_debt_amt = f""" UPDATE debt SET debt_amount = {newAmount} WHERE userID = '{user}' AND debt_type = '{selectedType}' """
        cursor.execute(update_debt_amt)

        print(f'Your {selectedType} debt amount has been successfully updated to ${newAmount:.2f}.')

    elif option == 'interest rate':
        newInterestRate = getValidInput('What is the new interest rate? ', decimal=True)

        # SQL command to update new interest rate
        update_interest_amount = f""" UPDATE debt SET interest_rate = {newInterestRate} WHERE userID = '{user}' AND debt_type = '{selectedType}' """
        cursor.execute(update_interest_amount)
        print(f'Your {selectedType} debt interest rate has been successfully updated to ${newInterestRate}%.')


    elif option == 'min payment' or option == 'minimum payment':
        newMinPayment = getValidInput('What is the new minimum payment? ', decimal=True)

        # SQL command to update new minimum payment
        update_min_amount = f""" UPDATE debt SET min_payment = {newMinPayment} WHERE userID = '{user}' AND debt_type = '{selectedType}' """
        cursor.execute(update_min_amount)
        print(f'Your {selectedType} debt minumum payment has been successfully updated to ${newMinPayment:.2f}.')

    elif option == 'delete':
        # SQL command to delete instance
        connection = sqlite3.connect('finances.db')
        cursor = connection.cursor()
        delete_debt = f""" DELETE FROM debt WHERE userID = '{user}' AND debt_type = '{selectedType}' """
        cursor.execute(delete_debt)

        print(f'Your {selectedType} debt has been successfully deleted.')
    
    connection.commit()
    connection.close()
    input('\nPress ENTER to continue')

def updateInvestments(user):
    """
    Updates the current user's selected investment or deletes it
    """
    # retrieves user's investment portfolio 
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_investment = f""" SELECT * FROM Investments WHERE userID = '{user}' """
    if cursor.execute(get_investment).fetchone() is None:
        print('You have no investments. Add an investment portfolio to continue.')
        connection.close()
        input('\nPress ENTER to continue')
        return

    option = getValidInput('Do you want to update your portfolio balance, change the risk score or simply delete the investment from your account? ', 
                  options=['portfolio balance', 'risk score', 'delete'])
    if option == 'portfolio balance':
        newBalance = getValidInput('What should the new balance be? ', decimal=True)

        # SQL command to update the new portfolio balance
        update_balance = f""" UPDATE Investments SET portfolio_total = {newBalance} WHERE userID = '{user}' """
        cursor.execute(update_balance)
        print(f'Your portfolio total has successfully been updated to ${newBalance:.2f}.')
    elif option == 'risk score':
        newScore = getValidInput('What is your new risk score? ', decimal=True)

        # SQL command to update the new risk score
        update_risk_score = f""" UPDATE Investments SET risk_score = {newScore} WHERE userID = '{user}' """
        cursor.execute(update_risk_score)
        print(f'Your risk score has successfully been updated to {newScore:.2f}%.')

    elif option == 'delete':
        # SQL command to delete instance
        delete_investment = f""" DELETE FROM Investments WHERE userID = '{user}' """
        cursor.execute(delete_investment)
        print(f'Your investment portfolio has successfully been deleted.')
    
    connection.commit()
    connection.close()
    input('\nPress ENTER to continue')

def updatePlannedPayments(user):
    """
    Updates the current user's selected planned payment or deletes it
    """  
    # retrieve the planned payment the use wants to alter
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_planned_payments = cursor.execute(f""" SELECT Title FROM planned_payments WHERE userID = '{user}' """).fetchall()
    pp = [item[0] for item in get_planned_payments]

    if len(pp) == 0:
        print('You do not have any planned payments. Add one to be able to update.\n')
        connection.close()
        input('\nPress ENTER to continue')

    selectedTitle = getValidInput(f'Which planned payment do you want to modify?\ncurrent planned payments: {", ".join(pp)}\n', options=pp, caseSensitive=True)

    option = getValidInput('Do you want to change the payment amount, due date, or simply delete it? ', 
                  options=['payment amount', 'amount', 'due date', 'date', 'delete'])
    
    if option == 'payment amount' or option == 'amount':
        newAmount = getValidInput('What is your new payment amount? ', decimal=True)

        # SQL command to update the payment amount
        update_payment_amt = f""" UPDATE Planned_payments SET Amount = {newAmount} WHERE userID = '{user}' AND title = '{selectedTitle}' """
        cursor.execute(update_payment_amt)

        print(f'Your planned payment, {selectedTitle}, has its amount successfully changed to ${newAmount:.2f}.')

    elif option == 'due date' or option == 'date':
        get_planned_payments = cursor.execute(f""" SELECT Recurring FROM planned_payments WHERE userID = '{user}' AND title='{selectedTitle}' """).fetchone()
        recurring = True if get_planned_payments[0] == 1 else False

        if recurring:
            newDate = getValidInput('What is the new day of the month? ', integer=True, intRange=[1, 31])

            # SQL command to update the due date  
            update_date = f""" UPDATE Planned_payments SET Date_by = '{newDate}' WHERE userID = '{user}' AND title = '{selectedTitle}' """
            cursor.execute(update_date)
            print(f'The date of your payment has successfully been updated to the {newDate} day of the month.')
        else:
            newDate = getValidInput('What is the new date of payment? ', isDate=True)

            # SQL command to update the due date  
            update_date = f""" UPDATE Planned_payments SET Date_by = '{newDate}' WHERE userID = '{user}' AND title = '{selectedTitle}' """
            cursor.execute(update_date)
            print(f'The date of your payment has successfully been updated to {newDate}.')

    elif option == 'delete':
        # SQL command to delete instance
        delete_planned_payment = f""" DELETE FROM planned_payments WHERE userID = '{user}' AND title = '{selectedTitle}' """
        cursor.execute(delete_planned_payment)
        print(f'Your planned payment has successfully been deleted.')
    
    connection.commit()
    connection.close()
    input('\nPress ENTER to continue')

def viewDebtPayoffTimeline(user):
    # retrieve types of debt where user.userID is the same, then put it as debtTypes list
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    get_debts = cursor.execute(f""" SELECT debt_type FROM Debt WHERE userID = '{user}' """).fetchall()
    debtTypes = [item[0] for item in get_debts]

    if len(debtTypes) == 0:
        print('You have no debts added. Create a new one to be able to see the timeline.')
        connection.close()
        input('\nPress ENTER to continue')
        return
    selectedType = getValidInput(f'Which debt type do you want to modify?\ncurrent debts: {", ".join(debtTypes)}\n', options=debtTypes, caseSensitive=True)
    
    get_debts = cursor.execute(f""" SELECT * FROM Debt WHERE userID = '{user}' AND debt_type = '{selectedType}' """).fetchone()
    connection.close()

    debtAmount = get_debts[1]
    debtType = get_debts[2]
    interestRate = get_debts[3]
    minPayment = get_debts[4]

    print(f'\nFor your {debtType} debt with a debt amount of ${debtAmount:.2f}, annual interest rate {interestRate}%, and minimum payment ${minPayment:.2f}:\n')

    totalMonths = 0
    totalPaid = 0
    while debtAmount > 0:
        monthlyInterest = debtAmount * interestRate/100
        debtAmount = debtAmount + monthlyInterest
        debtAmount = debtAmount - minPayment - monthlyInterest
        totalPaid += minPayment + monthlyInterest
        if debtAmount < 0:
            totalPaid += debtAmount
        totalMonths+=1
    
    print(f'It will take you {totalMonths} months, or {totalMonths/12:.2f} years and ${totalPaid:.2f} in total to\nfully pay off the {debtType} debt if you only pay the minimum payment plus monthly interest.')
    input('\nPress ENTER to continue')
    



def viewExpensesByCategory(user):
    """
    Returns sorted list of expenses
    """
    #SQL command
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    viewExpenses = f"""SELECT category, sum(amount)
                      FROM Transactions
                      WHERE userID = '{user}'
                      GROUP BY userID, category
                      ORDER BY sum(amount) DESC
                      """

    result = cursor.execute(viewExpenses).fetchall()
    connection.close()

    print(f'\nYour expenses in descending order are:\n ')
    for row in result:
        print(f'{row[0]}: ${row[1]}\n')
    input('\nPress ENTER to continue')

def viewBudget(user):
    """
    Returns budget table with combined income, savings, and expenses
    """
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()
    annualSalary = isAnnual(user)

    if annualSalary == True: 
        #SQL command to create budget for salary user
        viewBudget = f"""SELECT u.userID AS userID, ROUND(a.annual_pay/12, 2) AS monthlySalary, sum(t.amount) AS
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
                    WHERE u.userID = '{user}'
                    """

        result = cursor.execute(viewBudget).fetchone()
    else:
        #SQL command to create budget for hourly paid user
        viewBudget = f"""SELECT u.userID AS userID, ROUND(h.hourly_wages * h.hours_worked * 4, 2) AS monthlySalary, sum(t.amount) AS
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
                    WHERE u.userID = '{user}'
                    """
        result = cursor.execute(viewBudget).fetchone()
    
    monthly_salary = result[1] if result[1] is not None else 0
    total_transactions = result[2] if result[2] is not None else 0
    total_debt_payments = result[3] if result[3] is not None else 0
    total_planned_payments = result[4] if result[4] is not None else 0
    remaining_budget = monthly_salary - total_transactions - total_debt_payments - total_planned_payments

    insertBudget = f""" INSERT INTO Budget
    VALUES ('{user}', CURRENT_TIMESTAMP, {monthly_salary}, {total_transactions}, {total_debt_payments}, {total_planned_payments}, {remaining_budget})"""
    cursor.execute(insertBudget)
    connection.commit()
    connection.close()

    print(f'\nYour budget is:\n ')
    print(f'Monthly Salary: ${monthly_salary:.2f}')
    print(f'Total transactions from last month: ${total_transactions:.2f}')
    print(f'Total debt payments: ${total_debt_payments:.2f}')
    print(f'Total planned expenses: ${total_planned_payments:.2f}')
    print(f'Remaining estimated balance: ${remaining_budget:.2f}')
    input('\nPress ENTER to continue')

def isAnnual(user):
    #SQL command to check if a user is paid annually 
    connection = sqlite3.connect('finances.db')
    cursor = connection.cursor()

    check= f"SELECT COUNT(*) FROM annual_income WHERE userID = '{user}'"
    cursor.execute(check)
    count = cursor.fetchone()[0]
    connection.close()
    if count != 0:
        return True 
    else: 
        return False

class Debt:
    def __init__(self, userID, debt_amount, debt_type, interest_rate, min_payment):
        self.userID = userID
        self.debt_amount = debt_amount
        self.debt_type = debt_type
        self.interest_rate = interest_rate
        self.min_payment = min_payment

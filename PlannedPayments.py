class PlannedPayments:
    def __init__(self, userID, date_by, title, amount, recurring):
        self.userID = userID
        self.title = title
        self.date_by = date_by
        self.amount = amount
        self.recurring = recurring

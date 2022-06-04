import Loan

class Expenses:
  def __init__(self):
    self.total_debt = 0
    self.number_of_loans = 0
    self.total_montly_expenses = 0
  def add_loan(self, loan):
    self.number_of_loans += 1
    self.total_debt += loan.loan
    self.total_montly_expenses += loan.monthly_payments






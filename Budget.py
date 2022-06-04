import Loan

class Budget:
  def __init__(self, Loans=[]):
      self.Loans = Loans
      self.monthly_loan_payments = 0
      for loan in Loans:
        self.monthly_loan_payments += loan.monthly_payments
      self.monthly_income = 103000/12 
      self.dti = self.monthly_loan_payments/self.monthly_income
      self.after_tax = (2647.78*26)/12 + 1500
      self.expenses = self.after_tax - self.monthly_loan_payments


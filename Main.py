import numpy as np
import pandas as pd

class Loan:
  def __init__(self, name, loan, interest, years):

      self.name = name
      self.loan = loan
      self.interest = interest/100
      self.years = years
      
      self.total_recurring_payments = 0
      self.one_time_payments = []
      self.one_time_payments_months = []
      self.df = self.ammortization()

  def ammortization(self):
    a = self.loan
    r = self.interest / 12
    n = self.years * 12

    monthly_payment = a * (r*(1+r)**n) / ((1+r)**n - 1)
    first_month_interest = r*a
    first_month_principal = monthly_payment - first_month_interest

    interest_monthly = np.zeros(n)
    principal_monthly = np.zeros(n)
    loan_balance = np.full(n, a)
    monthly_payment_list = np.full(n, monthly_payment)

    interest_monthly[0] = first_month_interest
    principal_monthly[0] = first_month_principal


    for i in range(1, n):
      if self.one_time_payments != []:
        if i in self.one_time_payments_months:
          loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments - self.one_time_payments[self.one_time_payments_months.index(i)]
          if loan_balance[i] <= 0:
            loan_balance[i] = 0
            interest_monthly[i] = 0
            principal_monthly[i] = 0
          else:
            interest_monthly[i] = r*loan_balance[i]
            principal_monthly[i] = monthly_payment - interest_monthly[i]
        else:
          loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments
          if loan_balance[i] <= 0:
            loan_balance[i] = 0
            interest_monthly[i] = 0
            principal_monthly[i] = 0
          else:
            interest_monthly[i] = r*loan_balance[i]
            principal_monthly[i] = monthly_payment - interest_monthly[i]
      else:
        loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments
        if loan_balance[i] <= 0:
          loan_balance[i] = 0
          interest_monthly[i] = 0
          principal_monthly[i] = 0
        else:
          interest_monthly[i] = r*loan_balance[i]
          principal_monthly[i] = monthly_payment - interest_monthly[i]

    month_num = np.zeros(n)
    for i in range(n):
      month_num[i] = i+1
    df_initialize = list(zip(month_num, interest_monthly, principal_monthly, loan_balance, monthly_payment_list))

    df = pd.DataFrame(df_initialize, columns=['month', 'interest','principal', 'loan balance', 'monthly_payment'])

    return df

  def add_recurring_payment(self, amount):
    self.total_recurring_payments += amount
    self.df = self.ammortization()

  def add_one_time_payment(self, amount, month_paid):
    self.one_time_payments.append(amount)
    self.one_time_payments_months.append(month_paid)
    self.df = self.ammortization()

  def find_zero(self):
    arr = np.zeros((self.years*12, 2))
    for i in range(self.years*12):
      arr[i][0] = i
      arr[i][1] = self.df['loan balance'][i]
      if arr[i][1] <= 0:
        if self.total_recurring_payments != 0:
          print("Total amount of recurring payment = " + str(self.total_recurring_payments*arr[i][0]))
        return self.name + " loan will be paid off in " + str(arr[i][0]) + " months or " + str(arr[i][0] / 12) + " years. This is " + str(self.years*12 - arr[i][0]) + " months and " + str(self.years - (arr[i][0] / 12)) + " years less."
    return self.name + " loan will be paid off in " + str(self.years) + " years"

  def export_ammort_table(self):
    self.df.to_csv("./" + self.name + ".csv")


house = Loan("house", 327750, 2.625, 30)

condo = Loan("condo", 185000, 6.7, 20)
condo.add_recurring_payment(500)
condo.add_one_time_payment(10000, 1)
condo.add_one_time_payment(10000, 12)

condo.export_ammort_table()






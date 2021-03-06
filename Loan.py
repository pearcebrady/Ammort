import numpy as np
import pandas as pd

class Loan:
  def __init__(self, name, loan, interest, years):

    self.name = name
    self.loan = loan
    self.interest = interest/100
    self.years = years
    
    self.monthly_payments = 0
    self.total_recurring_payments = 0
    self.total_interest = 0
    self.one_time_payments = []
    self.one_time_payments_months = []
    self.df = self.ammortization()
    print(self.name + ' loan for ' + str(self.years) + ' years with payments of ' + str(self.monthly_payments) + ' per month and a total interest paid of ' + str(self.total_interest))

  def ammortization(self):
    a = self.loan
    r = self.interest / 12
    n = self.years * 12

    monthly_payment = round(a * (r*(1+r)**n) / ((1+r)**n - 1),2)
    first_month_interest = r*a
    first_month_principal = monthly_payment - first_month_interest

    interest_monthly = np.zeros(n)
    principal_monthly = np.zeros(n)
    loan_balance = np.full(n, float(a))
    monthly_payment_list = np.full(n, monthly_payment)
    total_interest = np.zeros(n)

    interest_monthly[0] = round(first_month_interest, 2)
    principal_monthly[0] = round(first_month_principal,2)
    total_interest[0] = interest_monthly[0]


    for i in range(1, n):
      if self.one_time_payments != []:
        if i in self.one_time_payments_months:
          loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments - self.one_time_payments[self.one_time_payments_months.index(i)]
          if loan_balance[i] <= 0:
            loan_balance[i] = 0
            interest_monthly[i] = 0
            principal_monthly[i] = 0
            total_interest[i] = 0
          else:
            interest_monthly[i] = round(r*loan_balance[i], 2)
            total_interest[i] = total_interest[i-1] + interest_monthly[i]
            principal_monthly[i] = round(monthly_payment - interest_monthly[i],2)
        else:
          loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments
          if loan_balance[i] <= 0:
            loan_balance[i] = 0
            interest_monthly[i] = 0
            principal_monthly[i] = 0
            total_interest[i] = 0
          else:
            interest_monthly[i] = round(r*loan_balance[i], 2)
            total_interest[i] = total_interest[i-1] + interest_monthly[i]
            principal_monthly[i] = round(monthly_payment - interest_monthly[i],2)
      else:
        loan_balance[i] = loan_balance[i-1] - principal_monthly[i-1] - self.total_recurring_payments
        if loan_balance[i] <= 0:
          loan_balance[i] = 0
          interest_monthly[i] = 0
          principal_monthly[i] = 0
          total_interest[i] = 0
        else:
          interest_monthly[i] = round(r*loan_balance[i], 2)
          total_interest[i] = total_interest[i-1] + interest_monthly[i]
          principal_monthly[i] = round(monthly_payment - interest_monthly[i],2)

    month_num = np.zeros(n)
    for i in range(n):
      month_num[i] = i+1
    df_initialize = list(zip(month_num, interest_monthly, principal_monthly, loan_balance, total_interest, monthly_payment_list))

    df = pd.DataFrame(df_initialize, columns=['month', 'interest','principal', 'loan balance', 'total_interest', 'monthly_payment'])

    self.monthly_payments = monthly_payment
    self.total_interest = total_interest[n-1]

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
        return self.name + " loan will be paid off in " + str(arr[i][0]) + " months or " + str(round(arr[i][0] / 12,2)) + " years. This is " + str(self.years*12 - arr[i][0]) + " months and " + str(round(self.years - (arr[i][0] / 12), 2)) + " years less."
    return self.name + " loan will be paid off in " + str(self.years) + " years"

  def export_ammort_table(self):
    self.df.to_csv("./" + self.name + ".csv")
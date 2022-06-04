import Loan
import Budget
import Expenses
import subprocess

home = Loan.Loan("House", 327750, 2.625, 30)
condo = Loan.Loan("Condo", 185000, 6.7, 20)
car = Loan.Loan("Prius Prime", 36904.72, 2.5, 6)

condo.add_one_time_payment(10000, 1)
condo.add_recurring_payment(2000)

total = Budget.Budget([home, condo, car])


print(condo.find_zero())
condo.export_ammort_table()
subprocess.run(["open", condo.name + ".csv"])
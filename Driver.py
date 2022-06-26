import Loan
import Budget
import Expenses
import subprocess

condo = Loan.Loan("Condo", 185000, 6.7, 20)

condo.add_one_time_payment(10000, 1)
condo.add_recurring_payment(2000)

print(condo.find_zero())
condo.export_ammort_table()
subprocess.run(["open", condo.name + ".csv"])
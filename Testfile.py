import Loan
from flask import Flask, request, render_template
from IPython.display import HTML

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def Ammort():
  if request.method == "POST":
    name_of_loan = request.form.get("loan_name")
    total_mortgage = float(request.form.get("mort"))
    interest = float(request.form.get("int"))
    years = int(request.form.get("years"))
    recurring = int(request.form.get("recurring"))
    one_pay = float(request.form.get("one_amount"))
    one_time = int(request.form.get("one_month"))

    loan = Loan.Loan(name_of_loan, total_mortgage, interest, years)
    loan.add_recurring_payment(recurring)
    loan.add_one_time_payment(10000, 1)

    msg = loan.find_zero()

    return f"<h1>{msg}</h1>" + loan.df.to_html()
  return render_template("form.html")

app.run()
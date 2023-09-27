from .models import Transaction
from datetime import date, timedelta

def calculate_emi(loan_amount, interest_rate, term_period):
    term_period = float(term_period)
    interest_rate = float(interest_rate)
    try:
        interest_rate = float(interest_rate)

        r = (interest_rate / 12) / 100  # Monthly interest rate
        n = term_period  # Total number of months

        emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return emi
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid loan parameters. Please ensure loan_amount, interest_rate, and term_period are numeric.") from e


def update_status(loan, amount):
    remaining_balance = float(loan.loan_amount) - float(amount)
    is_closed = remaining_balance <= 0

    # Updating loan status and loan_amount
    loan.loan_amount = remaining_balance
    loan.is_closed = is_closed
    loan.save()




def generate_loan_statement(loan):
    statement_data = {
        "past_transactions": [],
        "upcoming_transactions": []
    }

    next_due_date = loan.disbursement_date.replace(day=1) + timedelta(days=30)

    for transaction in Transaction.objects.filter(user=loan.user, date__lt=date.today()):
        statement_data["past_transactions"].append({
            "Date": transaction.date,
            "Principal": loan.emi_amount,  
            "Interest": (float(loan.loan_amount) * float(loan.interest_rate) / 12 / 100),  
            "Amount_paid": transaction.amount
        })

    while next_due_date < date.today() and not loan.is_closed:
        statement_data["upcoming_transactions"].append({
            "Date": next_due_date,
            "Amount_due": loan.emi_amount
        })
        next_due_date += timedelta(days=30)

    return statement_data

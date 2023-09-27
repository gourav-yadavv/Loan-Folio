from django.db import models
import uuid

class User(models.Model):
    aadhar_id = models.CharField(unique=True, max_length=12)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.PositiveIntegerField(default=0)

class Loan(models.Model):
    LOAN_TYPES = [
        ('Car', 'Car'),
        ('Home', 'Home'),
        ('Education', 'Education'),
        ('Personal', 'Personal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.PositiveIntegerField(default= 4)
    disbursement_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_closed = models.BooleanField(default=False)


class Transaction(models.Model):
    user = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateField()
    transaction_type = models.CharField(max_length=6, choices=[('DEBIT', 'DEBIT'), ('CREDIT', 'CREDIT')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)


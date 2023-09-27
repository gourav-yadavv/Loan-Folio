
from django.contrib import admin
from .models import User, Loan, Transaction 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'annual_income', 'credit_score')
    search_fields = ('name', 'email')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date', 'emi_amount', 'is_closed')
    list_filter = ('loan_type', 'is_closed')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'transaction_type', 'amount')
    list_filter = ('transaction_type',)

# loans/tasks.py
from celery import shared_task
from .models import User, Transaction
import logging

logger = logging.getLogger(__name__)

@shared_task
def calculate_credit_score(aadhar_id, annual_income):
    logger.info(f"Calculating credit score for aadhar id {aadhar_id} with annual income {annual_income}")
    annual_income = int(annual_income)
    print('Calculate credit score function called.')
    try:
        user = User.objects.get(aadhar_id=aadhar_id)
        
        if annual_income >= 1000000:
            credit_score = 900  # Maximum credit score
        elif annual_income <= 100000:
            credit_score = 300  # Minimum credit score
        else:
            # For intermediate income values, adjust credit score by 10 points for every Rs. 15,000 change
            credit_score = 300 + ((annual_income - 100000) // 15000) * 10
        
        user.credit_score = credit_score
        user.save()

        print("Credit score calculated successfully.") 
        return user.credit_score
    except User.DoesNotExist:
        print("User not found.")
        return 0

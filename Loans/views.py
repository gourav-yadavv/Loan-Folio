from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Loan, Transaction
from django.utils import timezone
from django.db import IntegrityError
import uuid 
# from celery.result import AsyncResult
from django.http import JsonResponse
from .models import Loan


from .tasks import calculate_credit_score
from .utils import calculate_emi,update_status,generate_loan_statement

@api_view(['POST'])
def register_user(request):
    # print("hello received")
    if request.method == 'POST':
        data = request.data
        aadhar_id = data.get('aadhar_id')
        name = data.get('name')
        email = data.get('email')
        annual_income = data.get('annual_income')

        # Calculate credit score synchronously
        # credit_score = calculate_credit_score(aadhar_id, annual_income)
        # print({'New user created and initial credir score is : '},credit_score)
        # Create a new User instance and save it to the database
        user = User.objects.create(
            aadhar_id=aadhar_id,
            name=name,
            email=email,
            annual_income=annual_income,
            credit_score = 50
        )
        print(user)

        # Calculating credit score synchronously
        credit_score = calculate_credit_score(aadhar_id, annual_income)
            
        # Updating the user's credit score
        user.credit_score = credit_score
        user.save()

        # Triggering the Celery task to calculate credit score asynchronously
        calculate_credit_score.apply_async((user.id, annual_income))


        # return Response({"message": "User registration initiated, credit score calculation in progress."}, status=status.HTTP_200_OK)
        return Response({"message": "User registration successful.", "unique_user_id": user.id}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def apply_loan(request):
    if request.method == 'POST':
        data = request.data
        unique_user_id = data.get('unique_user_id')
        loan_type = data.get('loan_type')
        loan_amount = data.get('loan_amount')
        interest_rate = data.get('interest_rate')
        term_period = data.get('term_period')
        disbursement_date = data.get('disbursement_date')
        loan_amount = float(loan_amount)
        term_period
        print({'this is time period'},term_period)

        try:
            user = User.objects.get(id=unique_user_id)
            if user.credit_score >= 0 and user.annual_income >= 150000:
                
                max_loan_amount = {
                    'Car': 750000,
                    'Home': 8500000,
                    'Education': 5000000,
                    'Personal': 1000000
                }.get(loan_type)
                if loan_amount <= max_loan_amount:
                    
                    emi_amount = calculate_emi(loan_amount, interest_rate, term_period)
                    
                    Loan.objects.create(
                        user=user,
                        loan_type=loan_type,
                        loan_amount=loan_amount,
                        interest_rate=interest_rate,
                        term_period=term_period,
                        disbursement_date=disbursement_date,
                        emi_amount=emi_amount
                    )
                    return Response({"message": "Loan application successful."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Loan amount exceeds the allowed limit for the loan type."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "User is not eligible for the loan."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def make_payment(request):
    if request.method == 'POST':
        
        data = request.data
        loan_id = int(data.get('loan_id'))
        amount = float(data.get('amount'))
        transaction_type = data.get('transaction_type')

        
        try:
            
            loan = Loan.objects.get(id=loan_id)
            user = loan.user

            transaction = Transaction.objects.create(
                user = user.id,
                amount=amount,
                date=timezone.now(), 
                transaction_type = transaction_type,
            )

            update_status(loan, transaction.amount)

            return Response({"message": "Payment successful."}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"message": "Loan not found."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_statement(request):
    if request.method == 'GET':
        loan_id = request.query_params.get('loan_id')
        
        try:
            loan = Loan.objects.get(id=loan_id)
            user = loan.user

            if loan.is_closed:
                return Response({"message": "Loan is closed."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"loan_statement": generate_loan_statement(loan)}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"message": "Loan not found."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)


def all_loans(request):
    loans = Loan.objects.all()

    # Serializing the loan data into a JSON response
    loan_data = []
    for loan in loans:
        loan_data.append({
            'id': loan.id,
            'user': loan.user.aadhar_id,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'term_period': loan.term_period,
            'is_closed': loan.is_closed,
        })
    print(loans)
    return JsonResponse({'loans': loan_data})

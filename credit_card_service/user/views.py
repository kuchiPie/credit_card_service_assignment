from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from user.models import User, Loan
from repayment.models import Transaction, Payment
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta



class RegisterUserView(APIView):

    def validate_data(self, data):
        return data['name'], data['aadhar_id'], data['email_id'], data['annual_income']

    def handle_exception(self, exc):
        if isinstance(exc, KeyError):
            return Response(
                data='Invalid data: ' + exc.__str__(),
                status=status.HTTP_400_BAD_REQUEST
                )
        return super().handle_exception(exc)

    def post(self, request):
        data = json.loads(request.body)
        
        name, aadhar_number, email, annual_income = self.validate_data(data)
        user = User(
            name=name,
            aadhar_number=aadhar_number,
            email=email,
            annual_income=annual_income
        )
        user.save()
        # celery task to calculate credit score

        return Response(
                data={
                    'user_id': str(user.user_id)
                },
                status=status.HTTP_201_CREATED
            )

class ApplyLoanView(APIView):
    
    def validate_data(self, data):
        return data['user_id'], data['loan_type'], data['loan_amount'], data['interest_rate'], data['term_period'], data['disbursement_date']

    def handle_exception(self, exc):
        if isinstance(exc, KeyError):
            return Response(
                data='Invalid data: ' +  exc.__str__(),
                status=status.HTTP_400_BAD_REQUEST
                )
        if isinstance(exc, ObjectDoesNotExist):
            return Response(
                data='Does Not Exist: ' + exc.__str__(),
                status=status.HTTP_400_BAD_REQUEST
                )
        if isinstance(exc, ValueError):
            return Response(
                data='Invalid details: ' + exc.__str__(),
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)

    def post(self, request):
        data = json.loads(request.body)
        
        user_id, loan_type, loan_amount, interest_rate, term_period, disbursement_date = self.validate_data(data)

        user = User.objects.get(user_id=user_id)

        if user.credit_score < 450:
            raise ValueError('Credit Score is too low')
        if user.annual_income < 150000:
            raise ValueError('Annual Income is too low')
        if loan_amount > 5000:
            raise ValueError('Loan Amount is too high')
        if interest_rate < 12:
            raise ValueError('Interest Rate is too low')
        if loan_amount/term_period > user.annual_income * 0.2:
            raise ValueError('EMI is too high')
        cumulative_interest = round(interest_rate / 365, 3) * 30 * loan_amount / 100
        if cumulative_interest <= 50:
            raise ValueError('Cumulative Interest is too low', cumulative_interest)
        
        disbursement_date = datetime.strptime(disbursement_date, '%d-%m-%Y')

        loan = Loan(
            user=user,
            loan_amount=loan_amount,
            loan_type=loan_type,
            interest_rate=interest_rate,
            term_period=term_period,
            disbursement_date=disbursement_date,
            principal_balance=loan_amount
        )

        loan.save()
        current_principal_balance = loan_amount

        if disbursement_date.day < user.billing_day:
            billing_date = datetime(disbursement_date.year, disbursement_date.month, user.billing_day)
        else:
            billing_date = datetime(
                disbursement_date.year if disbursement_date.month != 12 else disbursement_date.year+1, 
                disbursement_date.month+1 if disbursement_date.month != 12 else 1, 
                user.billing_day)
        
        last_billing_date = disbursement_date

        due_dates = []

        for _ in range(term_period):

            days_of_interest = (billing_date - last_billing_date).days
            interest_accured = round(interest_rate / 365, 3) * days_of_interest * current_principal_balance / 100 
            due_date = billing_date + timedelta(days=15)

            emi_amount = round(loan_amount/term_period + interest_accured)
            payment = Payment(
                loan = loan,
                emi_amount = emi_amount,
                total_paid = 0,
                due_date = due_date,
                status = "NOT_DUE"
            )
            due_dates.append([due_date, emi_amount])
            current_principal_balance = current_principal_balance - (loan_amount/term_period)
            last_billing_date = billing_date
            new_month = billing_date.month+1 if billing_date.month != 12 else 1
            new_year = billing_date.year if billing_date.month != 12 else billing_date.year+1
            billing_date = datetime(
                new_year, 
                new_month, 
                user.billing_day
            )            
            payment.save()
        
        response_data = {
            'loan_id': str(loan.loan_id),
            'due_dates': due_dates
        }

        return Response(
                data=response_data,
                status=status.HTTP_201_CREATED
            )
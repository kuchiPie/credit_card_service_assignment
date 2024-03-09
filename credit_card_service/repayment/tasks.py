import pandas as pd
from celery import shared_task
from credit_card_service.celery import app
import datetime
from django.db.models import Q

def get_users_billing_day(day):
    from user.models import User
    return User.objects.filter(billing_day=int(day))

def billing_process(loan, name, date):
    # Check if last payment done or not?
    # update status of next payment to DUE from NOT_DUE
    # create billing details and due payments csv file 
    print('started billing process for', loan, name, date)
    from repayment.models import Payment
    from repayment.serializers import PaymentSerializer

    if len(Payment.objects.filter(loan=loan.loan_id, status='DUE')) != 0:
        loan.loan_status = "STOPPED"
        loan.save()
    
    next_payment = Payment.objects.filter(loan=loan.loan_id, status='NOT_DUE')[0]
    next_payment.status = 'DUE'
    next_payment.save()

    billed_payments = Payment.objects.filter(Q(loan=loan.loan_id) & (Q(status="COMPLETED") | Q(status="PARTIALLY_COMPLETED")))
    serialized_billed_payments = PaymentSerializer(billed_payments, many=True).data
    print(serialized_billed_payments)
    billed_payments_df = pd.DataFrame(serialized_billed_payments)
    billed_payments_df.to_csv('./data/billed_payments_' + name + '_' + date + '.csv')
    

    due_payments = Payment.objects.filter(Q(loan=loan.loan_id) & (Q(status="DUE") | Q(status="NOT_DUE")))
    serialized_due_payments = PaymentSerializer(due_payments, many=True).data
    print(serialized_due_payments)
    due_payments_df = pd.DataFrame(serialized_due_payments)
    due_payments_df.to_csv('./data/due_payments_' + name + '_' + date + '.csv')
    
@app.task
def billing_queue():
    print('Billing Queue Started')
    from user.models import User, Loan
    now = datetime.datetime.now()
    month_day = now.day
    users = get_users_billing_day(month_day)
    print("Users For Today:", users)

    for user in users:
        name = user.name
        loans = Loan.objects.filter(user=user.user_id)
        print("loans for:", user.name, loans)
        for loan in loans:
            billing_process(loan, name, str(now.day) + '-' +  str(now.month) + '-' + str(now.year))

@shared_task
def update_next_emis(loan_id):
    # will be called when the user pays more than 
    # total_due and principal balance changes
    # and next emis need to be re calculated.
    from user.models import Loan
    from repayment.models import Payment

    loan = Loan.objects.get(loan_id=loan_id)
    print('Current Principal Balance When Extra Payment was done:', loan.principal_balance)
    interest_rate = loan.interest_rate

    current_principal_balance = loan.principal_balance

    # Fetch ALL not due payments
    payments = Payment.objects.filter(loan=loan_id, status="NOT_DUE")
    today = datetime.datetime.now()
    print(loan.user.billing_day, today.month, today.year)
    if today.day > loan.user.billing_day:
        last_billing_date = datetime.datetime(day=loan.user.billing_day, month=today.month, year=today.year)
    else:
        new_month = today.month - 1 if today.month != 1 else 12
        new_year = today.year if today.month != 1 else today.year - 1
        last_billing_date = datetime.datetime(day=loan.user.billing_day, month=new_month, year=new_year)
    
    constant_part_emi = round(current_principal_balance / len(payments))
    print("constant_part_emi: ",constant_part_emi)

    for payment in payments:
        due_date = datetime.datetime.combine(payment.due_date, datetime.datetime.min.time())
        duration = (due_date - datetime.timedelta(days=15)) - last_billing_date
        days_of_interest = duration.days
        interest_accured = round(round(interest_rate / 365, 3) * days_of_interest * current_principal_balance / 100) 
        payment.emi_amount = constant_part_emi + interest_accured
        current_principal_balance -= payment.emi_amount
        payment.save()



    


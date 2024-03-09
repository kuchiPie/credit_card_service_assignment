import pandas as pd
from celery import shared_task

df = pd.read_csv('./user/transactions.csv')

def calculate_credit_score(aadhar_id):
    
    cur_df = df.loc[df['aadhar_id'] == aadhar_id]

    if len(cur_df) == 0: # User not found
        return -1

    total_credit = cur_df['credit'].sum()
    total_debit = cur_df['debit'].sum()

    account_balance = total_credit - total_debit

    if account_balance >= 1000000:
        return 900
    if account_balance <= 10000:
        return 300

    credit_score = 300 +  (account_balance - 10000) // 1500

    return credit_score

@shared_task()
def update_credit_score(aadhar_id):
    credit_score = calculate_credit_score(aadhar_id)
    from .models import User
    user = User.objects.get(aadhar_number = aadhar_id)
    user.credit_score = credit_score
    user.save()




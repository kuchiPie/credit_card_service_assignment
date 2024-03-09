from django.db import models
import uuid
from datetime import timedelta
from user.tasks import update_credit_score

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    annual_income = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    billing_day = models.IntegerField(default=1)
    credit_score = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        billing_date = self.created + timedelta(days=30)
        self.billing_day = billing_date.day % 28
        super().save(*args, **kwargs)
        if self.credit_score == -1:
            update_credit_score.delay(int(self.aadhar_number))

class Loan(models.Model):

    LOAN_TYPES = (("Home Loan", "Home Loan"), ("Personal Loan","Personal Loan"), ("Car Loan", "Car Loan"))

    LOAN_STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("STOPPED", "STOPPED"), # If min due is not paid for some month
        ("REPAID", "REPAID")
    )

    loan_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=100)
    interest_rate = models.FloatField()
    term_period = models.IntegerField()
    disbursement_date = models.DateField()
    principal_balance = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    loan_status = models.CharField(choices=LOAN_STATUS, max_length=100, default='ACTIVE')
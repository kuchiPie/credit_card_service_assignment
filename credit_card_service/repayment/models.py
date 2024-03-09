from django.db import models
import uuid

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    loan = models.ForeignKey('user.Loan', on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Payment(models.Model):

    PAYMENT_STATUS = (
        ("COMPLETED", "COMPLETED"), 
        ("PARTIALLY_COMPLETED", "PARTIALLY_COMPLETED"), # In this case we will increase the total principal balance. This case also include incomplete payment.
        ("DUE", "DUE"),
        ("NOT_DUE", "NOT_DUE")
        )

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    loan = models.ForeignKey('user.Loan', on_delete=models.CASCADE)
    emi_amount = models.IntegerField()
    total_paid = models.IntegerField(default=0)
    due_date = models.DateField()
    status = models.CharField(choices=PAYMENT_STATUS, max_length=100)

    class Meta:
        ordering = ['due_date']


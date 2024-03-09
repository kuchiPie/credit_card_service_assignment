from django.contrib import admin
from .models import Payment, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'emi_amount', 'total_paid', 'due_date', 'status')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount', 'created')


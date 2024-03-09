from django.contrib import admin
from user.models import User, Loan

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'aadhar_number', 'email', 'annual_income', 'created', 'billing_day', 'credit_score')

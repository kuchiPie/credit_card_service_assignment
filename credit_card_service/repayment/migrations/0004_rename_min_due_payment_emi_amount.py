# Generated by Django 5.0 on 2023-12-12 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repayment', '0003_payment_total_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='min_due',
            new_name='emi_amount',
        ),
    ]

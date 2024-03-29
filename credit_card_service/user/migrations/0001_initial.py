# Generated by Django 5.0 on 2023-12-12 08:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('aadhar_number', models.CharField(max_length=12, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('annual_income', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('loan_amount', models.IntegerField()),
                ('loan_type', models.CharField(choices=[('Home Loan', 'Home Loan'), ('Personal Loan', 'Personal Loan'), ('Car Loan', 'Car Loan')], max_length=100)),
                ('interest_rate', models.FloatField()),
                ('term_period', models.IntegerField()),
                ('disbursement_date', models.DateField()),
                ('principal_balance', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]

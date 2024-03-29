# Generated by Django 5.0 on 2023-12-12 08:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('emi_amount', models.IntegerField()),
                ('min_due', models.IntegerField()),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('PARTIALLY_COMPLETED', 'PARTIALLY_COMPLETED'), ('DUE', 'DUE'), ('NOT_DUE', 'NOT_DUE')], max_length=100)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.loan')),
            ],
            options={
                'ordering': ['-due_date'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.loan')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]

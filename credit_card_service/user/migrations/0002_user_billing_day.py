# Generated by Django 5.0 on 2023-12-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='billing_day',
            field=models.IntegerField(default=1),
        ),
    ]

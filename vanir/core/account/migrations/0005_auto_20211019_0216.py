# Generated by Django 3.1.13 on 2021-10-19 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_extended_exchange'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.AlterField(
            model_name='account',
            name='api_key',
            field=models.CharField(default='None', help_text="API key for the exchange, do not touch if you're adding a manual exchange", max_length=250),
        ),
        migrations.AlterField(
            model_name='account',
            name='secret',
            field=models.CharField(default='None', help_text="API secret for the exchange, do not touch if you're adding a manual exchange", max_length=250),
        ),
    ]

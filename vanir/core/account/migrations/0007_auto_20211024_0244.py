# Generated by Django 3.2.8 on 2021-10-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttokens',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historicalaccounttokens',
            name='id',
            field=models.BigIntegerField(blank=True, db_index=True),
        ),
    ]

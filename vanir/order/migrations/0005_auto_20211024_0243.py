# Generated by Django 3.2.8 on 2021-10-24 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20211018_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limitorder',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='marketorder',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stoplossortakeprofitlimitorder',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stoppriceorder',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]

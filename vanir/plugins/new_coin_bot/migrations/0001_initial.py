# Generated by Django 3.1.13 on 2021-10-02 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BinanceNewToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('symbol', models.CharField(max_length=6, unique=True)),
                ('last_value', models.FloatField(null=True)),
                ('listing_day', models.DateTimeField(null=True)),
                ('announcement_seen', models.IntegerField(null=True)),
                ('discovered_method', models.CharField(choices=[('Binance Scrapper', 'Binance Scrapper'), ('Manual', 'Manual'), ('Other', 'Other')], default='Binance Scrapper', max_length=25)),
            ],
            options={
                'abstract': False,
                'unique_together': {('name', 'symbol')},
            },
        ),
    ]
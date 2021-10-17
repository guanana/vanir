# Generated by Django 3.1.13 on 2021-10-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newcoinconfig',
            name='activate_scheduler',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newcoinconfig',
            name='scrapper_class',
            field=models.CharField(choices=[('ScrapBinanceModel', 'Binance Scrapper')], default='', max_length=100, unique=True, verbose_name='Scrapper'),
            preserve_default=False,
        ),
    ]
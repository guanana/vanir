# Generated by Django 3.1.13 on 2021-10-06 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20211003_2119'),
        ('token', '0002_load_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='StopLossOrTakeProfitLimitOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('order_id', models.CharField(editable=False, max_length=250)),
                ('side', models.CharField(choices=[('BUY', 'Side Buy'), ('SELL', 'Side Sell')], max_length=4)),
                ('quoteOrderQty', models.FloatField(default=0.1)),
                ('price', models.FloatField(default=0, help_text='Price at which you want to buy/sell')),
                ('timeInForce', models.CharField(choices=[('GTC', 'Good Till Cancel'), ('IOC', 'Immediate Or Cancel'), ('FOK', 'Fill Or Kill')], help_text='Time in force indicates how long your order will remain active before it is executed or expired', max_length=4)),
                ('stopprice', models.FloatField(default=0, help_text='STOP_LOSS and TAKE_PROFIT will execute a MARKET order when the stopPrice is reached')),
                ('ORDER_TYPE', models.CharField(choices=[('STOP_LOSS_LIMIT', 'Order Type Stop Loss Limit'), ('TAKE_PROFIT_LIMIT', 'Order Type Take Profit Limit')], help_text='STOP_LOSS and TAKE_PROFIT will execute a MARKET order when the stopPrice is reached', max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('token_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_from_loss_or_take', to='token.token')),
                ('token_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_to_loss_or_take', to='token.token')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LimitOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('order_id', models.CharField(editable=False, max_length=250)),
                ('side', models.CharField(choices=[('BUY', 'Side Buy'), ('SELL', 'Side Sell')], max_length=4)),
                ('quoteOrderQty', models.FloatField(default=0.1)),
                ('price', models.FloatField(default=0, help_text='Price at which you want to buy/sell')),
                ('timeInForce', models.CharField(choices=[('GTC', 'Good Till Cancel'), ('IOC', 'Immediate Or Cancel'), ('FOK', 'Fill Or Kill')], help_text='Time in force indicates how long your order will remain active before it is executed or expired', max_length=4)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('token_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_from_limit', to='token.token')),
                ('token_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_to_limit', to='token.token')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StopPriceOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('order_id', models.CharField(editable=False, max_length=250)),
                ('side', models.CharField(choices=[('BUY', 'Side Buy'), ('SELL', 'Side Sell')], max_length=4)),
                ('quoteOrderQty', models.FloatField(default=0.1)),
                ('stopprice', models.FloatField(default=0, help_text='Price at which you want to buy/sell')),
                ('ORDER_TYPE', models.CharField(choices=[('STOP_LOSS', 'Order Type Stop Loss'), ('TAKE_PROFIT', 'Order Type Take Profit')], help_text='STOP_LOSS and TAKE_PROFIT will execute a MARKET order when the stopPrice is reached', max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('token_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_from_stop_price', to='token.token')),
                ('token_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_to_stop_price', to='token.token')),
            ],
            options={
                'abstract': False,
                'unique_together': {('order_id', 'account')},
            },
        ),
        migrations.CreateModel(
            name='MarketOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('order_id', models.CharField(editable=False, max_length=250)),
                ('side', models.CharField(choices=[('BUY', 'Side Buy'), ('SELL', 'Side Sell')], max_length=4)),
                ('quoteOrderQty', models.FloatField(default=0.1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('token_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_from_market', to='token.token')),
                ('token_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_to_market', to='token.token')),
            ],
            options={
                'abstract': False,
                'unique_together': {('order_id', 'account')},
            },
        ),
    ]

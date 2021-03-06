# Generated by Django 3.1.13 on 2021-10-03 21:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('token', '0002_load_data'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttokens',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accounttokens',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='accounttokens',
            unique_together={('account', 'token')},
        ),
        migrations.RemoveField(
            model_name='accounttokens',
            name='blockchain',
        ),
        migrations.RemoveField(
            model_name='accounttokens',
            name='update_time',
        ),
    ]

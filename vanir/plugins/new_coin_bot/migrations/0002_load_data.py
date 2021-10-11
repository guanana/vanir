from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    print('Forwards')
    call_command('loaddata', 'initial_new_coin_bot_config_data.yaml')


def reverse_func(apps, schema_editor):
    print('Reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('new_coin_bot', '0001_initial')
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]

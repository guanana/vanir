from django.db import migrations
from django.core.management import call_command


def forwards_func(apps, schema_editor):
    print('Forwards')
    call_command('loaddata', 'initial_token_data.yaml')


def reverse_func(apps, schema_editor):
    print('Reverse')


class Migration(migrations.Migration):
    dependencies = [
        ('token', '0001_initial'),
        ('blockchain', '0002_load_data'),
    ]
    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=False)
    ]

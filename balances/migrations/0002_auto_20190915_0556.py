# Generated by Django 2.2.1 on 2019-09-15 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balances', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Balance',
            new_name='DailyBalance',
        ),
    ]

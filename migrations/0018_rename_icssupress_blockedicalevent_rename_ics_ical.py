# Generated by Django 4.1.7 on 2023-06-11 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0017_remove_icssupress_ics_icssupress_name_alter_ics_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IcsSupress',
            new_name='BlockedIcalEvent',
        ),
        migrations.RenameModel(
            old_name='Ics',
            new_name='ICal',
        ),
    ]
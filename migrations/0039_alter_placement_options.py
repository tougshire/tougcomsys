# Generated by Django 4.1.7 on 2023-06-18 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0038_alter_placement_options_remove_placement_pagex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placement',
            options={'ordering': ('page', 'place_number')},
        ),
    ]

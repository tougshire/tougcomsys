# Generated by Django 4.1.7 on 2023-06-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0025_placement_event_date_until_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='type',
            field=models.IntegerField(choices=[(0, 'Article'), (1, 'Event List')], default=0, help_text='The type of placement', verbose_name='type'),
            preserve_default=False,
        ),
    ]

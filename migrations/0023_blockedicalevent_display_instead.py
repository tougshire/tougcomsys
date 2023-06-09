# Generated by Django 4.2.2 on 2023-06-16 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0022_blockedicalevent_ical'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockedicalevent',
            name='display_instead',
            field=models.ForeignKey(blank=True, help_text='Display this article instead of the actual ICAL event, on the date of the ical event', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tougcomsys.article'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-06-17 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0028_alter_articleplacement_placement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placement',
            name='event_date_until',
        ),
        migrations.AddField(
            model_name='ical',
            name='placement',
            field=models.ForeignKey(help_text='The placement which should display this ical', limit_choices_to={'type': 1}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tougcomsys.placement'),
        ),
        migrations.AddField(
            model_name='placement',
            name='event_list_start',
            field=models.IntegerField(default=0, help_text='For event lists, the start date of the event list, in days relative to the current date', verbose_name='event list start'),
        ),
        migrations.AddField(
            model_name='placement',
            name='events_list_length',
            field=models.IntegerField(default=366, help_text='For event lists, length in days of the list', verbose_name='event list length'),
        ),
    ]
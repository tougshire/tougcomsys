# Generated by Django 4.1.7 on 2023-06-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0026_placement_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='show_title',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1, help_text='If the title of the list should be shown. This is just a flag - the template has to be coded appropriately for this to work', verbose_name='show title'),
        ),
    ]

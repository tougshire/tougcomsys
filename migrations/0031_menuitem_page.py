# Generated by Django 4.1.7 on 2023-06-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0030_placement_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='page',
            field=models.IntegerField(default=0, help_text='The page on which this menu item should appear', verbose_name='page'),
        ),
    ]

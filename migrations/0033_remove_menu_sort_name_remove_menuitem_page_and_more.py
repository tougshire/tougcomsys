# Generated by Django 4.1.7 on 2023-06-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0032_alter_menuitem_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='sort_name',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='page',
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_number',
            field=models.IntegerField(default=0, help_text='A number to help determine the place of the menu in the template. For the default template, 0 is the pace for a top menu and 1 is the place a side menu', verbose_name='menu number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.IntegerField(default=0, help_text='The page on which this menu item should appear', verbose_name='page'),
        ),
    ]
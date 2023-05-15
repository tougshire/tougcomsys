# Generated by Django 4.1.7 on 2023-04-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0012_remove_menuitem_label_remove_menuitem_short_label_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='sort_number',
        ),
        migrations.AddField(
            model_name='menu',
            name='sort_name',
            field=models.SlugField(blank=True, help_text='A name for sorting.  The menu with the alphabetically earliest sort name is considered the main menu', verbose_name='sorting name'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='label',
            field=models.CharField(blank=True, help_text='The label of the menu item.  If left blank, the label of the link will be used', max_length=100, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='sort_name',
            field=models.CharField(blank=True, help_text='A name for sorting.  The item with the alphabetically earliest sort name is first', max_length=20),
        ),
        migrations.AlterField(
            model_name='menulink',
            name='label',
            field=models.CharField(help_text='The default label when added to menus', max_length=100, verbose_name='label'),
        ),
    ]

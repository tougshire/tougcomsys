# Generated by Django 4.1.7 on 2023-06-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0044_alter_articleimage_show_in_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='column_width',
            field=models.CharField(blank=True, choices=[('narrow', 'Narrow'), ('wide', 'Wide')], help_text='The width of the column. The template may ingore this setting either completely or for certain media types', max_length=20, null=True, verbose_name='column width'),
        ),
    ]

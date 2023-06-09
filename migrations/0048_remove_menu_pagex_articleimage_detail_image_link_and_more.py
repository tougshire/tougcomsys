# Generated by Django 4.1.7 on 2023-06-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0047_placement_font_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='pagex',
        ),
        migrations.AddField(
            model_name='articleimage',
            name='detail_image_link',
            field=models.URLField(blank=True, help_text='The link for the image if/when displayed detail content ( leave blank for default behavior )', verbose_name='detail image link'),
        ),
        migrations.AddField(
            model_name='articleimage',
            name='detail_image_link_attributes',
            field=models.CharField(blank=True, help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed detail content ( leave blank for default behavior )', max_length=70, verbose_name='detail image link attributes'),
        ),
        migrations.AlterField(
            model_name='articleimage',
            name='list_image_link',
            field=models.URLField(blank=True, help_text='The link for the image if/when displayed list content ( leave blank for default behavior )', verbose_name='list image link'),
        ),
        migrations.AlterField(
            model_name='articleimage',
            name='list_image_link_attributes',
            field=models.CharField(blank=True, help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed list content ( leave blank for default behavior )', max_length=70, verbose_name='list image link attributes'),
        ),
        migrations.AlterField(
            model_name='placement',
            name='font_size',
            field=models.CharField(choices=[('xl', 'XL'), ('l', 'L'), ('m', 'M'), ('s', 'S'), ('xs', 'XS')], default='m', help_text='The relative font size. The template may ingore this setting either completely or for certain media types', max_length=8, verbose_name='font size'),
        ),
    ]

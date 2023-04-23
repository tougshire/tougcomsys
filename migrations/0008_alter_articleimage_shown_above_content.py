# Generated by Django 4.1.7 on 2023-04-23 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0007_remove_articleimage_above_content_image_attributes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimage',
            name='shown_above_content',
            field=models.BooleanField(default=False, help_text='If this image should be displayed above the content in a detail view of the articles', verbose_name='shown above content'),
        ),
    ]

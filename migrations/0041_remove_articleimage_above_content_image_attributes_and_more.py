# Generated by Django 4.1.7 on 2023-06-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0040_page_column_widths'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleimage',
            name='above_content_image_attributes',
        ),
        migrations.RemoveField(
            model_name='articleimage',
            name='shown_above_content',
        ),
        migrations.RemoveField(
            model_name='articleimage',
            name='shown_below_content',
        ),
        migrations.RemoveField(
            model_name='articleimage',
            name='shown_on_list',
        ),
        migrations.AddField(
            model_name='articleimage',
            name='shown_in_detail',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Above Content'), (2, 'Right of Content'), (3, 'Below Content'), (4, 'Left of Content')], default=0, help_text='If and where this image should be displayed with in a detail view of this article', verbose_name='shown in detail view'),
        ),
        migrations.AddField(
            model_name='articleimage',
            name='shown_in_list',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Above Content'), (2, 'Right of Content'), (3, 'Below Content'), (4, 'Left of Content')], default=0, help_text="If and where this image should be displayed with this article's headline and summary on a list of articles", verbose_name='shown in list view'),
        ),
        migrations.AlterField(
            model_name='articleimage',
            name='list_image_attributes',
            field=models.CharField(blank=True, default='', help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed list content', max_length=200, verbose_name='list image attributes'),
        ),
    ]

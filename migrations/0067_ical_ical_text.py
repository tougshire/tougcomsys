# Generated by Django 4.2.4 on 2023-10-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0066_alter_article_detail_image_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ical',
            name='ical_text',
            field=models.TextField(blank=True, verbose_name='ical_text'),
        ),
    ]

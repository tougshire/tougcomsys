# Generated by Django 4.1.7 on 2023-06-18 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0037_remove_menuitem_link_menuitem_article_menuitem_page_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placement',
            options={'ordering': ('page', '-place_number')},
        ),
        migrations.RemoveField(
            model_name='placement',
            name='pagex',
        ),
    ]

# Generated by Django 4.1.7 on 2023-06-17 20:56

from django.db import migrations
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0031_menuitem_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': (django.db.models.functions.text.Upper('sort_name'),)},
        ),
    ]

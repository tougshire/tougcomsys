# Generated by Django 4.2.4 on 2024-01-01 00:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tougcomsys", "0070_alter_article_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="A URL friendly representation - usually a variation of the name",
                max_length=150,
                verbose_name="slug",
            ),
        ),
    ]

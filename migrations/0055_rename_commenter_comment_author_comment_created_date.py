# Generated by Django 4.2 on 2023-07-15 14:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0054_comment_comment_text_alter_article_allow_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commenter',
            new_name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, help_text='The date the comment was created'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0064_alter_article_options_remove_article_sortable_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='detail_image_link',
            field=models.URLField(default='', help_text='The link that clicking on the image will take you to.  By default clicking on the image will open the image in a new link', verbose_name='detail image link'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='list_image_link',
            field=models.URLField(default='', help_text='The link that clicking on the image will take you to.  By default clicking on the list image will take you to the article', verbose_name='list image link'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, help_text='A URL friendly representation - usually a variation of the headline', max_length=150, verbose_name='slug'),
        ),
    ]

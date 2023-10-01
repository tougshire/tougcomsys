# Generated by Django 4.2.4 on 2023-09-30 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tougcomsys', '0065_article_detail_image_link_article_list_image_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='detail_image_link',
            field=models.URLField(blank=True, help_text='The link that clicking on the image will take you to.  By default clicking on the image will open the image in a new link', verbose_name='detail image link'),
        ),
        migrations.AlterField(
            model_name='article',
            name='list_image_link',
            field=models.URLField(blank=True, help_text='The link that clicking on the image will take you to.  By default clicking on the list image will take you to the article', verbose_name='list image link'),
        ),
    ]
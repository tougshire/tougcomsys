# Generated by Django 4.1.7 on 2023-04-22 23:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tougcomsys', '0002_alter_placement_show_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='The title or headline of the article', max_length=100, verbose_name='Headline')),
                ('subheadline', models.CharField(blank=True, help_text='The optional subtitle title of the article', max_length=100, verbose_name='Headline')),
                ('content_format', models.CharField(choices=[('markdown', 'markdown'), ('html', 'html')], default='markdown', help_text='The format (or markup method) used for the content', max_length=20, verbose_name='content format')),
                ('content', models.TextField(blank=True, help_text='The content of the post', verbose_name='content')),
                ('summary_format', models.CharField(choices=[('same', 'same as content'), ('markdown', 'markdown'), ('html', 'html')], default='same', help_text='The format (or markup method) used for the summary', max_length=20, verbose_name='summary format')),
                ('summary', models.TextField(blank=True, help_text='A shorter version of the content', verbose_name='summary')),
                ('show_author', models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Use Placement Choice')], default=2, help_text='If the author should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work', verbose_name='show author')),
                ('show_updated', models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Use Placement Choice')], default=2, help_text='If the updated date should be shown in the detail view. This is just a flag - the template has to be coded appropriately for this to work', verbose_name='show updated')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='The date/time this article was created', verbose_name='created')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='The date/time this article was created', verbose_name='updated')),
                ('sortable_date', models.DateTimeField(default=datetime.datetime.now, help_text='The modifiable date used for sorting, normally used only if this is a post, and in the admin panel for pages.  Later dates normally appear list earlier dates', null=True, verbose_name='sortable date')),
                ('sticky', models.BooleanField(default=False, help_text='If this post is stuck to the top. This is used before sortable date', verbose_name='sticky')),
                ('draft_status', models.IntegerField(choices=[(7, 'published'), (3, 'archived'), (0, 'draft')], default=0, help_text='If this post is a draft, which only displays in preview mode', verbose_name='draft status')),
                ('slug', models.SlugField(help_text='The slug used to refer to the image in this post (refer to the image with {{ img:my-image }}) if my-image is the slug', verbose_name='slug')),
                ('author', models.ForeignKey(blank=True, help_text='The user who created ths article', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-sticky', '-sortable_date'),
            },
        ),
        migrations.CreateModel(
            name='ArticlePlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(help_text='The article which is to be placed on the site', on_delete=django.db.models.deletion.CASCADE, to='tougcomsys.article')),
                ('placement', models.ForeignKey(blank=True, help_text='The placement on the home page', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tougcomsys.placement')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shown_on_list', models.BooleanField(default=False, help_text="If this image should be displayed with this article's headline and summary on a list of articles", verbose_name='shown on list')),
                ('shown_above_content', models.BooleanField(default=False, help_text='If this image should be displayed list the content in a detail view of the articles', verbose_name='shown list content')),
                ('shown_below_content', models.BooleanField(default=False, help_text='If this image should be displayed below the content in a detail view of the articles', verbose_name='shown below content')),
                ('is_featured', models.BooleanField(default=False, help_text='If this image should be featured, for use in Social Media links', verbose_name='is featured')),
                ('list_image_attributes', models.CharField(blank=True, help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed in a list', max_length=200, verbose_name='above content attributes')),
                ('below_content_image_attributes', models.CharField(blank=True, help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed below content', max_length=200, verbose_name='below content attributes')),
                ('below_content_image_link', models.URLField(blank=True, help_text='The link for the image if/when displayed below content', verbose_name='below content link')),
                ('below_content_link_attributes', models.CharField(blank=True, help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed below content', max_length=70, verbose_name='below content link attributes')),
                ('above_content_image_attributes', models.CharField(blank=True, help_text='The attributes (ie style="width:60%") for the image for if/when the image is displayed list content', max_length=200, verbose_name='list content attributes')),
                ('above_content_image_link', models.URLField(blank=True, help_text='The link for the image if/when displayed list content', verbose_name='list content link')),
                ('above_content_link_attributes', models.CharField(blank=True, help_text='The attributes (ie target="_blank") for the link for if/when the image is displayed list content', max_length=70, verbose_name='list content link attributes')),
                ('article', models.ForeignKey(help_text='The article to which the image is attached', on_delete=django.db.models.deletion.CASCADE, to='tougcomsys.article')),
                ('image', models.ForeignKey(blank=True, help_text='The image to add to the article', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tougcomsys.image')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleEventdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whenday', models.DateField(help_text='If the article is an event, the date of the event', verbose_name='date')),
                ('article', models.ForeignKey(help_text='If the article is an event, the article to which this event date belongs', on_delete=django.db.models.deletion.CASCADE, to='tougcomsys.article')),
            ],
            options={
                'ordering': ('whenday', 'article'),
            },
        ),
    ]

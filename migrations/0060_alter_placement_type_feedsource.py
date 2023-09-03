# Generated by Django 4.2.4 on 2023-08-14 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0010_enclosure_description_enclosure_medium'),
        ('tougcomsys', '0059_articleplacement_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement',
            name='type',
            field=models.IntegerField(choices=[(0, 'Article List'), (1, 'Event List'), (2, 'RSS Feed')], help_text='The type of placement', verbose_name='type'),
        ),
        migrations.CreateModel(
            name='FeedSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placement', models.ForeignKey(help_text='The placement on the template on which this feed should be displayed', null=True, on_delete=django.db.models.deletion.CASCADE, to='tougcomsys.placement')),
                ('source', models.ForeignKey(help_text='The source (set up in the Feeds app)', on_delete=django.db.models.deletion.CASCADE, to='feeds.source')),
            ],
        ),
    ]
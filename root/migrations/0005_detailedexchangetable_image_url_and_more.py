# Generated by Django 4.0.1 on 2022-04-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_alter_detailednfttable_stat_table_container_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailedexchangetable',
            name='image_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='exchangetable',
            name='image_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='nfttable',
            name='image_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]

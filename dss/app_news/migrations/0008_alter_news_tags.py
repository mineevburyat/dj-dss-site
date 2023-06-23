# Generated by Django 4.2.1 on 2023-06-23 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tags', '0002_alter_tag_table'),
        ('app_news', '0007_alter_news_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app_tags.tag'),
        ),
    ]

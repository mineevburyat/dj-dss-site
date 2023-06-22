# Generated by Django 4.2.1 on 2023-06-22 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_news", "0005_news_important_news_tags_news_valid_until_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="date_activation",
            field=models.DateTimeField(
                default=datetime.datetime.now, verbose_name="дата активации"
            ),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-20 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_news", "0003_alter_news_content_alter_news_date_public_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="slug",
            field=models.SlugField(max_length=110, unique=True),
        ),
    ]
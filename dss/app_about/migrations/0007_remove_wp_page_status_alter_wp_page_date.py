# Generated by Django 4.2.1 on 2023-12-01 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_about', '0006_alter_wp_page_date_alter_wp_page_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wp_page',
            name='status',
        ),
        migrations.AlterField(
            model_name='wp_page',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 1, 14, 47, 28, 797671, tzinfo=datetime.timezone.utc), verbose_name='дата создания'),
        ),
    ]

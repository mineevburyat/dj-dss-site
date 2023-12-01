# Generated by Django 4.2.1 on 2023-12-01 11:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_about', '0004_typedocument_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='WP_Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 12, 1, 11, 24, 44, 959960, tzinfo=datetime.timezone.utc), verbose_name='дата создания')),
                ('slug', models.SlugField(max_length=150)),
                ('status', models.CharField(max_length=25)),
                ('template', models.CharField(max_length=50)),
                ('old_link', models.URLField(max_length=500)),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField(max_length=3000)),
                ('excerpt', models.TextField(max_length=1500)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_about.wp_page', verbose_name='родительская страница')),
            ],
            options={
                'verbose_name': 'страница',
                'verbose_name_plural': 'страницы',
            },
        ),
    ]

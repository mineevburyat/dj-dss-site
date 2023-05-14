# Generated by Django 4.2.1 on 2023-05-13 04:29

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='название услуги')),
                ('descriprion', ckeditor_uploader.fields.RichTextUploadingField(max_length=1000, verbose_name='краткое описание')),
                ('category', models.CharField(choices=[('Spt', 'Спортивные услуги'), ('Sec', 'Спортивные секции'), ('Oth', 'Прочие услуги')], max_length=4)),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
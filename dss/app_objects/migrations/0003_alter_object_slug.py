# Generated by Django 4.2.1 on 2023-05-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_objects', '0002_remove_object_contacts_object_descriprion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='slug',
            field=models.SlugField(help_text='только латинские буквы и цифры', max_length=15, unique=True, verbose_name='slug имя в url'),
        ),
    ]
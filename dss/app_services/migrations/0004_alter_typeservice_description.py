# Generated by Django 4.2.1 on 2023-06-01 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_services', '0003_typeservice_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeservice',
            name='description',
            field=models.TextField(default='необходимо заполнить', help_text='кратко описываем группу услуг', max_length=400, verbose_name='Описание группы услуг'),
        ),
    ]
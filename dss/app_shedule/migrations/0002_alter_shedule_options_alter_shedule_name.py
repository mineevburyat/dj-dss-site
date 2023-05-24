# Generated by Django 4.2.1 on 2023-05-24 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shedule',
            options={'verbose_name': 'график работы подразделения', 'verbose_name_plural': 'графики работ подразделений'},
        ),
        migrations.AlterField(
            model_name='shedule',
            name='name',
            field=models.CharField(max_length=100, verbose_name='имя расписания'),
        ),
    ]

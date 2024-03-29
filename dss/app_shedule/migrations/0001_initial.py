# Generated by Django 4.2.1 on 2023-11-20 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='имя расписания')),
                ('opening_house', models.JSONField(help_text='время в json виде, согласно схемы', verbose_name='время работы')),
                ('exeption_day', models.JSONField(help_text='перечисляем нерабочие и частично рабочие дни', verbose_name='исключительные дни')),
            ],
            options={
                'verbose_name': 'график работы подразделения',
                'verbose_name_plural': 'графики работ подразделений',
            },
        ),
    ]

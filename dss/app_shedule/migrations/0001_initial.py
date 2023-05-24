# Generated by Django 4.2.1 on 2023-05-22 15:22

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
                ('name', models.CharField(help_text='режим работы услуги или ресурса', max_length=100, verbose_name='имя расписания')),
                ('opening_house', models.JSONField(help_text='время в json виде, согласно схемы', verbose_name='время работы')),
                ('exeption_day', models.JSONField(help_text='перечисляем нерабочие и частично рабочие дни', verbose_name='исключительные дни')),
            ],
        ),
    ]
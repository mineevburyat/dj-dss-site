# Generated by Django 4.2.1 on 2023-05-27 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65, unique=True, verbose_name='название')),
                ('phone', models.CharField(max_length=15, verbose_name='телефон')),
                ('phone_add', models.CharField(blank=True, max_length=5, null=True, verbose_name='добавочный')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='email')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]

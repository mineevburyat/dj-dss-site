# Generated by Django 4.1.4 on 2023-01-04 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportdss', '0023_alter_about_category_alter_contact_about_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='service',
            field=models.ManyToManyField(blank=True, help_text='выберите доступные на объекте спортивные и прочие услуги, спортивные секции. ', null=True, to='sportdss.service'),
        ),
    ]

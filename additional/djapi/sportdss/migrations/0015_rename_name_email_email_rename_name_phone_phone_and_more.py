# Generated by Django 4.1.4 on 2022-12-28 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportdss', '0014_contact_rename_descriprion_about_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='name',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='phone',
            old_name='name',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='workingmode',
            old_name='name',
            new_name='mode',
        ),
    ]

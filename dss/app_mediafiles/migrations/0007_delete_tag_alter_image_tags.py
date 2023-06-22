# Generated by Django 4.2.1 on 2023-06-22 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_tags", "0001_initial"),
        ("app_mediafiles", "0006_alter_image_slug"),
    ]

    operations = [
        migrations.DeleteModel(name="Tag",),
        migrations.AlterField(
            model_name="image",
            name="tags",
            field=models.ManyToManyField(blank=True, to="app_tags.tag"),
        ),
    ]
# Generated by Django 2.1.7 on 2020-06-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_recipeimage_image_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeprocessimage',
            name='image_path',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]

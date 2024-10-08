# Generated by Django 5.1.1 on 2024-10-05 09:43

import cloudinary.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_remove_property_image_alter_propertyimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='propertyimage',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productpicture_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpicture',
            name='picture',
            field=models.ImageField(upload_to='media/productImages'),
        ),
    ]